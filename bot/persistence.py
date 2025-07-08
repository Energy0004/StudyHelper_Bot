# --- START OF FILE bot/persistence.py ---

import os
import logging
from telegram.ext import PicklePersistence

logger = logging.getLogger(__name__)


def create_persistence_instance() -> PicklePersistence:
    """Creates and returns a PicklePersistence instance based on environment variables."""

    try:
        persistence_dir = os.getenv("PERSISTENCE_DIR", "bot_data")
        persistence_filename = os.getenv("PERSISTENCE_FILENAME", "bot_persistence.pkl")

        # Ensure the directory exists
        os.makedirs(persistence_dir, exist_ok=True)

        persistence_filepath = os.path.join(persistence_dir, persistence_filename)

        logger.info(f"Setting up PicklePersistence at: {persistence_filepath}")

        return PicklePersistence(filepath=persistence_filepath)

    except Exception as e:
        logger.error(f"Could not create persistence directory or instance: {e}", exc_info=True)
        # Fallback to in-memory persistence if file-based fails
        logger.warning("Falling back to in-memory persistence. Bot state will be lost on restart.")
        return PicklePersistence(store_data=False)  # Or just return None and handle it in main

# --- END OF FILE bot/persistence.py ---