# --- START OF FINAL main.py ---

import sys
import os
import asyncio
import logging
from dotenv import load_dotenv

# --- Apply Windows Event Loop Policy FIRST ---
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# --- Load Environment Variables ---
load_dotenv()

# --- Configure Logging ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(module)s.%(funcName)s:%(lineno)d - %(message)s",
    level=os.getenv("LOG_LEVEL", "INFO").upper(),
    handlers=[logging.StreamHandler(sys.stdout)]
)
# Set levels for noisy libraries to avoid spamming your logs
logging.getLogger("httpx").setLevel(os.getenv("LOG_LEVEL_HTTPX", "WARNING").upper())
logging.getLogger("telegram.ext.ExtBot").setLevel(os.getenv("LOG_LEVEL_PTB_EXTBOT", "WARNING").upper())

logger = logging.getLogger(__name__)

# --- Import Bot Logic ---
try:
    from telegram import Update
    # ## ADDED HTTPXRequest FOR CUSTOM TIMEOUTS ##
    from telegram.request import HTTPXRequest
    from telegram.ext import ContextTypes, ApplicationBuilder, PicklePersistence
    from bot.telegram_bot import add_all_handlers, set_bot_commands
    from bot.persistence import create_persistence_instance
except (ImportError, EnvironmentError) as e:
    logger.critical(f"Failed to initialize bot components. Please check imports and .env file. Error: {e}",
                    exc_info=True)
    sys.exit(1)


# --- Global Error Handler ---
async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Logs errors and sends a message to the user on error."""
    logger.error("Global Error Handler caught an exception:", exc_info=context.error)

    if isinstance(update, Update) and update.effective_chat:
        try:
            # You can customize this message
            error_message = "I'm sorry, an unexpected error occurred. The developer has been notified."
            await context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)
        except Exception as e_send:
            logger.error(f"Failed to send error message to user {update.effective_chat.id}: {e_send}")


# --- Post-Init Function for Setup Tasks ---
async def post_init_tasks(application: "Application"):
    """Runs after the application is initialized but before polling starts."""
    logger.info("Running post-initialization tasks...")

    await set_bot_commands(application)

    logger.info("Deleting any existing webhook to ensure a clean polling start...")
    await application.bot.delete_webhook(drop_pending_updates=True)

    logger.info("Post-initialization tasks complete. Bot is now ready and will start polling.")


def main() -> None:
    """The main function that sets up and runs the bot."""

    logger.info("Application starting up...")

    # 1. Create the persistence object
    persistence = create_persistence_instance()

    # ## ADDED: Configure custom request timeouts for better network resilience ##
    # The default of 5s can be too short, causing 'TimedOut' errors during startup.
    # We increase the connection timeout to 10s and the read timeout to 20s.
    request = HTTPXRequest(connect_timeout=10.0, read_timeout=20.0)

    # 2. Use the ApplicationBuilder to construct the bot
    application = (
        ApplicationBuilder()
        .token(os.getenv("TELEGRAM_BOT_TOKEN"))
        .persistence(persistence)
        .request(request)  # ## MODIFIED: Pass the custom request object ##
        .post_init(post_init_tasks)
        .build()
    )

    # 3. Register all your handlers from telegram_bot.py
    add_all_handlers(application)

    # 4. Register the global error handler
    application.add_error_handler(global_error_handler)

    # 5. Run the bot
    # This is a blocking call that starts everything. It will run until you
    # press Ctrl+C or send a shutdown signal to the process.
    logger.info("Starting bot... Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    logger.info("--- Bot instance starting ---")
    main()
    logger.info("--- Bot instance finished ---")