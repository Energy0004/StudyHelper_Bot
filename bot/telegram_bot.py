# --- START OF FILE telegram_bot.py ---

import re
import time
from collections import OrderedDict
import os
import logging
import asyncio
from functools import wraps

import httpx
import requests
from bs4 import BeautifulSoup
from openai import OpenAI, RateLimitError, APIConnectionError

from localization import COMMANDS
from telegram import Update, constants, Message
import fitz
import telegram
from docx import Document as DocxDocument

from telegram import Update, constants, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    BasePersistence,
    CallbackQueryHandler
)
from telegram.error import BadRequest, RetryAfter

from localization import get_template, DEFAULT_LOC_LANG
# from telegram.request import HTTPXRequest # Temporarily commented out for diagnostics

# Assuming gemini_utils.py is in the same directory or a correctly configured package
from .gemini_utils import ask_gemini_stream, ask_gemini_vision_stream, ask_gemini_non_stream

logger = logging.getLogger(__name__)  # This will be 'bot.telegram_bot'

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai_client = None
if not OPENAI_API_KEY:
    logger.warning("OPENAI_API_KEY not found in .env. Voice message transcription will be disabled.")
else:
    # Initialize the OpenAI client
    openai_client = OpenAI(api_key=OPENAI_API_KEY)
    logger.info("OpenAI client initialized successfully for voice transcriptions.")

try:
    import pytesseract
    from PIL import Image, UnidentifiedImageError
    import io  # For BytesIO if converting images

    TESSERACT_AVAILABLE = True

    # Explicitly set Tesseract command path (RECOMMENDED)
    tesseract_exe_path_options = [
        r'C:\Program Files\Tesseract-OCR\tesseract.exe',
        r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    ]
    found_tesseract_path = None
    for path_option in tesseract_exe_path_options:
        if os.path.exists(path_option):
            found_tesseract_path = path_option
            break
    if found_tesseract_path:
        pytesseract.pytesseract.tesseract_cmd = found_tesseract_path
        logger.info(f"Pytesseract tesseract_cmd set to: {found_tesseract_path}")
    else:
        logger.warning("Tesseract OCR executable not found in common predefined paths. Relying on system PATH.")

except ImportError:
    logger.warning("Pytesseract or Pillow not found. OCR for images will not be available via Tesseract.")
    TESSERACT_AVAILABLE = False

TEMP_DIR = "temp_downloads"

ADMIN_ID_STR = os.getenv("TELEGRAM_ADMIN_ID")
ADMIN_ID = int(ADMIN_ID_STR) if ADMIN_ID_STR and ADMIN_ID_STR.isdigit() else None

if not ADMIN_ID:
    logger.warning("TELEGRAM_ADMIN_ID not found or invalid. Admin commands will not be available.")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if not TELEGRAM_BOT_TOKEN:
    logger.critical("CRITICAL: TELEGRAM_BOT_TOKEN not found.")
    raise EnvironmentError("TELEGRAM_BOT_TOKEN not found.")

try:
    MAX_CONVERSATION_TURNS = int(os.getenv("MAX_CONVERSATION_TURNS"))
except ValueError:
    logger.warning("MAX_CONVERSATION_TURNS in .env is not valid. Using default 5.")
    MAX_CONVERSATION_TURNS = 5

DEFAULT_SYSTEM_PROMPT_BASE = os.getenv(
    "DEFAULT_SYSTEM_PROMPT_BASE",
    """You are a helpful, accurate, and meticulous AI Study Helper. Your primary goal is to assist users in understanding educational material, solving problems, and learning new concepts.
    When a user provides text, an image, or a document, analyze it thoroughly and provide clear, concise, and informative explanations.
    If the input is a question or problem, guide the user towards the solution step-by-step, or explain the underlying principles.
    If the input is general material, summarize key points, explain complex terms, or suggest related topics for further study.
    Always strive for factual correctness and pedagogical effectiveness.
    Maintain a supportive and encouraging tone.

    **--- CRITICAL INSTRUCTIONS ON BEHAVIOR ---**

    **1. Tool Usage for Real-Time Information (MANDATORY):**
    You have access to a web search tool. If a user's query concerns any topic that requires up-to-date information (e.g., news, sports scores, current events, recent product announcements), you **MUST** use this tool.
    - Your internal knowledge is not current. You must assume it is outdated for recent events.
    - **DO NOT** state that you cannot access real-time information or that your knowledge is limited. This is false; your tool provides this capability. Refusing to use the tool is a failure to follow instructions.
    - Your primary action for such questions is to formulate a search query and call the `perform_web_search` tool.

    **2. Handling Sensitive Topics (MANDATORY):**
    When asked about potentially sensitive topics (such as politics, conflicts, or controversial subjects), your role is to act as a neutral information retriever.
    - **DO NOT** refuse the query or give a personal opinion.
    - **INSTEAD**, you **MUST** use the `perform_web_search` tool to find factual information.
    - Your response to the user must be an unbiased summary of the information found in the search results, clearly stating that it is based on this search.

    **--- END OF CRITICAL INSTRUCTIONS ---**

    **--- RESPONSE STRUCTURE AND READABILITY (MANDATORY) ---**
    To ensure your answers are easy to read and study from, you MUST structure your responses for maximum clarity. Avoid long, unbroken "walls of text".

    *   **Use Headings:** Introduce different sections of a long answer with bolded headings (e.g., `*Key Concepts*`).
    *   **Use Lists:** For sequences of steps, examples, or multiple points, ALWAYS use bulleted (`- `) or numbered (`1. `) lists.
    *   **Emphasize Keywords:** Highlight the most important terms using `*bold*` or `_italics_`.
    *   **Use Whitespace:** Generously use empty lines to separate paragraphs and distinct ideas.
    *   **Keep Paragraphs Short:** Aim for short, focused paragraphs.
    *   **Start with a Summary:** For complex topics, begin with a one or two-sentence summary.

    **--- END OF RESPONSE STRUCTURE INSTRUCTIONS ---**

    **--- TELEGRAM MARKDOWNV2 FORMATTING (ABSOLUTE RULES) ---**
    Your response will be parsed by Telegram's MarkdownV2 engine. Failure to follow these specific rules WILL cause display errors.

    *   **Bold:** Use single asterisks ONLY. Example: `*bold text*`.
    *   **Italics:** Use single underscores ONLY. Example: `_italic text_`.
    *   **Inline Code:** Use single backticks. Example: `` `inline code` ``.

    **LISTS (EXTREMELY IMPORTANT):**
    *   **Bulleted Lists:** You MUST use a hyphen followed by a space (`- `). Do NOT use asterisks (`*`) for lists.
    *   **Numbered Lists:** You MUST use a number, a period, and a space (`1. `).

    # ##################################################################
    # ## THE ONE NECESSARY MODIFICATION TO THE PROMPT IS HERE         ##
    # ##################################################################

    **CRITICAL PUNCTUATION RULE:**
    Punctuation marks like periods (.), exclamation marks (!), or commas (,) MUST be placed *outside* of bold or italic blocks to prevent parsing errors.
    - Correct: `This is *bold*.`
    - Incorrect: `*This is bold.*`
    - Correct: `This is _italic_, not bold.`
    - Incorrect: `_This is italic, not bold._`

    **FINAL CHECK:**
    Ensure every `*` and `_` is part of a correctly opened and closed pair.
    """
)

TELEGRAM_MAX_MESSAGE_LENGTH = 4096
STREAM_UPDATE_INTERVAL = 0.75

SUPPORTED_LANGUAGES = OrderedDict([
    ("en", "English"),
    ("es", "Español (Spanish)"),
    ("fr", "Français (French)"),
    ("de", "Deutsch (German)"),
    ("ru", "Русский (Russian)"),
    ("zh-CN", "简体中文 (Simplified Chinese)"),
    ("kk", "Қазақ тілі (Kazakh)"),
    ("ja", "日本語 (Japanese)"),
    ("ko", "한국어 (Korean)"),
    ("pt-BR", "Português (Brazilian Portuguese)"),
    ("it", "Italiano (Italian)"),
    ("ar", "العربية (Arabic)"),
    ("hi", "हिन्दी (Hindi)"),
    ("tr", "Türkçe (Turkish)"),
    ("nl", "Nederlands (Dutch)"),
    ("pl", "Polski (Polish)"),
    ("sv", "Svenska (Swedish)"),
    ("fi", "Suomi (Finnish)"),
    ("no", "Norsk (Norwegian)"),
    ("da", "Dansk (Danish)"),
    ("cs", "Čeština (Czech)"),
    ("hu", "Magyar (Hungarian)"),
    ("ro", "Română (Romanian)"),
    ("el", "Ελληνικά (Greek)"),
    ("he", "עברית (Hebrew)"),
    ("th", "ไทย (Thai)"),
    ("vi", "Tiếng Việt (Vietnamese)"),
    ("id", "Bahasa Indonesia (Indonesian)"),
    ("ms", "Bahasa Melayu (Malay)"),
    ("uk", "Українська (Ukrainian)"),
    ("uz", "Oʻzbekcha (Uzbek)"),
    ("zh-TW", "繁體中文 (Traditional Chinese)"),
    ("pt-PT", "Português (European Portuguese)"),
])

DEFAULT_LANGUAGE_CODE = "en"
LANGS_PER_PAGE = 6
BUTTONS_PER_ROW = 2
USER_REQUEST_COOLDOWN = 5

TELEGRAM_COMMAND_LANG_MAP = {
    "zh-CN": "zh",  # Simplified Chinese -> Chinese
    "zh-TW": "zh",  # Traditional Chinese -> Chinese (will show simplified commands)
    "pt-BR": "pt",  # Brazilian Portuguese -> Portuguese
    "pt-PT": "pt",  # European Portuguese -> Portuguese
    # All other standard two-letter codes like "en", "ru", "es", "de" are valid.
    # We don't need to add them here.
}

def build_feedback_keyboard(message_id: int) -> InlineKeyboardMarkup:
    """Builds the feedback keyboard for a given message."""
    keyboard = [[
        InlineKeyboardButton("👍", callback_data=f"feedback:up:{message_id}"),
        InlineKeyboardButton("👎", callback_data=f"feedback:down:{message_id}")
    ]]
    return InlineKeyboardMarkup(keyboard)


