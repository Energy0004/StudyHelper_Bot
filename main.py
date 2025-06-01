# --- START OF FILE main.py (Manual Polling Workaround) ---

import sys
import os
import asyncio

# --- Apply WindowsSelectorEventLoopPolicy FIRST ---
if sys.platform == "win32":
    print("INFO: Main project on Windows, attempting to set WindowsSelectorEventLoopPolicy.")
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception as e_policy:
        print(f"WARNING: Could not set WindowsSelectorEventLoopPolicy: {e_policy}", file=sys.stderr)
else:
    print(f"INFO: Main project not on Windows (platform: {sys.platform}), using default event loop policy.")

from dotenv import load_dotenv

# --- Load Environment Variables ---
if not load_dotenv():
    print("Warning: .env file not found or empty. Relying on system environment variables.", file=sys.stderr)
else:
    print("Successfully loaded environment variables from .env file.")

import logging
import telegram  # For telegram.error types
from telegram import Update
from telegram.ext import ContextTypes, PicklePersistence
from telegram.error import BadRequest

# --- Import Bot Logic AFTER loading .env and configuring logging ---
# Also after event loop policy is set.
try:
    from bot.telegram_bot import get_application_with_persistence, \
        set_bot_commands  # TELEGRAM_BOT_TOKEN is used within telegram_bot.py
except EnvironmentError as e:
    # Basic logger if main logger isn't set up yet
    logging.basicConfig(level=logging.CRITICAL)
    init_logger = logging.getLogger(__name__ + "_init_fail")
    init_logger.critical(f"Failed to initialize bot components due to missing environment variable: {e}")
    sys.exit(1)
except ImportError as e:
    logging.basicConfig(level=logging.CRITICAL)
    init_logger = logging.getLogger(__name__ + "_init_fail")
    init_logger.critical(f"Failed to import bot modules. Error: {e}")
    sys.exit(1)
except Exception as e:  # Catch-all for any other unexpected error during setup
    logging.basicConfig(level=logging.CRITICAL)
    init_logger = logging.getLogger(__name__ + "_init_fail")
    init_logger.critical(f"An unexpected error occurred during bot module loading or setup: {e}", exc_info=True)
    sys.exit(1)

# --- Configure Logging (after imports to ensure logger names are correct) ---
LOG_LEVEL_FROM_ENV = os.getenv("LOG_LEVEL", "INFO").upper()
numeric_log_level = getattr(logging, LOG_LEVEL_FROM_ENV, None)
if not isinstance(numeric_log_level, int):
    print(f"Warning: Invalid LOG_LEVEL '{LOG_LEVEL_FROM_ENV}'. Defaulting to INFO.", file=sys.stderr)
    numeric_log_level = logging.INFO

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
    level=numeric_log_level,
    handlers=[logging.StreamHandler(sys.stdout)]
)

logging.getLogger("httpx").setLevel(os.getenv("LOG_LEVEL_HTTPX", "WARNING").upper())
logging.getLogger("httpcore").setLevel(os.getenv("LOG_LEVEL_HTTPCORE", "WARNING").upper())
logging.getLogger("telegram.ext.Application").setLevel(os.getenv("LOG_LEVEL_PTB_APPLICATION", "DEBUG").upper())
logging.getLogger("telegram.bot").setLevel(os.getenv("LOG_LEVEL_PTB_BOT", "DEBUG").upper())  # For bot.get_updates
logging.getLogger("telegram.ext.ExtBot").setLevel(os.getenv("LOG_LEVEL_PTB_EXTBOT", "DEBUG").upper())
logging.getLogger("telegram.ext.Updater").setLevel(
    os.getenv("LOG_LEVEL_PTB_UPDATER", "WARNING").upper())  # Not actively used now
logging.getLogger("telegram.ext.dispatcher").setLevel(
    os.getenv("LOG_LEVEL_PTB_DISPATCHER", "DEBUG").upper())  # To see process_update work

logging.getLogger("bot.gemini_utils").setLevel(os.getenv("LOG_LEVEL_GEMINI", "INFO").upper())
logging.getLogger("bot.telegram_bot").setLevel(os.getenv("LOG_LEVEL_TELEGRAM_BOT", "DEBUG").upper())

logger = logging.getLogger(__name__)  # Logger for main.py


