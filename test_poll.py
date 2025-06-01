# test_poll.py (ensure it looks like this simplified version)
import sys
import os
import asyncio

if sys.platform == "win32":
    print("INFO: Running on Windows, attempting to set WindowsSelectorEventLoopPolicy.")
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
else:
    print(f"INFO: Not running on Windows (platform: {sys.platform}), using default event loop policy.")

import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, ContextTypes, MessageHandler, filters

# --- Load Environment Variables FIRST ---
if not load_dotenv():
    print("Warning: .env file not found or empty.", file=sys.stderr)
else:
    print("Successfully loaded environment variables from .env file.")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    print("CRITICAL: TELEGRAM_BOT_TOKEN not found in environment. Exiting.", file=sys.stderr)
    exit(1)

# --- Configure Basic Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
    level=logging.DEBUG
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("telegram.ext.dispatcher").setLevel(logging.DEBUG)
logging.getLogger("telegram.ext.Application").setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)

async def simple_update_logger(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.critical(f"--- MINIMAL TEST: RAW UPDATE RECEIVED --- Type: {type(update)}, Content: {update}")
    if update.message:
        logger.critical(f"Minimal Test - Message Text: {update.message.text}")


async def main() -> None:
    logger.info(f"Minimal Test: Building application with token ...{TELEGRAM_BOT_TOKEN[-6:]}")
    # We only need the bot instance for this hack, not the full application
    from telegram import Bot
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    # If you want to use application.bot and also have simple_update_logger registered
    # you'd need application = Application.builder()... as before
    # For this specific hack, let's focus on bot.get_updates
    # application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    # application.add_handler(MessageHandler(filters.ALL, simple_update_logger))
    # await application.initialize() # Initializes bot and dispatcher

    logger.info("Minimal Test: Initializing bot directly...")
    await bot.initialize()  # Initialize the bot instance

    # Manually delete webhook to ensure polling mode
    try:
        logger.info("Manually deleting webhook...")
        await bot.delete_webhook()
        logger.info("Webhook manually deleted.")
    except Exception as e_wh:
        logger.error(f"Error manually deleting webhook: {e_wh}")

    logger.info("Minimal Test: Starting manual update fetching loop.")
    offset = 0
    while True:
        try:
            logger.debug(f"Manually calling get_updates with offset: {offset}")
            updates = await bot.get_updates(offset=offset, timeout=10, allowed_updates=Update.ALL_TYPES)
            if updates:
                logger.critical(f"MANUAL FETCH - Updates received: {updates}")
                for update_obj in updates:
                    logger.critical(f"MANUAL FETCH - Processing update_id: {update_obj.update_id}")
                    # Manually call your handler (or a simplified version)
                    # This bypasses the dispatcher entirely.
                    # For a real handler, you'd need a ContextTypes.DEFAULT_TYPE mock or build one.
                    # Let's just log the update content directly from simple_update_logger's logic
                    logger.critical(
                        f"--- MINIMAL TEST (MANUAL): RAW UPDATE RECEIVED --- Type: {type(update_obj)}, Content: {update_obj}")
                    if update_obj.message:
                        logger.critical(f"Minimal Test (MANUAL) - Message Text: {update_obj.message.text}")

                    offset = update_obj.update_id + 1
            else:
                logger.debug("Manually called get_updates, no new updates.")
        except Exception as e_manual_poll:
            logger.error(f"Error in manual polling loop: {e_manual_poll}", exc_info=True)

        await asyncio.sleep(1)  # Poll every 1 second

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Minimal Test: Shutdown signal received.")
    except Exception as e:
        logger.critical(f"Minimal Test: An unhandled exception occurred: {e}", exc_info=True)
    finally:
        logger.info("Minimal Test: Shutting down.")