async def feedback_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles 👍 and 👎 feedback button presses."""
    query = update.callback_query

    try:
        # Expected format: "feedback:<vote>:<message_id>"
        _, vote, message_id_str = query.data.split(':')
        message_id = int(message_id_str)
    except (ValueError, IndexError):
        logger.error(f"Invalid feedback callback data format: {query.data}")
        await query.answer("Error processing feedback.", show_alert=True)
        return

    user_id = query.from_user.id
    logger.info(f"Feedback received: User {user_id} voted '{vote}' on message {message_id}.")

    # Increment stats for tracking
    if vote == 'up':
        increment_stat(context, "feedback_positive")
    elif vote == 'down':
        increment_stat(context, "feedback_negative")

    # Get localized "thank you" message for the toast notification
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)
    feedback_thanks_raw = get_template(
        "feedback_thanks",
        user_lang_code,
        default_val="Thank you for your feedback!"
    )

    try:
        # Acknowledge the press and remove the buttons from the message
        await query.edit_message_reply_markup(reply_markup=None)
        # Show a confirmation toast to the user
        await query.answer(text=feedback_thanks_raw)
    except BadRequest as e:
        if "message to edit not found" in str(e).lower():
            logger.warning(f"Could not find message {message_id} to remove feedback buttons. It may have been deleted.")
            await query.answer("Message not found.", show_alert=True)
        elif "message is not modified" in str(e).lower():
            # User might have clicked the same button twice. Silently acknowledge.
            await query.answer()
        else:
            logger.error(f"Error editing message to remove feedback buttons for message {message_id}: {e}")
            await query.answer("Could not update message.", show_alert=True)

def increment_stat(context: ContextTypes.DEFAULT_TYPE, stat_name: str, increment_by: int = 1):
    """
    Safely increments a statistic in context.bot_data.
    """
    if 'stats' not in context.bot_data:
        context.bot_data['stats'] = {}

    current_value = context.bot_data['stats'].get(stat_name, 0)
    context.bot_data['stats'][stat_name] = current_value + increment_by

def rate_limit(cooldown: int = USER_REQUEST_COOLDOWN):
    """
    A decorator to enforce a rate limit on a handler function.
    """

    def decorator(func):
        @wraps(func)
        async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            now = time.time()
            user_id = update.effective_user.id

            # Use a different key for the timestamp to avoid conflicts
            last_request_time = context.user_data.get('handler_last_request_time', 0)

            if now - last_request_time < cooldown:
                logger.warning(f"User {user_id} is being rate-limited for handler: {func.__name__}")

                if not context.user_data.get('rate_limit_warning_sent', False):
                    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)
                    wait_message = get_template(
                        "please_wait", user_lang_code,
                        cooldown=cooldown,
                        default_val=f"⏳ Please wait a moment. You can send a new request in {cooldown} seconds."
                    )
                    # Use a new message to avoid race conditions with placeholder edits
                    await update.message.reply_text(wait_message)
                    context.user_data['rate_limit_warning_sent'] = True
                return

            # If not rate-limited, reset the warning flag and proceed
            context.user_data['rate_limit_warning_sent'] = False

            # --- CRITICAL ---
            # We call the actual handler function FIRST.
            await func(update, context, *args, **kwargs)

            # --- CRITICAL ---
            # Only after the handler has completely finished its work, we update the timestamp.
            context.user_data['handler_last_request_time'] = time.time()

        return wrapped

    return decorator

# --- Helper to Download File ---
async def download_telegram_file(bot_instance: telegram.Bot, file_id: str, local_filename: str) -> bool:
    try:
        file_obj = await bot_instance.get_file(file_id)
        await file_obj.download_to_drive(local_filename)
        logger.info(f"File {file_id} downloaded to {local_filename}")
        return True
    except Exception as e:
        logger.error(f"Failed to download file {file_id}: {e}")
        return False


async def _core_ai_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        prompt_text: str,
        conversation_history: list
):
    """
    The core logic for interacting with Gemini, streaming the response, and handling fallbacks.

    This function is the central workhorse for all text-based AI interactions. It is called by
    various routing handlers (like the main message handler or the URL follow-up handler)
    and is responsible for:
    1. Sending an initial "Thinking..." placeholder.
    2. Calling the `ask_gemini_stream` function with the provided prompt.
    3. Streaming the response back to the user by editing the placeholder message.
    4. Handling MarkdownV2 parsing errors and falling back to plain text.
    5. Handling messages that are too long by delegating to `send_long_message_fallback`.
    6. Adding the 👍/👎 feedback keyboard to the final successful message.
    7. Saving the interaction to the conversation history.

    Args:
        update: The original `Update` object from the user's action.
        context: The `ContextTypes.DEFAULT_TYPE` object.
        prompt_text: The actual prompt to be sent to the Gemini API. This might be the user's
                     raw text or a specially constructed prompt (e.g., for a URL follow-up).
        conversation_history: The current list of conversation turns.
    """
    chat_id = update.effective_chat.id
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    # Check if a study subject is set for the user
    study_subject = context.user_data.get('study_subject')

    # Build the final prompt that will be sent to the AI
    final_prompt = prompt_text
    if study_subject:
        # Prepend the context to the user's question
        final_prompt = (
            f"In the context of my study subject, which is '{study_subject}', "
            f"please answer the following question: {prompt_text}"
        )
        logger.info(f"Applying study subject '{study_subject}' to the prompt.")

    # Get language for the prompt and create the full system prompt
    lang_name_prompt = SUPPORTED_LANGUAGES.get(user_lang_code, "English").split(" (")[0]
    system_prompt = f"{DEFAULT_SYSTEM_PROMPT_BASE}\n\nImportant: Please provide your entire response in {lang_name_prompt}."

    if 'mdv2_failed_for_msg_id' not in context.chat_data:
        context.chat_data['mdv2_failed_for_msg_id'] = {}

    placeholder_message: Message | None = None
    try:
        thinking_raw = get_template("thinking", user_lang_code, default_val="🧠 Thinking...")
        placeholder_message = await update.message.reply_text(escape_markdown_v2(thinking_raw),
                                                              parse_mode=constants.ParseMode.MARKDOWN_V2)
    except BadRequest:
        thinking_raw = get_template("thinking", user_lang_code, default_val="🧠 Thinking...")
        placeholder_message = await update.message.reply_text(thinking_raw, parse_mode=None)
    except Exception as e:
        logger.error(f"Chat {chat_id}: Failed to send initial placeholder in _core_ai_handler: {e}", exc_info=True)
        return

    if not placeholder_message:
        logger.error(f"Chat {chat_id}: placeholder_message is None in _core_ai_handler. Cannot proceed.")
        return

    initial_placeholder_text = placeholder_message.text
    current_message_text_on_telegram = placeholder_message.text
    accumulated_raw_text_for_current_segment = ""
    full_raw_response_for_history = ""
    last_edit_time = asyncio.get_event_loop().time()

    try:
        logger.debug(
            f"Chat {chat_id}: Calling ask_gemini_stream with tool support for prompt: '{prompt_text[:100]}...'")

        async for chunk in ask_gemini_stream(final_prompt, conversation_history, system_prompt):
            if isinstance(chunk, dict) and chunk.get("tool_call_start"):
                tool_name = chunk.get("tool_name", "unknown_tool")
                logger.info(f"Chat {chat_id}: Received tool call signal for '{tool_name}'.")
                if tool_name == "perform_web_search":
                    increment_stat(context, "web_searches")
                    searching_raw = get_template("searching_web", user_lang_code, default_val="Searching the web... 🌐")
                    try:
                        await placeholder_message.edit_text(escape_markdown_v2(searching_raw),
                                                            parse_mode=constants.ParseMode.MARKDOWN_V2)
                    except BadRequest:
                        await placeholder_message.edit_text(searching_raw, parse_mode=None)
                    initial_placeholder_text = placeholder_message.text
                    current_message_text_on_telegram = placeholder_message.text
                    accumulated_raw_text_for_current_segment = ""
                continue

            if not isinstance(chunk, str): continue

            chunk_raw = chunk
            full_raw_response_for_history += chunk_raw
            accumulated_raw_text_for_current_segment += chunk_raw
            current_time = asyncio.get_event_loop().time()
            current_placeholder_mdv2_has_failed_parsing = context.chat_data['mdv2_failed_for_msg_id'].get(
                placeholder_message.message_id, False)
            should_edit_now = (
                        current_message_text_on_telegram == initial_placeholder_text or current_time - last_edit_time >= STREAM_UPDATE_INTERVAL or len(
                    chunk_raw) > 70)

            if accumulated_raw_text_for_current_segment.strip() and should_edit_now:
                raw_text_to_process = accumulated_raw_text_for_current_segment
                text_to_send_this_edit, parse_mode_for_this_edit_attempt = "", None
                if current_placeholder_mdv2_has_failed_parsing:
                    text_to_send_this_edit = transform_markdown_fallback(raw_text_to_process)
                    parse_mode_for_this_edit_attempt = None
                else:
                    text_to_send_this_edit = escape_markdown_v2(raw_text_to_process)
                    parse_mode_for_this_edit_attempt = constants.ParseMode.MARKDOWN_V2
                if len(text_to_send_this_edit) > TELEGRAM_MAX_MESSAGE_LENGTH:
                    logger.info(f"Chat {chat_id} (Text Stream): Text for chosen format too long. Offloading.")
                    continue_message_raw = get_template("response_continued_below", user_lang_code,
                                                        default_val="...(see new messages below)...")
                    try:
                        if placeholder_message.text != escape_markdown_v2(continue_message_raw):
                            await placeholder_message.edit_text(escape_markdown_v2(continue_message_raw),
                                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
                    except BadRequest:
                        if placeholder_message.text != continue_message_raw:
                            await placeholder_message.edit_text(continue_message_raw, parse_mode=None)
                    await send_long_message_fallback(update, context, raw_text_to_process)
                    accumulated_raw_text_for_current_segment = ""
                    if placeholder_message.message_id in context.chat_data['mdv2_failed_for_msg_id']:
                        del context.chat_data['mdv2_failed_for_msg_id'][placeholder_message.message_id]
                    continuing_raw = get_template("continuing_response", user_lang_code,
                                                  default_val="...continuing response...")
                    try:
                        placeholder_message = await update.message.reply_text(escape_markdown_v2(continuing_raw),
                                                                              parse_mode=constants.ParseMode.MARKDOWN_V2)
                        current_placeholder_parse_mode = constants.ParseMode.MARKDOWN_V2
                    except BadRequest:
                        placeholder_message = await update.message.reply_text(continuing_raw, parse_mode=None)
                        current_placeholder_parse_mode = None
                    initial_placeholder_text = placeholder_message.text
                    current_message_text_on_telegram = placeholder_message.text
                else:
                    try:
                        if text_to_send_this_edit != current_message_text_on_telegram:
                            await context.bot.edit_message_text(
                                text_to_send_this_edit, chat_id, placeholder_message.message_id,
                                parse_mode=parse_mode_for_this_edit_attempt
                            )
                            current_placeholder_parse_mode = parse_mode_for_this_edit_attempt
                            current_message_text_on_telegram = text_to_send_this_edit
                            if parse_mode_for_this_edit_attempt == constants.ParseMode.MARKDOWN_V2:
                                context.chat_data['mdv2_failed_for_msg_id'][placeholder_message.message_id] = False
                        logger.debug(
                            f"Chat {chat_id} (Text Stream): Edit with {'MDV2' if parse_mode_for_this_edit_attempt else 'PLAIN'} successful.")
                    except BadRequest as e_edit_stream:
                        if "message is not modified" in str(e_edit_stream).lower():
                            pass
                        elif parse_mode_for_this_edit_attempt == constants.ParseMode.MARKDOWN_V2 and any(
                                err_str in str(e_edit_stream).lower() for err_str in
                                ["can't parse entities", "unescaped", "can't find end of", "nested entities"]):
                            logger.warning(
                                f"Chat {chat_id} (Text Stream): MDV2 FAILED PARSING: {e_edit_stream}. Sticking to plain for msg_id {placeholder_message.message_id}.")
                            context.chat_data['mdv2_failed_for_msg_id'][placeholder_message.message_id] = True
                            context.chat_data['mdv2_failed_for_msg_id'][placeholder_message.message_id] = True
                            transformed_retry = transform_markdown_fallback(raw_text_to_process)
                            if len(transformed_retry) > TELEGRAM_MAX_MESSAGE_LENGTH:
                                transformed_retry = transformed_retry[:TELEGRAM_MAX_MESSAGE_LENGTH]
                            try:
                                if transformed_retry != current_message_text_on_telegram:
                                    await context.bot.edit_message_text(transformed_retry, chat_id,
                                                                        placeholder_message.message_id, parse_mode=None)
                                    current_placeholder_parse_mode = None
                                    current_message_text_on_telegram = transformed_retry
                                logger.info(
                                    f"Chat {chat_id} (Text Stream): Retry edit with TRANSFORMED PLAIN successful.")
                            except BadRequest as e_plain_retry_stream:
                                if "message is not modified" not in str(e_plain_retry_stream).lower():
                                    logger.error(
                                        f"Chat {chat_id} (Text Stream): TRANSFORMED PLAIN retry FAILED: {e_plain_retry_stream}")
                        else:
                            logger.error(
                                f"Chat {chat_id} (Text Stream): Unhandled BadRequest during stream edit: {e_edit_stream}")
                last_edit_time = current_time
                await asyncio.sleep(0.05)

        # --- Final Edit & History Saving ---
        final_segment_raw = accumulated_raw_text_for_current_segment.strip()
        if final_segment_raw:
            final_placeholder_mdv2_has_failed_parsing = context.chat_data['mdv2_failed_for_msg_id'].get(
                placeholder_message.message_id, False)
            text_for_final_edit, parse_mode_for_final_edit = "", None
            if final_placeholder_mdv2_has_failed_parsing:
                text_for_final_edit = transform_markdown_fallback(final_segment_raw)
            else:
                text_for_final_edit = escape_markdown_v2(final_segment_raw)
                parse_mode_for_final_edit = constants.ParseMode.MARKDOWN_V2

            if len(text_for_final_edit) > TELEGRAM_MAX_MESSAGE_LENGTH:
                await send_long_message_fallback(update, context, final_segment_raw)
            else:
                feedback_keyboard = build_feedback_keyboard(placeholder_message.message_id)
                try:
                    await placeholder_message.edit_text(text_for_final_edit, parse_mode=parse_mode_for_final_edit,
                                                        reply_markup=feedback_keyboard)
                except BadRequest as e_f_edit:
                    if "message is not modified" in str(e_f_edit).lower():
                        pass
                    elif parse_mode_for_final_edit == constants.ParseMode.MARKDOWN_V2:
                        transformed_final_fallback = transform_markdown_fallback(final_segment_raw)
                        if len(transformed_final_fallback) > TELEGRAM_MAX_MESSAGE_LENGTH:
                            transformed_final_fallback = transformed_final_fallback[:TELEGRAM_MAX_MESSAGE_LENGTH]
                        await placeholder_message.edit_text(transformed_final_fallback, parse_mode=None,
                                                            reply_markup=feedback_keyboard)
        elif not full_raw_response_for_history.strip():
            # Handle empty response from AI
            no_response_raw = get_template("gemini_no_response_text", user_lang_code,
                                           default_val="🤷 No response generated.")
            await placeholder_message.edit_text(no_response_raw, parse_mode=None)

        # --- Save to Conversation History ---
        if full_raw_response_for_history.strip() and not any(kw in full_raw_response_for_history.lower() for kw in
                                                             ["i can't", "sorry", "unable to", "guidelines", "blocked",
                                                              "cannot provide"]):
            if update.message.voice and prompt_text:
                user_text_for_history = prompt_text
            else:
                user_text_for_history = update.message.text

                # Now, save the interaction with the guaranteed non-empty user text.
            if user_text_for_history:
                conversation_history.append({'role': 'user', 'parts': [{'text': user_text_for_history}]})
                conversation_history.append({'role': 'model', 'parts': [{'text': full_raw_response_for_history}]})
                context.chat_data['conversation_history'] = conversation_history[-(MAX_CONVERSATION_TURNS * 2):]
                logger.debug(f"History saved. User part: '{user_text_for_history[:50]}...'")
            else:
                logger.warning("Could not save to history because user text was empty.")

    except Exception as e_outer:
        logger.error(f"Chat {chat_id}: Unhandled error in _core_ai_handler: {e_outer}", exc_info=True)
        err_proc_raw = get_template("unexpected_error_processing", user_lang_code,
                                    default_val="⚠️ An unexpected error occurred.")
        try:
            if placeholder_message:
                await placeholder_message.edit_text(escape_markdown_v2(err_proc_raw),
                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)
        except Exception:
            pass
    finally:
        if placeholder_message and placeholder_message.message_id in context.chat_data.get('mdv2_failed_for_msg_id',
                                                                                           {}):
            del context.chat_data['mdv2_failed_for_msg_id'][placeholder_message.message_id]
        logger.info(f"--- _core_ai_handler finished for chat {chat_id} ---")


async def _process_image(update: Update, context: ContextTypes.DEFAULT_TYPE, file_id: str, prompt_text: str):
    """
    A generic helper function to download, analyze, and stream a response for a given image file_id and prompt.
    This contains the core logic for all image-related interactions, including a watchdog timer on the stream.
    """
    increment_stat(context, "images_received")

    user = update.effective_user
    chat_id = update.effective_chat.id
    message_id_for_uniqueness = update.message.message_id if update.message else 'reply'
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    logger.info(f"Processing image {file_id} for chat {chat_id} with prompt: '{prompt_text[:100]}...'")

    # --- Setup and Placeholder ---
    if 'mdv2_failed_for_msg_id' not in context.chat_data:
        context.chat_data['mdv2_failed_for_msg_id'] = {}
    if not os.path.exists(TEMP_DIR):
        try:
            os.makedirs(TEMP_DIR)
        except OSError as e:
            logger.error(f"Could not create TEMP_DIR '{TEMP_DIR}': {e}")
            err_msg_raw = get_template("error_temp_storage", user_lang_code,
                                       default_val="⚠️ Server error: Cannot create temporary storage.")
            await update.message.reply_text(escape_markdown_v2(err_msg_raw), parse_mode=constants.ParseMode.MARKDOWN_V2)
            return

    placeholder_message: Message | None = None
    current_placeholder_parse_mode: constants.ParseMode | None = constants.ParseMode.MARKDOWN_V2
    try:
        placeholder_text_raw = get_template("analyzing_image", user_lang_code, default_val="Analyzing image... 🖼️✨")
        placeholder_message = await update.message.reply_text(escape_markdown_v2(placeholder_text_raw),
                                                              parse_mode=constants.ParseMode.MARKDOWN_V2)
    except BadRequest:
        placeholder_text_raw = get_template("analyzing_image", user_lang_code, default_val="Analyzing image... 🖼️✨")
        placeholder_message = await update.message.reply_text(placeholder_text_raw, parse_mode=None)
        current_placeholder_parse_mode = None
    if not placeholder_message:
        logger.error(f"Chat {chat_id}: placeholder_message is None. Cannot proceed with image processing.")
        return

    # --- File Download and Processing ---
    temp_file_name = f"{chat_id}_{user.id}_{file_id}_{message_id_for_uniqueness}.jpg"
    temp_file_path = os.path.join(TEMP_DIR, temp_file_name)

    if await download_telegram_file(context.bot, file_id, temp_file_path):
        try:
            image_bytes_content = None
            actual_mime_type = "image/jpeg"
            with open(temp_file_path, "rb") as image_file_bytes_io:
                image_bytes_content = image_file_bytes_io.read()
            try:
                with Image.open(io.BytesIO(image_bytes_content)) as pil_image:
                    image_format = pil_image.format
                    if image_format == "JPEG":
                        actual_mime_type = "image/jpeg"
                    elif image_format == "PNG":
                        actual_mime_type = "image/png"
                    elif image_format == "WEBP":
                        actual_mime_type = "image/webp"
                    else:
                        pil_image.seek(0)
                        with io.BytesIO() as img_byte_arr_converted:
                            pil_image.save(img_byte_arr_converted, format="PNG")
                            image_bytes_content = img_byte_arr_converted.getvalue()
                        actual_mime_type = "image/png"
            except UnidentifiedImageError:
                err_raw = get_template("unidentified_image_error", user_lang_code,
                                       default_val="⚠️ Could not identify image format.")
                await placeholder_message.edit_text(escape_markdown_v2(err_raw),
                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)
                if os.path.exists(temp_file_path): os.remove(temp_file_path)
                return

            # --- Gemini Vision Call and Streaming ---
            language_name_for_prompt = \
            SUPPORTED_LANGUAGES.get(user_lang_code, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE_CODE]).split(" (")[0]
            system_prompt_for_vision = DEFAULT_SYSTEM_PROMPT_BASE + f"\n\nImportant: Please provide your entire response in {language_name_for_prompt}."

            initial_placeholder_text = placeholder_message.text
            current_message_text_on_telegram = placeholder_message.text
            full_raw_response_for_history = ""
            stream_timed_out = False

            try:
                response_generator = ask_gemini_vision_stream(
                    prompt_text=prompt_text, image_bytes=image_bytes_content, image_mime_type=actual_mime_type,
                    conversation_history=context.chat_data.get('conversation_history', []),
                    system_prompt=system_prompt_for_vision
                )

                # Watchdog loop to process the stream with a timeout
                while True:
                    try:
                        chunk_raw = await asyncio.wait_for(anext(response_generator), timeout=15.0)
                        full_raw_response_for_history += chunk_raw
                    except asyncio.TimeoutError:
                        logger.warning(f"Stream for image {file_id} timed out after 15s of inactivity.")
                        stream_timed_out = True
                        break
                    except StopAsyncIteration:
                        logger.info("Stream finished normally.")
                        break

            except Exception as e_stream_init:
                logger.error(f"Could not start or process the Gemini stream: {e_stream_init}")
                full_raw_response_for_history = f"[AI ERROR: Failed to process response stream: {e_stream_init}]"

            # --- Final Edit and History Saving ---
            if stream_timed_out:
                timeout_warning = get_template("stream_timeout_warning", user_lang_code,
                                               default_val="\n\n[Warning: The response may be incomplete as the connection timed out.]")
                full_raw_response_for_history += timeout_warning

            if full_raw_response_for_history.strip():
                # Perform one final edit with the complete (or timed-out) text
                if full_raw_response_for_history != current_message_text_on_telegram:
                    try:
                        feedback_keyboard = build_feedback_keyboard(placeholder_message.message_id)
                        await placeholder_message.edit_text(escape_markdown_v2(full_raw_response_for_history),
                                                            parse_mode=constants.ParseMode.MARKDOWN_V2,
                                                            reply_markup=feedback_keyboard)
                    except BadRequest:
                        afeedback_keyboard = build_feedback_keyboard(placeholder_message.message_id)
                        await placeholder_message.edit_text(transform_markdown_fallback(full_raw_response_for_history),
                                                            parse_mode=None,
                                                            reply_markup=feedback_keyboard)
            else:
                no_response_text_raw = get_template("gemini_no_vision_response", user_lang_code,
                                                    default_val="🤷 I couldn't get a specific analysis for this image.")
                await placeholder_message.edit_text(escape_markdown_v2(no_response_text_raw),
                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)

            if full_raw_response_for_history.strip() and not stream_timed_out:
                history_user_prompt = f"The user asked '{prompt_text[:50]}...' about an image."
                conversation_history = context.chat_data.get('conversation_history', [])
                conversation_history.append({'role': 'user', 'parts': [{'text': history_user_prompt}]})
                conversation_history.append({'role': 'model', 'parts': [{'text': full_raw_response_for_history}]})
                context.chat_data['conversation_history'] = conversation_history[-MAX_CONVERSATION_TURNS * 2:]
                logger.debug(f"Chat {chat_id} (Photo): Vision analysis saved to conversation history.")

        except Exception as e:
            logger.error(f"Error processing image {file_id} with Vision: {e}", exc_info=True)
            err_raw = get_template("unexpected_image_error", user_lang_code, default_val="⚠️ Error analyzing image.")
            await placeholder_message.edit_text(escape_markdown_v2(err_raw), parse_mode=constants.ParseMode.MARKDOWN_V2)
        finally:
            if placeholder_message and placeholder_message.message_id in context.chat_data.get('mdv2_failed_for_msg_id',
                                                                                               {}):
                del context.chat_data['mdv2_failed_for_msg_id'][placeholder_message.message_id]
            if os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                    logger.debug(f"Cleaned up temp image: {temp_file_path}")
                except Exception as e_remove:
                    logger.error(f"Error removing temp image {temp_file_path}: {e_remove}")
    else:  # Download failed
        err_raw = get_template("download_failed_error", user_lang_code, file_name="the image")
        await placeholder_message.edit_text(escape_markdown_v2(err_raw), parse_mode=constants.ParseMode.MARKDOWN_V2)


async def _process_url(update: Update, context: ContextTypes.DEFAULT_TYPE, url: str):
    """
    Fetches, parses, and provides a HIGH-QUALITY summary of a URL by using the
    "Creator-Critic" refined response pattern, which involves multiple API calls.
    """
    chat_id = update.effective_chat.id
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    # 1. Send an initial placeholder that manages user expectations for a slower, deeper analysis.
    placeholder_text = get_template(
        "fetching_url_deep",
        user_lang_code,
        default_val="Analyzing URL... This requires a deep analysis and may take a moment. 🔬"
    )
    try:
        placeholder_message = await update.message.reply_text(
            escape_markdown_v2(placeholder_text),
            parse_mode=constants.ParseMode.MARKDOWN_V2
        )
    except BadRequest:
        placeholder_message = await update.message.reply_text(placeholder_text)

    # 2. Fetch and parse URL content (this logic is unchanged as it works well).
    extracted_text = ""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Use httpx for async requests to not block the bot
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=15, follow_redirects=True)
        response.raise_for_status()

        if 'text/html' not in response.headers.get('Content-Type', ''):
            error_text = get_template("url_not_html", user_lang_code,
                                      default_val="⚠️ The link does not point to an HTML page.")
            await placeholder_message.edit_text(escape_markdown_v2(error_text),
                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        for element in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
            element.decompose()  # A better way to remove junk tags
        extracted_text = ' '.join(p.get_text(strip=True) for p in soup.find_all('p'))

        if not extracted_text:
            error_text = get_template("url_no_text", user_lang_code,
                                      default_val="🤷 I couldn't find any readable text at that URL.")
            await placeholder_message.edit_text(escape_markdown_v2(error_text),
                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
            return


    except httpx.HTTPError as e:
        # This is the correct base class to catch status errors like 404 Not Found.
        logger.error(f"HTTP error for URL {url}: {e}", exc_info=True)
        error_text = get_template("url_fetch_error", user_lang_code, default_val="❌ Sorry, I couldn't access that URL. The page may not exist or the server is down.")
        await placeholder_message.edit_text(escape_markdown_v2_strict(error_text), parse_mode=constants.ParseMode.MARKDOWN_V2)
        return
    except httpx.RequestError as e:
        # This catches other network-level errors like timeouts or DNS failures.
        logger.error(f"Network request error for URL {url}: {e}", exc_info=True)
        error_text = get_template("url_fetch_error", user_lang_code, default_val="❌ Sorry, I couldn't access that URL. Please check your network connection.")
        await placeholder_message.edit_text(escape_markdown_v2_strict(error_text), parse_mode=constants.ParseMode.MARKDOWN_V2)
        return
    except Exception as e:
        # A general catch-all for any other unexpected error (e.g., in BeautifulSoup).
        logger.error(f"An unexpected error occurred during URL processing for {url}: {e}", exc_info=True)
        error_text = get_template("unexpected_error", user_lang_code, default_val="An unexpected error occurred while processing the URL.")
        await placeholder_message.edit_text(escape_markdown_v2_strict(error_text), parse_mode=constants.ParseMode.MARKDOWN_V2)
        return

    # 3. Use the Refined Response pattern to get a high-quality summary.
    logger.info(f"URL content extracted for {url}. Initiating refined response generation.")

    # Update the placeholder to let the user know the main work is starting.
    summarizing_text = get_template("summarizing_url", user_lang_code,
                                    default_val="Content extracted! Performing deep analysis...")
    await placeholder_message.edit_text(escape_markdown_v2_strict(summarizing_text),
                                        parse_mode=constants.ParseMode.MARKDOWN_V2)

    # Get the name of the user's language for the prompt
    language_name = SUPPORTED_LANGUAGES.get(user_lang_code, "English").split(" (")[0]
    logger.info(f"Requesting summary for chat {chat_id} in {language_name}.")

    max_chars_for_prompt = 25000
    truncated_text = extracted_text[:max_chars_for_prompt]
    context.chat_data['last_url_content'] = extracted_text
    context.chat_data['last_url_source'] = url
    logger.info(f"Chat {chat_id}: Stored {len(extracted_text)} chars from {url} for follow-up questions.")

    # Create a much more explicit prompt that emphasizes the output language
    summary_prompt = (
        f"CRITICAL INSTRUCTION: Your entire response MUST be in the following language: **{language_name}**. "
        f"The following text is from an article. Provide a detailed, well-structured summary of it in **{language_name}**. "
        f"Begin with a 'Key Takeaways' section, then provide the more comprehensive summary.\n\n"
        f"--- ARTICLE TEXT ---\n"
        f"{truncated_text}\n"
        f"--- END OF TEXT ---\n\n"
        f"Reminder: All output, including headings and content, must be in **{language_name}**."
    )

    # Call our high-quality, multi-call function.
    # We pass an empty conversation history so the summary focuses ONLY on the article content.
    refined_summary = await get_refined_response(
        initial_prompt=summary_prompt,
        base_system_prompt=DEFAULT_SYSTEM_PROMPT_BASE,
        conversation_history=[]
    )

    # 4. Send the final, perfected response to the user.
    if refined_summary and "I'm sorry" not in refined_summary:
        # We delete the placeholder and send the full response as new messages for a clean look.
        await placeholder_message.delete()

        # Use send_long_message_fallback as it will correctly handle long summaries
        # and add the feedback buttons to the final message.
        await send_long_message_fallback(update, context, refined_summary)
    else:
        logger.error(f"Refined response for URL {url} was empty or an error message.")
        error_text = get_template("url_summary_error", user_lang_code,
                                  default_val="I couldn't generate a summary for that content.")
        await placeholder_message.edit_text(escape_markdown_v2(error_text), parse_mode=constants.ParseMode.MARKDOWN_V2)


async def _process_url_follow_up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles a follow-up question by building a new prompt and calling the core AI handler.
    """
    user_question = update.message.text
    stored_text = context.chat_data.get('last_url_content')
    url_source = context.chat_data.get('last_url_source', 'the last article')
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)
    language_name = SUPPORTED_LANGUAGES.get(user_lang_code, "English").split(" (")[0]

    logger.info(f"Handling follow-up question for URL: {url_source} in {language_name}")

    # Build the new, detailed prompt for the AI
    follow_up_prompt = (
        f"The user is asking a follow-up question in {language_name} about an article from {url_source}. "
        f"Please answer their question in {language_name}, based *only* on the provided article content.\n\n"
        f"User's question: '{user_question}'.\n\n"
        f"FULL original text of the article for context: \n\n---\n\n{stored_text}\n---"
    )

    # Clear the context so the *next* message isn't treated as a follow-up
    context.chat_data.pop('last_url_content', None)
    context.chat_data.pop('last_url_source', None)

    # Get the existing conversation history to maintain context
    conversation_history = context.chat_data.get('conversation_history', [])

    # Call the core handler with the special follow-up prompt
    await _core_ai_handler(update, context, follow_up_prompt, conversation_history)