async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Global Error Handler: Exception while handling an update:", exc_info=context.error)
    # ... (rest of your global_error_handler) ...
    if isinstance(context.error, BadRequest) and "message is not modified" in str(context.error).lower():
        logger.warning(
            f"Global Error Handler: Suppressed user notification for 'message not modified' error: {context.error}")
        return
    if isinstance(update, Update) and update.effective_chat:
        try:
            error_message_text = "Apologies, an unexpected error occurred on my end processing your request. The developers have been notified."
            if context.error:
                error_message_text += f"\nError: {str(context.error)[:100]}"
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=error_message_text
            )
        except Exception as e_send:
            logger.error(
                f"Global Error Handler: Failed to send error message to user (chat_id: {update.effective_chat.id}): {e_send}",
                exc_info=True)
    else:
        logger.warning(
            "Global Error Handler: Could not send error message as 'update' or 'effective_chat' was not available.")


async def main() -> None:
    logger.info("Application starting up with MANUAL POLLING WORKAROUND...")

    application = None
    bot_persistence = None

    try:
        persistence_dir = os.getenv("PERSISTENCE_DIR", "bot_data")
        persistence_filename = os.getenv("PERSISTENCE_FILENAME", "bot_persistence.pkl")
        persistence_filepath = os.path.join(persistence_dir, persistence_filename)
        os.makedirs(persistence_dir, exist_ok=True)
        bot_persistence = PicklePersistence(filepath=persistence_filepath)
        logger.info(f"Using PicklePersistence with file: {persistence_filepath}")

        application = get_application_with_persistence(bot_persistence)
        application.add_error_handler(global_error_handler)
        logger.info("Global error handler registered.")

        logger.info("Initializing application instance (bot, dispatcher, persistence)...")
        await application.initialize()
        logger.info("Application instance initialized.")

        await set_bot_commands(application)

        logger.info("Attempting to manually delete webhook (if any)...")
        if application.bot:
            try:
                await application.bot.delete_webhook(drop_pending_updates=True)
                logger.info("Webhook manually deleted or was not set.")
            except Exception as e_wh:
                logger.warning(f"Could not delete webhook during startup: {e_wh}")
        else:
            logger.warning("application.bot is not available, cannot delete webhook.")

        logger.info("Starting MANUAL polling and processing loop...")
        offset = 0

        while True:
            try:
                if not application.bot:
                    logger.error("Main loop: application.bot is not available! Waiting...")
                    await asyncio.sleep(30)
                    continue

                updates = await application.bot.get_updates(
                    offset=offset,
                    timeout=20,
                    allowed_updates=Update.ALL_TYPES
                )

                if updates:
                    logger.debug(f"MANUAL LOOP: Received {len(updates)} update(s).")
                    for update_obj in updates:
                        logger.debug(f"MANUAL LOOP: Processing update_id: {update_obj.update_id}")
                        try:
                            await application.process_update(update_obj)
                        except Exception as e_process_update:
                            logger.error(
                                f"MANUAL LOOP: Error in application.process_update for update {update_obj.update_id}: {e_process_update}",
                                exc_info=True)
                        offset = update_obj.update_id + 1

            except telegram.error.NetworkError as ne:
                logger.warning(f"MANUAL LOOP: NetworkError: {ne}. Retrying in 15 seconds.")
                await asyncio.sleep(15)
            except telegram.error.RetryAfter as ra:
                logger.warning(f"MANUAL LOOP: Flood control. RetryAfter: {ra.retry_after} seconds.")
                await asyncio.sleep(ra.retry_after + 1)
            except telegram.error.TimedOut:
                logger.debug("MANUAL LOOP: get_updates timed out (normal for long polling). Continuing.")
            except telegram.error.TelegramError as te:
                logger.error(f"MANUAL LOOP: TelegramError: {te}. Retrying in 30 seconds.", exc_info=True)
                await asyncio.sleep(30)
            except Exception as e_outer_loop:
                logger.error(f"MANUAL LOOP: Unexpected critical error: {e_outer_loop}", exc_info=True)
                await asyncio.sleep(20)

            await asyncio.sleep(0.05)

    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutdown signal received (KeyboardInterrupt/SystemExit).")
    except Exception as e:
        logger.critical(f"CRITICAL Unhandled exception in main function: {e}", exc_info=True)
    finally:
        logger.info("Application attempting to shut down gracefully...")
        if application:
            logger.info("Shutting down application instance...")
            await application.shutdown()
        else:
            logger.warning("Application object was not available for shutdown.")
        logger.info("Application shutdown procedures complete.")


if __name__ == '__main__':
    # asyncio.run(clear_webhook_once())
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if "Cannot close a running event loop" in str(e) or "Event loop is closed" in str(e):
            logging.getLogger(__name__).warning(f"Known asyncio loop issue during final interpreter shutdown: {e}")
        else:
            logging.getLogger(__name__).critical(f"Unhandled RuntimeError in asyncio.run(main()): {e}", exc_info=True)
            raise
    except Exception as e_top_level:
        logging.getLogger(__name__).critical(f"Top-level unhandled exception: {e_top_level}", exc_info=True)
        sys.exit(1)