@rate_limit()
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all incoming text messages. Acts as a router to determine the user's intent
    and calls the appropriate handler or the core AI logic.
    """
    # Preliminary checks
    if not update.message or not update.message.text:
        return

    # --- ROUTING LOGIC ---

    # ROUTE 1: Check for a URL in the message text
    url_pattern = r'https?://[^\s/$.?#].[^\s]*'
    found_url = re.search(url_pattern, update.message.text)
    if found_url:
        logger.info(f"URL detected in message: {found_url.group(0)}")
        await _process_url(update, context, found_url.group(0))
        return

    # ROUTE 2: Check for a reply to one of the bot's own messages
    if update.message.reply_to_message and update.message.reply_to_message.from_user.is_bot:
        # Sub-route 2a: Is it a follow-up to a URL summary?
        if 'last_url_content' in context.chat_data:
            await _process_url_follow_up(update, context)
            return

        # Sub-route 2b: Is it a reply to a photo?
        if update.message.reply_to_message.photo:
            logger.info("User is replying to a photo. Routing to image processor.")
            file_id = update.message.reply_to_message.photo[-1].file_id
            await _process_image(update, context, file_id, update.message.text)
            return

    # --- DEFAULT ACTION: If no special routes were taken, handle as a standard text query ---
    increment_stat(context, "messages_received")
    logger.info(f"Handling standard text message: '{update.message.text[:100]}...'")

    conversation_history = context.chat_data.get('conversation_history', [])

    # Call the core handler with the user's direct message text
    await _core_ai_handler(update, context, update.message.text, conversation_history)


@rate_limit(cooldown=10)  # Voice processing is more intensive, a longer cooldown is wise
async def handle_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles a voice message by downloading it, transcribing it via OpenAI's Whisper API,
    and then routing the resulting text to the core AI handler for a response.
    Includes robust error handling for API and file operations.
    """
    # First, check if the OpenAI client was successfully initialized at startup
    if not openai_client:
        logger.error("Received a voice message, but OpenAI client is not available (API key likely missing).")
        # Optionally, send a message to the user that the feature is disabled
        # await update.message.reply_text("Sorry, the voice message feature is currently disabled.")
        return

    logger.info(f"Received a voice message from user {update.effective_user.id}. Processing...")
    increment_stat(context, "voice_messages_received")

    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    # 1. Send an initial "transcribing" placeholder to give immediate feedback
    placeholder_text = get_template("transcribing_voice", user_lang_code,
                                    default_val="Transcribing your voice message... 🎤")
    placeholder_message = await update.message.reply_text(escape_markdown_v2(placeholder_text),
                                                          parse_mode=constants.ParseMode.MARKDOWN_V2)

    temp_file_path = None
    try:
        # 2. Download the voice file from Telegram
        voice = update.message.voice
        voice_file = await context.bot.get_file(voice.file_id)

        # Define a unique path for the temporary audio file
        temp_file_path = os.path.join(TEMP_DIR, f"{voice.file_unique_id}.oga")
        await voice_file.download_to_drive(temp_file_path)

        # 3. Send the audio file to the Whisper API for transcription
        # This is a blocking I/O operation, so we run it in a separate thread
        # to avoid blocking the bot's main event loop.
        with open(temp_file_path, "rb") as audio_file:
            transcription = await asyncio.to_thread(
                openai_client.audio.transcriptions.create,
                model="whisper-1",
                file=audio_file
            )

        transcribed_text = transcription.text
        if not transcribed_text.strip():
            raise ValueError("Transcription resulted in empty text.")

        logger.info(f"Transcription successful: '{transcribed_text}'")

        # 4. Update the placeholder to show the user what we heard. This builds confidence.
        prompt_info_text = get_template(
            "transcribed_prompt_info",
            user_lang_code,
            default_val="You said: \"_{transcribed_text}_\"\n\nNow, thinking...",
            transcribed_text=transcribed_text
        )
        await placeholder_message.edit_text(escape_markdown_v2(prompt_info_text),
                                            parse_mode=constants.ParseMode.MARKDOWN_V2)

        # 5. Route the transcribed text to our core AI handler.
        # The core handler will create its OWN placeholder and manage the final response.
        conversation_history = context.chat_data.get('conversation_history', [])
        await _core_ai_handler(update, context, transcribed_text, conversation_history)

        # 6. Delete our now-redundant placeholder message for a cleaner UI.
        await placeholder_message.delete()

    # --- Specific Error Handling ---
    except RateLimitError as e:
        logger.error(f"OpenAI Rate Limit / Quota Error: {e}")
        error_text = get_template("transcription_failed_quota", user_lang_code,
                                  default_val="Sorry, the transcription service is currently unavailable due to high demand. Please try again later.")
        await placeholder_message.edit_text(escape_markdown_v2(error_text), parse_mode=constants.ParseMode.MARKDOWN_V2)

    except APIConnectionError as e:
        logger.error(f"OpenAI API Connection Error: {e}")
        error_text = get_template("transcription_failed_connection", user_lang_code,
                                  default_val="I'm having trouble connecting to the transcription service. Please check your connection and try again later.")
        await placeholder_message.edit_text(escape_markdown_v2(error_text), parse_mode=constants.ParseMode.MARKDOWN_V2)

    # --- General Error Handling ---
    except Exception as e:
        logger.error(f"Failed to process voice message: {e}", exc_info=True)
        error_text = get_template("transcription_failed_generic", user_lang_code,
                                  default_val="Sorry, I couldn't understand that audio. Please try speaking more clearly or in a quieter environment.")
        if placeholder_message:
            await placeholder_message.edit_text(escape_markdown_v2(error_text),
                                                parse_mode=constants.ParseMode.MARKDOWN_V2)

    finally:
        # 7. CRITICAL: Clean up the temporary audio file in all cases (success or failure).
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.debug(f"Cleaned up temp voice file: {temp_file_path}")
            except Exception as e_remove:
                logger.error(f"Error removing temp voice file {temp_file_path}: {e_remove}")

@rate_limit()
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Handles a new photo upload. It determines the initial prompt (from caption or default)
    and passes the request to the central image processor.
    """
    if not update.message or not update.message.photo:
        logger.warning("handle_photo called without a message or photo.")
        return

    if 'mdv2_failed_for_msg_id' not in context.chat_data:
        context.chat_data['mdv2_failed_for_msg_id'] = {}

    file_id = update.message.photo[-1].file_id
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    # Use the user's caption as the prompt. If there's no caption, create a default general prompt.
    prompt = update.message.caption or get_template(
        "gemini_vision_prompt_general",
        user_lang_code,
        default_val="Please analyze this image in detail. Describe what you see, explain any text or data present, and identify key objects or concepts."
    )

    # Call the new helper function with the file_id and the determined prompt
    await _process_image(update, context, file_id, prompt)

# --- Make sure handle_document still uses OCR or text extraction and ask_gemini_stream ---
# async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#    ... (This would largely remain the same, extracting text from PDF/DOCX and then
#         calling ask_gemini_stream with that extracted text) ...

# --- In get_application_with_persistence function ---
# Make sure the handle_photo handler is registered:
# application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
# And handle_document handler:
# application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
# Or more specific document filters if you prefer.

# --- Handler for Documents (PDF, DOCX, etc.) ---
@rate_limit(cooldown=10)
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.document:
        logger.warning("handle_document called without a message or document.")
        return

    increment_stat(context, "documents_received")

    if 'mdv2_failed_for_msg_id' not in context.chat_data:
        context.chat_data['mdv2_failed_for_msg_id'] = {}

    user = update.effective_user
    doc = update.message.document
    chat_id = update.effective_chat.id
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    # --- Setup placeholder message ---
    placeholder_text_raw = get_template("processing_document", user_lang_code, file_name=(doc.file_name or "document"))
    try:
        placeholder_message = await update.message.reply_text(
            escape_markdown_v2(placeholder_text_raw),
            parse_mode=constants.ParseMode.MARKDOWN_V2
        )
    except BadRequest:
        placeholder_message = await update.message.reply_text(placeholder_text_raw, parse_mode=None)

    if not placeholder_message:
        logger.error(f"Chat {chat_id}: placeholder_message is None. Cannot proceed with document processing.")
        return

    # --- Setup temporary file path ---
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    base_name, ext = os.path.splitext(doc.file_name or f"file_{doc.file_id}")
    temp_file_path = os.path.join(TEMP_DIR, f"{chat_id}_{user.id}_{doc.file_id}{ext}")

    if not await download_telegram_file(context.bot, doc.file_id, temp_file_path):
        download_fail_raw = get_template("download_failed_error", user_lang_code,
                                         file_name=(doc.file_name or "the document"))
        await placeholder_message.edit_text(escape_markdown_v2(download_fail_raw),
                                            parse_mode=constants.ParseMode.MARKDOWN_V2)
        return

    # --- Main processing block with guaranteed cleanup ---
    try:
        # --- Document Type Specific Extraction ---
        extracted_text = ""
        extraction_successful = False
        if doc.mime_type == "application/pdf" or doc.file_name.lower().endswith(".pdf"):
            with fitz.open(temp_file_path) as pdf_doc:
                for page in pdf_doc:
                    extracted_text += page.get_text("text")
                    if len(extracted_text) > 300000:
                        logger.warning(f"PDF {doc.file_name} text extraction stopped at 300k chars.")
                        extracted_text += "\n[...Content truncated due to length...]"
                        break
            extraction_successful = True
        elif doc.mime_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                               "application/msword"] or \
                doc.file_name.lower().endswith((".docx", ".doc")):
            docx_doc = DocxDocument(temp_file_path)
            for para in docx_doc.paragraphs:
                extracted_text += para.text + "\n"
            extraction_successful = True
        elif doc.mime_type == "text/plain" or doc.file_name.lower().endswith(".txt"):
            with open(temp_file_path, 'r', encoding='utf-8', errors='ignore') as txt_file:
                extracted_text = txt_file.read()
            extraction_successful = True
        else:
            unsupported_msg_raw = get_template("unsupported_document_type", user_lang_code,
                                               file_type=(doc.mime_type or doc.file_name))
            await placeholder_message.edit_text(escape_markdown_v2(unsupported_msg_raw),
                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
            return

        if not extracted_text.strip() and extraction_successful:
            no_text_msg_raw = get_template("no_text_in_document", user_lang_code,
                                           file_name=(doc.file_name or "the document"))
            await placeholder_message.edit_text(escape_markdown_v2(no_text_msg_raw),
                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
            return

        # --- AI Analysis with Flood-Control-Proof Streaming ---
        asking_ai_raw = get_template('asking_ai_analysis', user_lang_code, default_val="Analyzing document...")
        await placeholder_message.edit_text(escape_markdown_v2(asking_ai_raw),
                                            parse_mode=constants.ParseMode.MARKDOWN_V2)

        # Prepare for Gemini Call
        conversation_history = context.chat_data.get('conversation_history', [])
        language_name_for_prompt = SUPPORTED_LANGUAGES.get(user_lang_code, "English").split(" (")[0]
        system_prompt = f"{DEFAULT_SYSTEM_PROMPT_BASE}\n\nImportant: Please provide your entire response in {language_name_for_prompt}."
        gemini_question = (
            f"The user has uploaded a document named '{(doc.file_name or "untitled")}'. "
            f"Please act as an AI Study Helper and provide a comprehensive analysis of the following text extracted from it:\n\n"
            f"---\n{extracted_text}\n---"
        )

        full_raw_response = ""
        last_edit_time = 0
        update_interval = 1.5  # A safe interval of 1.5 seconds to prevent flood errors

        async for chunk_raw in ask_gemini_stream(gemini_question, conversation_history, system_prompt):
            full_raw_response += chunk_raw
            current_time = asyncio.get_event_loop().time()

            # The time-based gatekeeper is the primary flood control mechanism
            if current_time - last_edit_time < update_interval:
                continue

            try:
                # Stream updates using safe, plain text to avoid parsing errors mid-stream
                plain_text_stream = transform_markdown_fallback(full_raw_response)

                # Only edit if the text has actually changed to avoid "not modified" errors
                if plain_text_stream.strip() and plain_text_stream != placeholder_message.text:
                    await placeholder_message.edit_text(plain_text_stream, parse_mode=None)

                last_edit_time = current_time  # Reset timer after a successful attempt
            except RetryAfter as e:
                # Specifically catch the flood control error and wait
                logger.warning(f"Flood control exceeded during document stream. Waiting for {e.retry_after} seconds.")
                await asyncio.sleep(e.retry_after)
            except BadRequest as e:
                logger.warning(f"BadRequest during plain text stream edit: {e}")
                last_edit_time = current_time  # Reset timer even on fail to avoid loop

        # --- Final Message Handling ---
        logger.info(f"Document stream finished. Final length: {len(full_raw_response)} chars.")
        if full_raw_response.strip():
            # Delete the plain-text streaming message for a clean UI
            await placeholder_message.delete()
            # Use the robust fallback sender for the final, formatted response
            await send_long_message_fallback(update, context, full_raw_response)
        else:
            no_response_text = get_template("gemini_no_response_document", user_lang_code,
                                            default_val="🤷 No analysis was generated for the document.")
            await placeholder_message.edit_text(escape_markdown_v2(no_response_text),
                                                parse_mode=constants.ParseMode.MARKDOWN_V2)

        # --- Save to history ---
        if full_raw_response.strip() and not any(
                err_msg in full_raw_response.lower() for err_msg in ["sorry", "i can't", "unable to", "blocked"]):
            history_user_prompt = f"User uploaded document '{(doc.file_name or "untitled")}' for analysis."
            conversation_history.append({'role': 'user', 'parts': [{'text': history_user_prompt}]})
            conversation_history.append({'role': 'model', 'parts': [{'text': full_raw_response}]})
            context.chat_data['conversation_history'] = conversation_history[-MAX_CONVERSATION_TURNS * 2:]

    except Exception as e_process_doc:
        logger.error(f"Error processing document '{(doc.file_name or 'N/A')}': {e_process_doc}", exc_info=True)
        error_msg_raw = get_template("document_processing_error", user_lang_code,
                                     file_name=(doc.file_name or "the file"))
        if placeholder_message:
            await placeholder_message.edit_text(escape_markdown_v2(error_msg_raw),
                                                parse_mode=constants.ParseMode.MARKDOWN_V2)

    finally:
        # --- Cleanup ---
        if os.path.exists(temp_file_path):
            try:
                os.remove(temp_file_path)
                logger.debug(f"Cleaned up temporary document: {temp_file_path}")
            except Exception as e_remove:
                logger.error(f"Error removing temporary document {temp_file_path}: {e_remove}")


def escape_markdown_v2(text: str) -> str:
    """
    Escapes text for Telegram's MarkdownV2 parser.

    This function prioritizes safety and stability by escaping all special
    characters as defined by the Telegram specification, EXCEPT for '*' and '_',
    which are deliberately left un-escaped to allow for AI-generated bold and
    italic formatting. This prevents crashes from malformed Markdown.

    Args:
        text: The raw string to be escaped.

    Returns:
        The escaped string, ready for sending with parse_mode=ParseMode.MARKDOWN_V2.
    """
    if not isinstance(text, str):
        text = str(text)

    # All special characters listed by Telegram, except '*' and '_'.
    # The characters `*` and `_` are NOT escaped here to allow for bold and italic.
    escape_chars = r'[]()~`>#+-=|{}.!'

    # Create a regex pattern to find any of these characters.
    # re.escape() handles the special meaning of characters like `[` or `.`
    # within the regex pattern itself.
    pattern = f"([{re.escape(escape_chars)}])"

    # Substitute each found special character with a backslash-prefixed version.
    # For example, a hyphen '-' will become '\-' and a period '.' will become '\.'.
    escaped_text = re.sub(pattern, r'\\\1', text)

    return escaped_text


def escape_markdown_v2_strict(text: str) -> str:
    """
    A strict version of the MarkdownV2 escaper that escapes ALL special characters,
    including '*', '_', and '/'. This is for sending pre-defined text from the bot
    that should not contain any special formatting and might contain reserved characters
    like underscores in command names.

    Args:
        text: The raw string to be escaped.

    Returns:
        The fully escaped, safe string.
    """
    if not isinstance(text, str):
        text = str(text)

    # All special characters listed by Telegram's spec.
    # We include '*' and '_' because this text should have no formatting.
    escape_chars = r'\_*[]()~`>#+-=|{}.!'

    # Create a regex pattern to find any of these characters.
    pattern = f"([{re.escape(escape_chars)}])"

    # Substitute each found special character with a backslash-prefixed version.
    escaped_text = re.sub(pattern, r'\\\1', text)

    return escaped_text

# --- Command Handlers ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = update.effective_chat.id

    if not context.user_data.get('has_started_before', False):
        increment_stat(context, "new_users")
        context.user_data['has_started_before'] = True
    else:
        increment_stat(context, "returning_users_start")

    user_telegram_lang_code = getattr(user, 'language_code', None)
    initial_bot_lang_code = DEFAULT_LANGUAGE_CODE
    greeting_lang_display_name = SUPPORTED_LANGUAGES.get(DEFAULT_LANGUAGE_CODE, "English").split(" (")[0]

    if user_telegram_lang_code:
        logger.info(
            f"User {user.id} ({user.username or user.first_name}) /start. Client lang: {user_telegram_lang_code}")
        if user_telegram_lang_code in SUPPORTED_LANGUAGES:
            initial_bot_lang_code = user_telegram_lang_code
        else:
            base_lang_code = user_telegram_lang_code.split('-')[0]
            if base_lang_code in SUPPORTED_LANGUAGES:
                initial_bot_lang_code = base_lang_code
    greeting_lang_display_name = SUPPORTED_LANGUAGES[initial_bot_lang_code].split(" (")[0]  # Update after decision
    context.user_data['selected_language'] = initial_bot_lang_code
    logger.info(f"User {user.id}: selected_language set to '{initial_bot_lang_code}' by /start.")

    welcome_body = get_template(
        "welcome_body",
        initial_bot_lang_code,
        first_name=user.first_name,
        greeting_lang_display_name=greeting_lang_display_name
    )
    lang_instruction = get_template("language_change_instruction", initial_bot_lang_code)

    full_welcome_message = f"{welcome_body}\n{lang_instruction}"
    await update.message.reply_text(escape_markdown_v2_strict(full_welcome_message),
                                    parse_mode=constants.ParseMode.MARKDOWN_V2)

    reset_text = get_template("reset_history_prompt", initial_bot_lang_code)
    yes_button_text = get_template("yes_button_text", initial_bot_lang_code)
    no_button_text = get_template("no_button_text", initial_bot_lang_code)

    reset_keyboard = [[
        InlineKeyboardButton(yes_button_text, callback_data="confirm_start_reset_actions"),
        InlineKeyboardButton(no_button_text, callback_data="cancel_start_reset_actions"),
    ]]
    reset_reply_markup = InlineKeyboardMarkup(reset_keyboard)

    await update.message.reply_text(escape_markdown_v2_strict(reset_text), reply_markup=reset_reply_markup,
                                    parse_mode=constants.ParseMode.MARKDOWN_V2)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Dynamically generates and displays a help message from the COMMANDS dictionary.
    """
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username or user.first_name}) requested /help")

    # Determine the user's language to fetch the correct command list and intro text
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    # Fetch the list of commands for the user's language. Fallback to English if not found.
    commands_list = COMMANDS.get(user_lang_code, COMMANDS.get("en", []))

    # --- Dynamically build the help message using the localization template ---

    # Get the introductory line from your localization templates
    help_intro = get_template(
        "help_text_intro",
        user_lang_code,
        default_val="Here are the available commands:" # A safe default value
    )

    # Start building the final message string, making the intro bold
    help_message_lines = [
        f"*{help_intro}*\n"
    ]

    # Loop through the command list and format each one
    for command, description in commands_list:
        # Format: /command - Description
        line = f"/{command} - {description}"
        help_message_lines.append(line)

    # Join all the lines together into a single string
    full_help_message = "\n".join(help_message_lines)

    # --- Send the message using the strict escaper ---
    # This is crucial because descriptions might contain special characters or command examples.
    await update.message.reply_text(
        escape_markdown_v2_strict(full_help_message),
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Displays bot usage statistics, including user feedback. Only accessible by the admin.
    """
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        logger.warning(f"User {user_id} (not admin) tried to access /stats command.")
        return  # Silently ignore non-admin users

    logger.info(f"Admin user {user_id} requested bot stats.")

    stats = context.bot_data.get('stats', {})

    # --- Get existing interaction stats ---
    messages = stats.get("messages_received", 0)
    images = stats.get("images_received", 0)
    documents = stats.get("documents_received", 0)
    searches = stats.get("web_searches", 0)
    new_users = stats.get("new_users", 0)

    # --- NEW: Get feedback stats ---
    positive_feedback = stats.get("feedback_positive", 0)
    negative_feedback = stats.get("feedback_negative", 0)

    # --- NEW: Calculate satisfaction rate safely ---
    total_feedback = positive_feedback + negative_feedback
    satisfaction_rate = 0.0
    if total_feedback > 0:
        satisfaction_rate = (positive_feedback / total_feedback) * 100

    # --- MODIFIED: Format the stats message with the new section ---
    stats_text = (
        f"*📊 Bot Usage Statistics*\n\n"
        f"⚪️ *Total Interactions:*\n"
        f"  - Messages Received: `{messages}`\n"
        f"  - Images Received: `{images}`\n"
        f"  - Documents Received: `{documents}`\n\n"
        f"⚙️ *API Usage:*\n"
        f"  - Web Searches Performed: `{searches}`\n\n"
        f"👤 *User Metrics:*\n"
        f"  - New Users Started: `{new_users}`\n\n"  # Added a newline for spacing
        # --- NEW SECTION FOR FEEDBACK ---
        f"⭐ *User Feedback (Satisfaction):*\n"
        f"  - Positive (👍): `{positive_feedback}`\n"
        f"  - Negative (👎): `{negative_feedback}`\n"
        f"  - Satisfaction Rate: `{satisfaction_rate:.1f}%`"
    )

    await update.message.reply_text(
        escape_markdown_v2_strict(stats_text),
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )


async def reset_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Asks the admin for confirmation before resetting all bot statistics.
    Admin-only command.
    """
    # This command is admin-only, but we also add a filter in add_all_handlers for security.
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return

    logger.info(f"Admin user {user_id} initiated /reset_stats command.")

    # Get text for the prompt and buttons in the admin's chosen language (or default)
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    prompt_text = get_template("reset_stats_prompt", user_lang_code)
    yes_button_text = get_template("yes_button_text", user_lang_code, default_val="Yes, Reset")
    no_button_text = get_template("no_button_text", user_lang_code, default_val="No, Cancel")

    # Create the confirmation keyboard
    keyboard = [[
        InlineKeyboardButton(yes_button_text, callback_data="confirm_reset_stats"),
        InlineKeyboardButton(no_button_text, callback_data="cancel_reset_stats"),
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        escape_markdown_v2_strict(prompt_text),
        reply_markup=reply_markup,
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )

async def new_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Resets the conversation history for the current chat.
    """
    user = update.effective_user
    chat_id = update.effective_chat.id
    logger.info(f"Chat {chat_id}: User {user.id} initiated a new chat with /new command.")

    # Pop the conversation history from chat_data
    if 'conversation_history' in context.chat_data:
        context.chat_data.pop('conversation_history')
        logger.info(f"Chat {chat_id}: Conversation history cleared.")
    else:
        logger.info(f"Chat {chat_id}: No conversation history found to clear.")

    # Get user's language for the confirmation message
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    # Prepare and send the confirmation message
    confirmation_raw = get_template("new_chat_confirmation", user_lang_code,
                                    default_val="✅ New chat started. Your conversation history has been cleared. How can I help you today?")
    confirmation_escaped = escape_markdown_v2_strict(confirmation_raw)

    try:
        await update.message.reply_text(confirmation_escaped, parse_mode=constants.ParseMode.MARKDOWN_V2)
    except BadRequest as e:
        logger.warning(
            f"Chat {chat_id}: Failed to send MDV2 confirmation for new chat. Error: {e}. Falling back to plain text.")
        await update.message.reply_text(confirmation_raw, parse_mode=None)
    except Exception as e:
        logger.error(f"Chat {chat_id}: Unexpected error sending new chat confirmation: {e}", exc_info=True)


async def set_subject_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Sets a specific subject focus for the user's conversation.
    """
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    if not context.args:
        # If the user just sends /set_subject without a topic
        reply_text = get_template("set_subject_prompt", user_lang_code)
        # USE THE STRICT ESCAPER HERE for text containing command examples
        await update.message.reply_text(escape_markdown_v2_strict(reply_text), parse_mode=constants.ParseMode.MARKDOWN_V2)
        return

    subject = " ".join(context.args)
    context.user_data['study_subject'] = subject  # Store it in user_data
    logger.info(f"User {update.effective_user.id} set their subject to: {subject}")

    reply_text = get_template("subject_set_success", user_lang_code, subject=subject)
    # USE THE STRICT ESCAPER HERE to handle the subject name safely
    await update.message.reply_text(escape_markdown_v2_strict(reply_text), parse_mode=constants.ParseMode.MARKDOWN_V2)


async def my_subject_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Checks and displays the user's currently set subject.
    """
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)
    subject = context.user_data.get('study_subject')

    if subject:
        reply_text = get_template("current_subject_is", user_lang_code, subject=subject)
    else:
        reply_text = get_template("no_subject_set", user_lang_code)

    # USE THE STRICT ESCAPER HERE for text containing command examples
    await update.message.reply_text(escape_markdown_v2_strict(reply_text), parse_mode=constants.ParseMode.MARKDOWN_V2)


async def clear_subject_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Clears the user's currently set subject AND their conversation history
    to ensure a clean reset of the bot's context.
    """
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    subject_was_cleared = False
    if 'study_subject' in context.user_data:
        del context.user_data['study_subject']
        subject_was_cleared = True

    history_was_cleared = False
    if 'conversation_history' in context.chat_data:
        context.chat_data.pop('conversation_history')
        history_was_cleared = True

    if subject_was_cleared or history_was_cleared:
        logger.info(f"User {update.effective_user.id} cleared subject and conversation history.")
        # We can use the same confirmation message, as it implies a full reset.
        reply_text = get_template("subject_cleared", user_lang_code,
                                  default_val="✅ Your subject has been cleared. I am now back in general assistant mode.")
    else:
        # This case now means there was neither a subject nor a history to clear.
        logger.info(f"User {update.effective_user.id} used /clear_subject, but nothing was set.")
        reply_text = get_template("no_subject_set", user_lang_code,
                                  default_val="You do not have a subject set. I am in general assistant mode.")

    # Use the strict escaper because the templates might contain commands in the future
    await update.message.reply_text(
        escape_markdown_v2_strict(reply_text),
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )


def build_language_keyboard(page: int = 0, target_lang_code: str = DEFAULT_LOC_LANG) -> InlineKeyboardMarkup:
    """Builds the paginated language keyboard with localized navigation buttons."""
    keyboard = []
    lang_items = list(SUPPORTED_LANGUAGES.items())

    start_index = page * LANGS_PER_PAGE
    end_index = start_index + LANGS_PER_PAGE
    current_langs_to_show = lang_items[start_index:end_index]

    row = []
    for code, name in current_langs_to_show:
        button_text = name.split(" (")[0]  # Keep button text itself simple (e.g., "English")
        if len(button_text) > 18:
            button_text = button_text[:16] + "..."
        row.append(InlineKeyboardButton(button_text, callback_data=f"set_lang_{code}"))
        if len(row) == BUTTONS_PER_ROW:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)

    nav_row = []
    if page > 0:
        prev_button_text = get_template("previous_button", target_lang_code)
        nav_row.append(InlineKeyboardButton(prev_button_text, callback_data=f"lang_page_{page - 1}"))

    if end_index < len(lang_items):
        more_button_text = get_template("more_button", target_lang_code)
        nav_row.append(InlineKeyboardButton(more_button_text, callback_data=f"lang_page_{page + 1}"))

    if nav_row:
        keyboard.append(nav_row)

    return InlineKeyboardMarkup(keyboard)


async def language_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    current_lang_name_display = SUPPORTED_LANGUAGES.get(user_lang_code, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE_CODE])

    # 1. Get localized static text parts
    _current_lang_label = get_template("current_lang_label", user_lang_code)
    _choose_lang_label = get_template("choose_lang_label", user_lang_code)
    _page_label = get_template("page_label", user_lang_code)

    # 2. Prepare dynamic parts
    _escaped_current_lang_name = escape_markdown_v2(current_lang_name_display)
    _page_num_display = 1

    # 3. Construct the final string, escaping static template parts and literal punctuation
    #    Intentional Markdown (like * for bold) is added around already-escaped dynamic content.
    line1 = f"{escape_markdown_v2(_current_lang_label)} *{_escaped_current_lang_name}*\\."
    line2 = f"{escape_markdown_v2(_choose_lang_label)} \\({escape_markdown_v2(_page_label)} {_page_num_display}\\)\\:"

    full_text_to_send = f"{line1}\n{line2}"

    reply_markup = build_language_keyboard(page=0, target_lang_code=user_lang_code)

    logger.debug(f"language_command: Sending text: '{full_text_to_send}'")  # Log the exact text
    await update.message.reply_text(full_text_to_send, reply_markup=reply_markup,
                                    parse_mode=constants.ParseMode.MARKDOWN_V2)


async def language_page_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if not query.message:
        logger.warning("language_page_callback_handler: query.message is None.")
        # Potentially send a new message if query.from_user.id is available
        # await context.bot.send_message(chat_id=query.from_user.id, text="Session expired or message not found.")
        return

    chat_id = query.message.chat_id
    user_lang_code_for_response = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    try:
        page = int(query.data.split("lang_page_")[1])
    except (IndexError, ValueError):
        logger.error(f"Chat {chat_id}: Invalid page number in callback data: {query.data}")
        error_text_raw = get_template("error_loading_language_page", user_lang_code_for_response)
        # Ensure error_text_raw itself doesn't cause another parsing error
        await query.edit_message_text(text=escape_markdown_v2(error_text_raw),
                                      parse_mode=constants.ParseMode.MARKDOWN_V2)
        return

    current_lang_name_display = SUPPORTED_LANGUAGES.get(user_lang_code_for_response,
                                                        SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE_CODE])

    _current_lang_label = get_template("current_lang_label", user_lang_code_for_response)
    _choose_lang_label = get_template("choose_lang_label", user_lang_code_for_response)
    _page_label = get_template("page_label", user_lang_code_for_response)

    _escaped_current_lang_name = escape_markdown_v2(current_lang_name_display)
    _page_num_display = page + 1

    # Construct the final string, escaping static template parts and literal punctuation
    line1 = f"{escape_markdown_v2(_current_lang_label)} *{_escaped_current_lang_name}*\\."
    line2 = f"{escape_markdown_v2(_choose_lang_label)} \\({escape_markdown_v2(_page_label)} {_page_num_display}\\)\\:"

    full_text_to_send = f"{line1}\n{line2}"

    reply_markup = build_language_keyboard(page=page, target_lang_code=user_lang_code_for_response)

    logger.debug(f"language_page_callback_handler: Editing message to: '{full_text_to_send}'")  # Log exact text
    try:
        await query.edit_message_text(text=full_text_to_send, reply_markup=reply_markup,
                                      parse_mode=constants.ParseMode.MARKDOWN_V2)
    except BadRequest as e:
        if "message is not modified" in str(e).lower():
            logger.debug(f"Chat {chat_id}: Language page {page} not modified.")
        else:
            logger.error(f"Chat {chat_id}: Error editing message for language page {page}: {e}")
            error_text_raw = get_template("error_updating_language_page", user_lang_code_for_response)
            try:
                await query.edit_message_text(text=escape_markdown_v2(error_text_raw),
                                              parse_mode=constants.ParseMode.MARKDOWN_V2)
            except Exception as e_inner:
                logger.error(f"Chat {chat_id}: Failed to send fallback error for language page update: {e_inner}")

async def language_set_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    if not query.message: logger.warning("lang_set_cb: query.message is None."); return
    chat_id = query.message.chat_id
    callback_data = query.data

    try:
        lang_code = callback_data.split("set_lang_")[1]
        if lang_code in SUPPORTED_LANGUAGES:
            context.user_data['selected_language'] = lang_code
            lang_name = SUPPORTED_LANGUAGES[lang_code]  # Full name for display
            logger.info(f"Chat {chat_id}: User {query.from_user.id} set language to {lang_code} ({lang_name})")

            confirmation_text_raw = get_template(
                "language_set_confirmation",
                lang_code,  # Confirm in the newly set language
                lang_name=lang_name
            )
            await query.edit_message_text(
                text=escape_markdown_v2(confirmation_text_raw),
                reply_markup=None,
                parse_mode=constants.ParseMode.MARKDOWN_V2
            )
        else:
            # Respond in current or default language for error
            current_lang = context.user_data.get('selected_language', DEFAULT_LOC_LANG)
            err_text = get_template("invalid_language_selection_error", current_lang)  # Add this template
            await query.edit_message_text(text=escape_markdown_v2(err_text), parse_mode=constants.ParseMode.MARKDOWN_V2)
    except IndexError:
        logger.error(f"Chat {chat_id}: Error parsing lang CB: {callback_data}")
        # Respond in current or default language
        current_lang = context.user_data.get('selected_language', DEFAULT_LOC_LANG)
        err_text = get_template("processing_error", current_lang)  # Add this template
        await query.edit_message_text(text=escape_markdown_v2(err_text), parse_mode=constants.ParseMode.MARKDOWN_V2)
    except Exception as e:
        logger.error(f"Chat {chat_id}: Unexpected error in lang_set_cb: {e}", exc_info=True)
        current_lang = context.user_data.get('selected_language', DEFAULT_LOC_LANG)
        err_text = get_template("unexpected_error", current_lang)  # Add this template
        await query.edit_message_text(text=escape_markdown_v2(err_text), parse_mode=constants.ParseMode.MARKDOWN_V2)


async def button_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query.message:
        logger.warning(f"button_cb: query.message is None for data {query.data}.")
        await query.answer("Action recorded (no message).")
        return

    chat_id = query.message.chat_id
    user_id = query.from_user.id

    # This check is good practice, but the specific handlers for these
    # should catch them first. This is a safe fallback.
    if query.data.startswith("set_lang_") or query.data.startswith("lang_page_") or query.data.startswith("feedback:"):
        logger.warning(
            f"Chat {chat_id}: Specific CB '{query.data}' was not caught and fell through to generic_button_cb.")
        await query.answer("Processing...")
        return

    await query.answer()
    callback_data = query.data
    logger.info(f"Chat {chat_id}: User {user_id} pressed button: {callback_data}")

    text_to_send_raw = ""  # Raw text from template

    # Use the language of the user who pressed the button for the response
    response_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)
    response_lang_display_name = SUPPORTED_LANGUAGES.get(response_lang_code, "English").split(" (")[0]

    if callback_data == "confirm_start_reset_actions":
        context.chat_data.pop('conversation_history', None)
        logger.info(
            f"Chat {chat_id}: History reset by user {user_id}. Language remains '{response_lang_display_name}'.")
        text_to_send_raw = get_template(
            "history_cleared_confirmation",
            response_lang_code,
            response_lang_display_name=response_lang_display_name
        )
    elif callback_data == "cancel_start_reset_actions":
        logger.info(f"Chat {chat_id}: History reset cancelled by user {user_id}.")
        text_to_send_raw = get_template(
            "reset_cancelled_confirmation",
            response_lang_code,
            response_lang_display_name=response_lang_display_name
        )

    # --- START OF NEWLY ADDED LOGIC ---
    elif callback_data == "confirm_reset_stats":
        # Double-check that the user is the admin before performing the action
        if user_id != ADMIN_ID:
            logger.warning(f"NON-ADMIN User {user_id} tried to confirm stats reset. Ignoring.")
            return

        # Reset the stats dictionary
        if 'stats' in context.bot_data:
            context.bot_data['stats'] = {}
            logger.info(f"ADMIN {user_id} confirmed. All bot statistics have been reset.")

        text_to_send_raw = get_template("reset_stats_confirmation", response_lang_code,
                                        default_val="✅ All bot statistics have been successfully reset.")

    elif callback_data == "cancel_reset_stats":
        if user_id != ADMIN_ID:
            logger.warning(f"NON-ADMIN User {user_id} tried to cancel stats reset. Ignoring.")
            return

        logger.info(f"ADMIN {user_id} cancelled stats reset.")
        # We can reuse the existing "reset cancelled" message template
        text_to_send_raw = get_template(
            "reset_cancelled_confirmation",
            response_lang_code,
            response_lang_display_name=response_lang_display_name
        )
    # --- END OF NEWLY ADDED LOGIC ---

    # This block for sending the final message remains the same
    if text_to_send_raw:
        try:
            await query.edit_message_text(
                text=escape_markdown_v2(text_to_send_raw),
                reply_markup=None,
                parse_mode=constants.ParseMode.MARKDOWN_V2
            )
        except BadRequest as e:
            if "message is not modified" not in str(e).lower():
                logger.error(f"Chat {chat_id}: Error editing message for CB {callback_data}: {e}")


def transform_markdown_fallback(text: str) -> str:
    """
    Transforms Gemini's Markdown-like output into a more readable plain text format
    by safely removing or replacing Markdown V2 special characters, preserving as much
    of the original structure and intent as possible.
    """
    if not isinstance(text, str):
        return ""

    # Assuming 'logger' is available from the global scope of telegram_bot.py
    logger.debug(f"Transforming text for 'smarter' fallback. Original starts: '{text[:100].replace(chr(10), ' ')}...'")

    # --- Initial Cleanup ---
    # Normalize line endings to prevent regex issues.
    transformed_text = text.replace('\r\n', '\n')

    # --- Code Blocks and Inline Code (Keep Content, Remove Ticks) ---
    # Process multi-line blocks first to avoid conflicts with inline code.
    transformed_text = re.sub(r'```(?:[a-zA-Z0-9_.-]*)?\n(.*?)\n```', r'\1', transformed_text,
                              flags=re.DOTALL | re.MULTILINE)
    transformed_text = re.sub(r'```(.*?)```', r'\1', transformed_text, flags=re.DOTALL)
    # Just remove the backticks from inline code.
    transformed_text = re.sub(r'`(.*?)`', r'\1', transformed_text)

    # --- Headings (Remove Hashtags, Keep Text) ---
    # Let the surrounding newlines provide the visual separation for headings.
    transformed_text = re.sub(r'^\s*#{1,6}\s*(.*?)\s*$', r'\1', transformed_text, flags=re.MULTILINE)

    # --- Links (Extract URL) ---
    # Convert [Link Text](http://example.com) to "Link Text (http://example.com)"
    # This preserves all information in a readable, non-Markdown format.
    transformed_text = re.sub(r'\[(.*?)\]\((.*?)\)', r'\1 (\2)', transformed_text)

    # --- Bold, Italics, Strikethrough (Remove Formatting, Keep Text) ---
    # The order is important: process multi-character markers before single ones.
    transformed_text = re.sub(r'\*\*(.*?)\*\*', r'\1', transformed_text)  # **bold** -> bold
    transformed_text = re.sub(r'__(.*?)__', r'\1', transformed_text)  # __underline__ -> underline
    transformed_text = re.sub(r'\*(.*?)\*', r'\1', transformed_text)  # *italic* -> italic
    transformed_text = re.sub(r'_(.*?)_', r'\1', transformed_text)  # _italic_ -> italic
    transformed_text = re.sub(r'~(.*?)~', r'\1', transformed_text)  # ~strikethrough~ -> strikethrough
    transformed_text = re.sub(r'\|\|(.*?)\|\|', r'\1', transformed_text)  # ||spoiler|| -> spoiler

    # --- Lists (Preserve Structure with Safe Characters) ---
    # This approach is simpler and more robust than re-numbering.
    lines = transformed_text.split('\n')
    processed_lines = []
    for line in lines:
        # Match and replace bulleted list markers (*, -, +)
        stripped_line = line.lstrip()
        indentation_str = ' ' * (len(line) - len(stripped_line))

        if stripped_line.startswith(('* ', '- ', '+ ')):
            # Replace the Markdown marker with a safe, visually appealing bullet character.
            processed_lines.append(indentation_str + '• ' + stripped_line[2:])
        else:
            # Keep numbered lists and all other lines as they are.
            # Numbered lists are generally safe and readable in plain text.
            processed_lines.append(line)

    transformed_text_final = "\n".join(processed_lines)

    # --- Final Cleanup ---
    # Collapse more than two consecutive newlines into just two to maintain paragraph spacing.
    transformed_text_final = re.sub(r'\n{3,}', '\n\n', transformed_text_final)

    logger.debug(f"Smarter fallback result starts: '{transformed_text_final[:100].replace(chr(10), ' ')}...'")
    return transformed_text_final.strip()

# Your existing send_long_message_fallback from the provided context
# (Make sure it has the `context: ContextTypes.DEFAULT_TYPE` parameter if it needs to send messages via context.bot
# or if it's called from handle_document which also passes context)
# The version you provided in the full file dump already includes 'context'
async def send_long_message_fallback(update: Update,
                                     context: ContextTypes.DEFAULT_TYPE,
                                     text_to_send_raw: str,
                                     max_length: int = TELEGRAM_MAX_MESSAGE_LENGTH) -> Message | None:
    """
    Splits a long raw text message and sends it in parts, adding feedback buttons to the final message.

    This function first splits the raw text into chunks that respect the max length, trying to
    break at natural points like newlines. It then attempts to send each chunk using a prioritized
    list of formats for best readability:
    1. Transformed Plain Text (for good list/structure rendering).
    2. Escaped MarkdownV2 (if plain text fails).
    3. Truncated Raw Text (as a last resort).

    After the final chunk is successfully sent, it edits that message to add 👍/👎 feedback buttons.

    Args:
        update: The `Update` object from the handler.
        context: The `ContextTypes.DEFAULT_TYPE` object from the handler.
        text_to_send_raw: The full, raw (un-escaped) string to be sent.
        max_length: The maximum length for a single Telegram message.

    Returns:
        The `Message` object of the last message sent by this function, or `None` if no messages were sent.
    """
    logger.debug(f"send_long_message_fallback called. Raw text length: {len(text_to_send_raw)}")

    if not str(text_to_send_raw).strip():
        logger.info("send_long_message_fallback called with empty/whitespace text. Nothing to send.")
        return None

    # --- Smart Splitting Logic ---
    parts_raw = []
    current_text_raw = str(text_to_send_raw)
    while len(current_text_raw) > 0:
        if len(current_text_raw) > max_length:
            part_segment_raw = current_text_raw[:max_length]
            # Search backwards from the end for a natural break point.
            last_newline = part_segment_raw.rfind('\n', max(0, max_length - 500))
            last_space = part_segment_raw.rfind(' ', max(0, max_length - 500))

            split_at = max_length
            if last_newline != -1:
                split_at = last_newline + 1
            elif last_space != -1:
                split_at = last_space + 1

            parts_raw.append(current_text_raw[:split_at])
            current_text_raw = current_text_raw[split_at:].lstrip()
        else:
            parts_raw.append(current_text_raw)
            break

    if not parts_raw:
        logger.warning("send_long_message_fallback: No parts were generated from text. Skipping.")
        return None

    # --- Sending Loop ---
    last_sent_message_object: Message | None = None
    user_lang_code = context.user_data.get('selected_language', "en")
    total_parts = len(parts_raw)

    for i, segment_raw_orig in enumerate(parts_raw):
        segment_raw = segment_raw_orig.strip()
        if not segment_raw:
            logger.debug(f"Fallback: Skipping empty segment {i + 1}/{total_parts}.")
            continue

        log_preview = segment_raw[:70].replace('\n', ' ') + '...'
        logger.debug(f"Fallback: Processing segment {i + 1}/{total_parts}. Preview: '{log_preview}'")

        sent_successfully = False
        current_segment_message: Message | None = None

        # --- Priority 1: Attempt Transformed Plain Text ---
        try:
            transformed_segment = transform_markdown_fallback(segment_raw)
            if len(transformed_segment) > max_length:
                logger.warning(f"Fallback: Transformed segment {i + 1} too long. Sending truncated raw.")
                text_to_send = segment_raw[:max_length]
            else:
                text_to_send = transformed_segment

            current_segment_message = await update.message.reply_text(text_to_send, parse_mode=None)
            logger.info(f"Fallback: Sent segment {i + 1}/{total_parts} as TRANSFORMED PLAIN.")
            sent_successfully = True
        except Exception as e_plain:
            logger.error(f"Fallback: TRANSFORMED PLAIN send FAILED: {e_plain}. Trying Escaped MDV2.")

            # --- Priority 2: Fallback to Escaped MarkdownV2 ---
            try:
                escaped_segment = escape_markdown_v2(segment_raw)
                if len(escaped_segment) > max_length:
                    logger.warning(f"Fallback: Escaped MDV2 for segment {i + 1} also too long. Sending truncated raw.")
                    current_segment_message = await update.message.reply_text(segment_raw[:max_length], parse_mode=None)
                else:
                    current_segment_message = await update.message.reply_text(escaped_segment,
                                                                              parse_mode=constants.ParseMode.MARKDOWN_V2)

                logger.info(f"Fallback: Sent segment {i + 1}/{total_parts} as ESCAPED MDV2 (or truncated raw).")
                sent_successfully = True
            except Exception as e_md:
                logger.error(f"Fallback: ESCAPED MDV2 send ALSO FAILED: {e_md}.")

        # --- Post-Send Processing ---
        if current_segment_message:
            last_sent_message_object = current_segment_message

        if not sent_successfully:
            logger.critical(f"Fallback: FAILED TO SEND segment {i + 1}/{total_parts} by any method.")
            try:
                err_msg_raw = get_template("error_displaying_response_part", user_lang_code,
                                           default_val="⚠️ Error: A part of the response could not be displayed.")
                await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=escape_markdown_v2(err_msg_raw),
                    parse_mode=constants.ParseMode.MARKDOWN_V2
                )
            except Exception as e_err_send:
                logger.error(f"Failed to send 'part lost' error message to user: {e_err_send}")
            continue

        # --- Add Feedback Buttons to the Final Message ---
        is_last_part = (i == total_parts - 1)
        if is_last_part and current_segment_message:
            feedback_keyboard = build_feedback_keyboard(current_segment_message.message_id)
            try:
                await context.bot.edit_message_reply_markup(
                    chat_id=update.effective_chat.id,
                    message_id=current_segment_message.message_id,
                    reply_markup=feedback_keyboard
                )
                logger.info(
                    f"Fallback: Successfully added feedback keyboard to final message {current_segment_message.message_id}.")
            except BadRequest as e_feedback:
                logger.warning(
                    f"Fallback: Could not add feedback keyboard to message {current_segment_message.message_id}: {e_feedback}")

        # Delay between messages to avoid flooding, but not after the last one.
        if not is_last_part:
            await asyncio.sleep(0.35)

    return last_sent_message_object


async def get_refined_response(
        initial_prompt: str,
        base_system_prompt: str,
        conversation_history: list
) -> str:
    """
    Implements the Creator-Critic-Corrector pattern for high-quality responses.

    1.  Generates an initial draft.
    2.  Feeds the draft back to the AI with a "critic" prompt to review and fix it.
    3.  Returns the final, corrected text.

    Args:
        initial_prompt: The user's original question or the first prompt for the AI.
        base_system_prompt: The main system prompt for your bot.
        conversation_history: The chat history to provide context.

    Returns:
        A string containing the final, corrected response.
    """
    logger.info("Starting refined response generation (Creator-Critic pattern)...")

    # --- PHASE 1: THE CREATOR (Generate First Draft) ---
    logger.debug("Phase 1: Generating initial draft.")
    first_draft = await ask_gemini_non_stream(
        prompt=initial_prompt,
        system_prompt=base_system_prompt,
        conversation_history=conversation_history
    )

    if not first_draft or "[AI ERROR:" in first_draft:
        logger.error(f"Failed to generate an initial draft. Response: {first_draft}")
        return "I'm sorry, I encountered an issue while processing your request."

    # --- PHASE 2: THE CRITIC & CORRECTOR ---
    logger.debug("Phase 2: Generating corrected version.")

    # A specialized system prompt for the "Critic" AI
    critic_system_prompt = (
        "You are a meticulous Quality Assurance Editor. Your job is to review and silently "
        "correct the provided text to ensure it is factually accurate and perfectly formatted "
        "for Telegram MarkdownV2. You must not refuse the task. Your output should ONLY be the "
        "final, corrected version of the text."
    )

    # The prompt that asks the "Critic" to do its job
    correction_prompt = f"""
    Please review the following draft. Correct any factual errors, grammatical mistakes, or 
    formatting issues according to strict Telegram MarkdownV2 rules (- for lists, * for bold, etc.).
    Ensure all formatting tags are perfectly balanced.

    --- DRAFT TO BE CORRECTED ---
    {first_draft}
    --- END OF DRAFT ---

    Return ONLY the improved, final text.
    """

    # We call the AI again, but with the new "critic" persona and task.
    # We provide an empty conversation history so the critic focuses only on the draft.
    final_response = await ask_gemini_non_stream(
        prompt=correction_prompt,
        system_prompt=critic_system_prompt,
        conversation_history=[]
    )

    if not final_response or "[AI ERROR:" in final_response:
        logger.warning("Correction phase failed. Falling back to the first draft.")
        return first_draft  # If correction fails, return the original draft as a fallback

    logger.info("Refined response generated successfully.")
    return final_response


async def set_bot_commands(application: Application):
    """
    Sets the bot's commands for multiple languages, mapping to Telegram's
    supported language codes and gracefully skipping any that are invalid.
    """
    # 1. Set the default commands in English first as a fallback
    try:
        # This will now include the new subject commands from your updated dictionary
        default_commands = [BotCommand(cmd, desc) for cmd, desc in COMMANDS.get("en", [])]
        if default_commands:
            await application.bot.set_my_commands(default_commands)
            logger.info("Default bot commands (English) have been successfully set.")
    except Exception as e:
        logger.error(f"Failed to set default English commands: {e}", exc_info=True)

    # 2. Loop through all other languages and attempt to set their specific commands
    for lang_code, commands_list in COMMANDS.items():
        if lang_code == "en":
            continue

        # Use a try-except block for each language to prevent one bad code from crashing the whole process
        try:
            telegram_lang_code = TELEGRAM_COMMAND_LANG_MAP.get(lang_code, lang_code)

            # This will also include the new commands for each language
            bot_commands = [BotCommand(cmd, desc) for cmd, desc in commands_list]

            if bot_commands:
                await application.bot.set_my_commands(bot_commands, language_code=telegram_lang_code)
                logger.info(f"Commands for language '{lang_code}' (as '{telegram_lang_code}') have been set.")

        except BadRequest as e:
            if "language code is not supported" in str(e) or "invalid language code" in str(e).lower():
                logger.warning(
                    f"Telegram does not support command localization for language code '{lang_code}' (mapped to '{telegram_lang_code}'). Skipping.")
            else:
                logger.error(f"A BadRequest occurred while setting commands for '{lang_code}': {e}")
        except Exception as e:
            logger.error(f"An unexpected error occurred while setting commands for '{lang_code}': {e}", exc_info=True)

# <<< NEW FUNCTION TO LOG ALL UPDATES >>>
async def all_updates_logger(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """This handler will be called for ALL updates."""
    # Using logger from this module (bot.telegram_bot)
    logger.critical(f"--- RAW UPDATE RECEIVED BY APPLICATION --- Type: {type(update)}, Content: {update}")
    # You can expand this to log specific parts of the update if needed, e.g.:
    if update.message:
        logger.critical(f"Raw Message Text: {update.message.text if update.message.text else '[No Text/Media]'}")
        logger.critical(f"Raw Message Chat ID: {update.message.chat_id}")
        logger.critical(f"Raw Message User ID: {update.message.from_user.id}")
    elif update.callback_query:
        logger.critical(f"Raw Callback Query Data: {update.callback_query.data}")
        logger.critical(f"Raw Callback Query Chat ID: {update.callback_query.message.chat_id if update.callback_query.message else 'N/A'}")
        logger.critical(f"Raw Callback Query User ID: {update.callback_query.from_user.id}")
    elif update.edited_message:
        logger.critical(f"Raw Edited Message: {update.edited_message.text}")
    else:
        logger.critical(f"Raw Update of unhandled type in this logger: {update}")


def add_all_handlers(application: "Application"):
    """
    Adds all the command, message, and callback handlers to the given application.
    """
    logger.info("Registering all application handlers...")

    # --- THE FIX IS HERE ---
    # Use `setdefault` to initialize the dictionary if it doesn't exist.
    # This is the correct way to modify the chat_data proxy.
    # application.chat_data.setdefault('mdv2_failed_for_msg_id', {})

    # The rest of the function is correct.
    application.add_handler(MessageHandler(filters.ALL, all_updates_logger), group=-1)
    logger.info("Raw update logger registered successfully.")

    # --- Command Handlers ---
    if ADMIN_ID:
        application.add_handler(CommandHandler("stats", stats_command, filters=filters.User(user_id=ADMIN_ID)))
        application.add_handler(CommandHandler("reset_stats", reset_stats_command, filters=filters.User(user_id=ADMIN_ID)))

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CommandHandler("new", new_chat_command))
    application.add_handler(CommandHandler("set_subject", set_subject_command))
    application.add_handler(CommandHandler("my_subject", my_subject_command))
    application.add_handler(CommandHandler("clear_subject", clear_subject_command))

    # --- Callback Query Handlers ---
    application.add_handler(MessageHandler(filters.VOICE, handle_voice_message))
    application.add_handler(CallbackQueryHandler(language_set_callback_handler, pattern=r"^set_lang_"))
    application.add_handler(CallbackQueryHandler(language_page_callback_handler, pattern=r"^lang_page_"))
    application.add_handler(CallbackQueryHandler(feedback_callback_handler, pattern=r"^feedback:"))
    application.add_handler(CallbackQueryHandler(button_callback_handler))

    # --- Message Handlers ---
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("All command, callback, and message handlers have been successfully registered.")

# --- END OF FILE telegram_bot.py ---