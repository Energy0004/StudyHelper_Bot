# --- START OF FILE telegram_bot.py ---

import re
import time
from collections import OrderedDict
import os
import logging
import asyncio
from functools import wraps

import requests
from bs4 import BeautifulSoup

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
from telegram.error import BadRequest

from localization import get_template, DEFAULT_LOC_LANG
# from telegram.request import HTTPXRequest # Temporarily commented out for diagnostics

# Assuming gemini_utils.py is in the same directory or a correctly configured package
from .gemini_utils import ask_gemini_stream, ask_gemini_vision_stream

logger = logging.getLogger(__name__)  # This will be 'bot.telegram_bot'

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

    *   **Use Headings:** Introduce different sections of a long answer with bolded headings (e.g., `*Key Concepts*`, `*Step-by-Step Solution*`). This helps the user navigate your response.
    *   **Use Lists:** For sequences of steps, examples, or multiple points, ALWAYS use bulleted (`* ` or `- `) or numbered (`1. `) lists. This is much easier to read than a long paragraph.
    *   **Emphasize Keywords:** Highlight the most important terms, definitions, or conclusions using `*bold*` or `_italics_` to draw the user's attention to key information.
    *   **Use Whitespace:** Generously use empty lines to separate paragraphs, headings, and distinct ideas. This gives the text "breathing room" and prevents it from looking cramped.
    *   **Keep Paragraphs Short:** Aim for short, focused paragraphs, each covering a single idea.
    *   **Start with a Summary:** For complex topics, begin with a one or two-sentence summary (the "bottom line") before diving into the details.
    *   **DO NOT Use Plain Text Tables:** Avoid creating tables using plain text characters like `|` and `-`. This formatting breaks easily in chat applications and looks unprofessional. If a table is truly necessary, use proper Markdown table syntax.

    **--- END OF RESPONSE STRUCTURE INSTRUCTIONS ---**


    **Strict MarkdownV2 Formatting Rules (MANDATORY FOR CORRECT DISPLAY!):**
    Your response will be parsed by Telegram's MarkdownV2 engine. Failure to adhere to these rules WILL result in incorrect display or parsing errors.

    *   **Headings:** Use bold text for headings. Example: `*Main Topic*` or `*Sub-Topic*`. Do NOT use `#` for headings.
    *   **Bold:** Use asterisks: `*bold text*`.
    *   **Italics:** Use ONE underscore on each side of the text (`_italic text_`) or ONE asterisk on each side (`*italic text*`).
        *   **CRITICAL: ALL ITALIC TAGS MUST BE CORRECTLY OPENED AND CLOSED. NO UNTERMINATED ITALICS.** For example, `_this is correct_`, but `_this is incorrect` (missing closing underscore) WILL FAIL.
        *   Ensure there are no stray `_` or `*` characters that could be misinterpreted as unclosed italics, especially at the end of lines or paragraphs. Avoid using underscores or asterisks for emphasis if they are not part of a valid, closed pair, unless they are escaped.
    *   **Strikethrough:** Use tildes: `~strikethrough text~`.
    *   **Underline:** Use double underscores: `__underline text__`. (Note: Telegram clients may render this as italics if underline is not supported, or it might be a custom interpretation by the library).
    *   **Spoiler:** Use double vertical bars: `||spoiler text||`.
    *   **Inline Code:** Use single backticks: `` `inline code` ``.
        *   **CRITICAL (for inline code):** Content within inline code (`...`) must NOT contain any other MarkdownV2 special characters (`_`, `*`, `[`, `]`, `(`, `)`, `~`, `` ` ``, `>`, `#`, `+`, `-`, `=`, `|`, `{`, `}`, `.`, `!`) unless they are *also* escaped with a preceding `\`. For example, to show `_variable_` literally inside inline code, it should be ``` ``\\_variable\\_`` ```.
    *   **Code Blocks (Preformatted Text):** Use triple backticks for multi-line code blocks. You can specify a language.
        Example:
        ```python
        def hello():
            print("Hello, World!")
        ```
        *   **CRITICAL (for code blocks):** Content within code blocks (```...```) is generally treated as literal and does not need escaping of Markdown characters. However, the triple backticks themselves must not be escaped.

    *   **Bullet Lists:**
        *   Must start with `* ` (asterisk followed by ONE space) OR `- ` (hyphen followed by ONE space) OR `+ ` (plus followed by ONE space).
        *   **CRITICAL: A single space character MUST follow the `*`, `-`, or `+` bullet marker.**
        *   Correct Example: `* List item text`
        *   Correct Example: `- Another list item`
        *   INCORRECT (will fail): `*List item text` (no space)
        *   INCORRECT (will fail): `-Another list item` (no space)
        *   Nested lists are possible by indenting with spaces (e.g., four spaces). `    * Nested item`

    *   **Numbered Lists:**
        *   Must start with `1. ` (number, then a period, then ONE space).
        *   **CRITICAL: A single space character MUST follow the period (`.`) after the number.**
        *   The actual numbers you use (1, 2, 3 or 1, 1, 1) usually don't matter as much as the format `number. space text`; Telegram often re-numbers them. But for clarity, use sequential numbers.
        *   Correct Example: `1. First item text`
        *   Correct Example: `2. Second item text`
        *   INCORRECT (will fail): `1.First item text` (no space)
        *   INCORRECT (will fail): `2.Second item text` (no space)

    *   **Links:**
        *   Inline links: `[Link Text](http://example.com)`
        *   The URL part `(http://example.com)` should generally not contain Markdown special characters unless they are percent-encoded. Parentheses `()` within the URL itself must be percent-encoded (`%28` and `%29`).

    *   **Escaping Special Characters:**
        *   If you need to use any of the special MarkdownV2 characters `_`, `*`, `[`, `]`, `(`, `)`, `~`, `` ` ``, `>`, `#`, `+`, `-`, `|`, `{`, `}`, `.`, `!` literally (not for formatting), you MUST escape them with a preceding backslash `\`.
        *   Example: `This is a literal asterisk: \* and this is a literal period: \. not a list item\.`
        *   Example: `1\. This is not a list item, but a sentence starting with 1 followed by an escaped period.`
        *   A literal backslash `\` must also be escaped: `\\`.

    *   **Well-Formed Markdown:** All formatting pairs (`*...*`, `_..._`, `` `...` ``, `~...~`, `__...__`, `||...||`) must be correctly opened and closed. No unclosed entities.

    Please pay EXTREME attention to these formatting rules, especially the correct opening AND CLOSING of all formatting entities like italics, bold, code, etc., the spacing in lists, and the correct escaping of literal special characters. AVOID UNTERMINATED MARKDOWN ENTITIES. Your output's readability depends entirely on this.
    If uncertain about a complex formatting, prefer simpler, well-formed Markdown or plain text for that segment.

    **--- ADD THIS NEW LINE HERE ---**
    **Final Check:** Before finalizing your response, double-check that every `*`, `_`, `~`, `__`, and `` ` `` character is part of a correctly opened and closed pair, or is properly escaped with a `\` if it is meant to be a literal character.
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
    Fetches, parses, and summarizes a URL using the robust "Plain Text Stream, Final Markdown" strategy.
    """
    chat_id = update.effective_chat.id
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    # 1. Send initial placeholder
    placeholder_text = get_template("fetching_url", user_lang_code, default_val="Fetching content from URL... 🌐")
    try:
        placeholder_message = await update.message.reply_text(escape_markdown_v2(placeholder_text),
                                                              parse_mode=constants.ParseMode.MARKDOWN_V2)
    except BadRequest:
        placeholder_message = await update.message.reply_text(placeholder_text)

    # 2. Fetch and parse URL content (This part is correct and remains unchanged)
    extracted_text = ""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        if 'text/html' not in response.headers.get('Content-Type', ''):
            error_text = get_template("url_not_html", user_lang_code,
                                      default_val="⚠️ The link does not point to an HTML page.")
            await placeholder_message.edit_text(escape_markdown_v2(error_text),
                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
            return
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        extracted_text = ' '.join(p.get_text(strip=True) for p in paragraphs)
        if not extracted_text:
            error_text = get_template("url_no_text", user_lang_code,
                                      default_val="🤷 I couldn't find any readable text at that URL.")
            await placeholder_message.edit_text(escape_markdown_v2(error_text),
                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
            return
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch URL {url}: {e}", exc_info=True)
        error_text = get_template("url_fetch_error", user_lang_code, default_val="❌ Sorry, I couldn't access that URL.")
        await placeholder_message.edit_text(escape_markdown_v2(error_text), parse_mode=constants.ParseMode.MARKDOWN_V2)
        return

    # 3. Prepare for Gemini summary
    summarizing_text = get_template("summarizing_url", user_lang_code, default_val="Content extracted! Summarizing...")
    await placeholder_message.edit_text(escape_markdown_v2(summarizing_text),
                                        parse_mode=constants.ParseMode.MARKDOWN_V2)

    max_chars_for_prompt = 20000
    truncated_text = extracted_text[:max_chars_for_prompt]
    context.chat_data['last_url_content'] = extracted_text
    context.chat_data['last_url_source'] = url
    logger.info(f"Chat {chat_id}: Stored {len(extracted_text)} chars from {url} for follow-up questions.")

    language_name_for_prompt = SUPPORTED_LANGUAGES.get(user_lang_code, "English").split(" (")[0]
    system_prompt_for_url = (
        f"{DEFAULT_SYSTEM_PROMPT_BASE}\n\nCRITICAL: Please provide your entire response in {language_name_for_prompt}.")
    summary_prompt = (
        f"Please provide a concise summary of the following article... Here is the text:\n\n---\n\n{truncated_text}\n---")

    # 4. Robust Streaming and Final Edit Logic
    try:
        current_message_text_on_telegram = placeholder_message.text
        accumulated_raw_text = ""
        last_edit_time = asyncio.get_event_loop().time()

        # --- STREAMING LOOP (PLAIN TEXT ONLY) ---
        async for chunk_raw in ask_gemini_stream(summary_prompt, [], system_prompt_for_url):
            accumulated_raw_text += chunk_raw
            current_time = asyncio.get_event_loop().time()

            if current_time - last_edit_time >= STREAM_UPDATE_INTERVAL:
                # Use transform_markdown_fallback to create a clean, plain text stream
                plain_text_stream = transform_markdown_fallback(accumulated_raw_text)
                if plain_text_stream.strip() and plain_text_stream != current_message_text_on_telegram:
                    try:
                        await placeholder_message.edit_text(plain_text_stream, parse_mode=None)
                        current_message_text_on_telegram = plain_text_stream
                    except BadRequest as e:
                        if "message is not modified" not in str(e).lower():
                            logger.warning(f"URL Summary Stream (Plain): Edit failed. Error: {e}")
                last_edit_time = current_time

        # --- FINAL EDIT (ATTEMPT MARKDOWN) ---
        if accumulated_raw_text.strip():
            final_raw_text = accumulated_raw_text
            feedback_keyboard = build_feedback_keyboard(placeholder_message.message_id)

            # First, try to send with beautiful MarkdownV2
            try:
                escaped_final_text = escape_markdown_v2(final_raw_text)
                if len(escaped_final_text) > TELEGRAM_MAX_MESSAGE_LENGTH:
                    logger.info("Final summary (MD) is too long, using send_long_message_fallback.")
                    await send_long_message_fallback(update, context, final_raw_text)
                else:
                    await placeholder_message.edit_text(escaped_final_text, parse_mode=constants.ParseMode.MARKDOWN_V2,
                                                        reply_markup=feedback_keyboard)

            except BadRequest:
                # If MarkdownV2 fails for any reason, fall back to sending clean plain text
                logger.warning("Final MDV2 edit failed. Sending as transformed plain text.")
                plain_final_text = transform_markdown_fallback(final_raw_text)
                if len(plain_final_text) > TELEGRAM_MAX_MESSAGE_LENGTH:
                    logger.info("Final summary (Plain) is too long, using send_long_message_fallback.")
                    await send_long_message_fallback(update, context,
                                                     final_raw_text)  # send_long_message_fallback already uses plain text
                else:
                    await placeholder_message.edit_text(plain_final_text, parse_mode=None,
                                                        reply_markup=feedback_keyboard)
        else:
            raise ValueError("No summary generated by model")

    except Exception as e:
        logger.error(f"Error during summary stream/edit for URL {url}: {e}", exc_info=True)
        # CORRECTED THE TYPO ON THE NEXT LINE:
        error_text = get_template("url_summary_error", user_lang_code,
                                  default_val="I couldn't generate a summary for that content.")
        try:
            await placeholder_message.edit_text(escape_markdown_v2(error_text),
                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
        except Exception:
            pass

# NEW HELPER FUNCTION 2: To handle follow-up questions
async def _process_url_follow_up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles a follow-up question about the last processed URL.
    """
    user_question = update.message.text
    stored_text = context.chat_data.get('last_url_content')
    url_source = context.chat_data.get('last_url_source', 'the last article')

    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)
    language_name_for_prompt = SUPPORTED_LANGUAGES.get(user_lang_code, "English").split(" (")[0]

    logger.info(f"Handling follow-up question for URL: {url_source} in {language_name_for_prompt}")

    follow_up_prompt = (
        f"The user is asking a follow-up question in {language_name_for_prompt} about an article from {url_source}. "
        f"Please answer their question in {language_name_for_prompt}, based *only* on the provided article content.\n\n"
        f"User's question: '{user_question}'.\n\n"
        f"FULL original text of the article for context: \n\n---\n\n{stored_text}\n---"
    )

    # Since this is a follow-up, we can reuse the main handle_message logic.
    # To avoid code duplication, we'll just modify the prompt and let handle_message do the rest.
    # A cleaner but more complex way would be to refactor handle_message's streaming logic
    # into its own helper that both can call. For now, this is a pragmatic solution.

    # To prevent re-triggering this logic, we clear the context before calling the main handler
    context.chat_data.pop('last_url_content', None)
    context.chat_data.pop('last_url_source', None)

    # Create a "fake" update with the new, combined prompt to pass to the main handler
    fake_update = update
    fake_update.message.text = follow_up_prompt

    # Directly call the main message handler with our new prompt
    await handle_message(fake_update, context)

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
    message_id_for_uniqueness = update.message.message_id

    logger.info(
        f"User {user.id} in chat {chat_id} (msg_id: {message_id_for_uniqueness}) sent document: {doc.file_name} (MIME: {doc.mime_type})")

    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    if not os.path.exists(TEMP_DIR):
        try:
            os.makedirs(TEMP_DIR)
        except OSError as e:
            logger.error(f"Could not create TEMP_DIR '{TEMP_DIR}': {e}")
            error_msg_raw = get_template("error_temp_storage", user_lang_code,
                                         default_val="⚠️ Server error: Cannot create temporary storage.")
            await update.message.reply_text(escape_markdown_v2(error_msg_raw),
                                            parse_mode=constants.ParseMode.MARKDOWN_V2)
            return

    base_name, ext = os.path.splitext(doc.file_name or f"file_{doc.file_id}")
    temp_file_name = f"{chat_id}_{user.id}_{doc.file_id}_{message_id_for_uniqueness}{ext}"
    temp_file_path = os.path.join(TEMP_DIR, temp_file_name)

    if 'mdv2_failed_for_msg_id' not in context.chat_data:
        context.chat_data['mdv2_failed_for_msg_id'] = {}

    placeholder_message: telegram.Message | None = None
    current_placeholder_parse_mode: constants.ParseMode | None = constants.ParseMode.MARKDOWN_V2  # Assume MDV2 initially

    try:
        # CORRECTED: Pass the raw filename, escape the final string
        placeholder_text_raw = get_template("processing_document", user_lang_code,
                                            file_name=(doc.file_name or "document"))
        placeholder_message = await update.message.reply_text(
            escape_markdown_v2(placeholder_text_raw),
            parse_mode=constants.ParseMode.MARKDOWN_V2
        )
        current_placeholder_parse_mode = constants.ParseMode.MARKDOWN_V2
    except BadRequest:
        try:
            placeholder_text_raw = get_template("processing_document", user_lang_code,
                                                file_name=doc.file_name or "document")
            placeholder_message = await update.message.reply_text(placeholder_text_raw, parse_mode=None)
            current_placeholder_parse_mode = None  # Plain text
        except Exception as e_plain_ph:
            logger.error(f"Chat {chat_id}: Failed to send even plain initial placeholder for document: {e_plain_ph}")
            return
    if not placeholder_message:
        logger.error(f"Chat {chat_id}: placeholder_message is None after initial sending. Cannot proceed.")
        return

    if await download_telegram_file(context.bot, doc.file_id, temp_file_path):
        extracted_text = ""
        extraction_successful = False
        try:
            # --- Document Type Specific Extraction ---
            if doc.mime_type == "application/pdf" or doc.file_name.lower().endswith(".pdf"):
                with fitz.open(temp_file_path) as pdf_doc:
                    for page in pdf_doc:
                        extracted_text += page.get_text("text")
                        if len(extracted_text) > 300000:
                            logger.warning(f"PDF {doc.file_name} text extraction stopped at 300k chars.")
                            extracted_text += "\n[...Content truncated due to length...]"
                            break
                logger.info(f"Extracted text from PDF '{doc.file_name}': {len(extracted_text)} chars.")
                extraction_successful = True
            elif doc.mime_type in ["application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                                   "application/msword"] or \
                    doc.file_name.lower().endswith((".docx", ".doc")):
                try:
                    docx_doc = DocxDocument(temp_file_path)
                    for para in docx_doc.paragraphs:
                        extracted_text += para.text + "\n"
                    logger.info(f"Extracted text from DOCX/DOC '{doc.file_name}': {len(extracted_text)} chars.")
                    extraction_successful = True
                except Exception as e_docx:
                    logger.error(f"Error extracting from DOCX/DOC {doc.file_name}: {e_docx}")
                    # This will be caught by the generic e_process_doc handler below
                    raise e_docx
            elif doc.mime_type == "text/plain" or doc.file_name.lower().endswith(".txt"):
                with open(temp_file_path, 'r', encoding='utf-8', errors='ignore') as txt_file:
                    extracted_text = txt_file.read()
                logger.info(f"Read text from TXT '{doc.file_name}': {len(extracted_text)} chars.")
                extraction_successful = True
            else:
                unsupported_msg_raw = get_template("unsupported_document_type", user_lang_code,
                                                   file_type=(doc.mime_type or doc.file_name))
                await placeholder_message.edit_text(escape_markdown_v2(unsupported_msg_raw),
                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)
                if os.path.exists(temp_file_path): os.remove(temp_file_path)
                return

            if not extracted_text.strip() and extraction_successful:
                # CORRECTED: Pass raw filename, then escape
                no_text_msg_raw = get_template("no_text_in_document", user_lang_code,
                                               file_name=(doc.file_name or "the document"))
                try:
                    await placeholder_message.edit_text(escape_markdown_v2(no_text_msg_raw),
                                                        parse_mode=constants.ParseMode.MARKDOWN_V2)
                except BadRequest:
                    await placeholder_message.edit_text(no_text_msg_raw, parse_mode=None)
                return

            elif extracted_text.strip():
                # --- Update placeholder to "Asking AI..." ---
                snippet_info_raw = get_template("extracted_text_snippet_info", user_lang_code,
                                                file_name=(doc.file_name or "the document"),
                                                chars_count=len(extracted_text))
                asking_ai_raw = get_template('asking_ai_analysis', user_lang_code)
                new_placeholder_text_raw = f"{snippet_info_raw}\n\n```\n{extracted_text[:1000]}\n```\n\n{asking_ai_raw}"
                try:
                    await placeholder_message.edit_text(escape_markdown_v2(new_placeholder_text_raw),
                                                        parse_mode=constants.ParseMode.MARKDOWN_V2)
                    current_placeholder_parse_mode = constants.ParseMode.MARKDOWN_V2
                except BadRequest:
                    plain_placeholder = f"{snippet_info_raw}\n---\n{extracted_text[:1000]}\n---\n{asking_ai_raw}"
                    await placeholder_message.edit_text(plain_placeholder, parse_mode=None)
                    current_placeholder_parse_mode = None

                initial_placeholder_text_for_gemini_interaction = placeholder_message.text
                current_message_text_on_telegram = placeholder_message.text

                # --- Prepare for Gemini Call ---
                conversation_history = context.chat_data.get('conversation_history', [])
                language_name_for_prompt = \
                SUPPORTED_LANGUAGES.get(user_lang_code, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE_CODE]).split(" (")[0]
                system_prompt = DEFAULT_SYSTEM_PROMPT_BASE + f"\n\nImportant: Please provide your entire response in {language_name_for_prompt}."
                gemini_question = (
                    f"The user has uploaded a document named '{(doc.file_name or "untitled")}'. "
                    f"Here is the text content extracted from it. Please act as an AI Study Helper: analyze this text, "
                    f"explain key concepts, summarize it, or answer potential questions a student might have about it. "
                    f"Prioritize correctness and clarity in your explanation.\n\n"
                    f"Extracted Text:\n---\n{extracted_text}\n---"
                )

                accumulated_raw_text_for_current_segment = ""
                full_raw_response_for_history = ""
                last_edit_time = asyncio.get_event_loop().time()

                logger.debug(f"Chat {chat_id}: Calling ask_gemini_stream for document '{doc.file_name}' content.")
                async for chunk_raw in ask_gemini_stream(gemini_question, conversation_history, system_prompt):
                    full_raw_response_for_history += chunk_raw
                    accumulated_raw_text_for_current_segment += chunk_raw
                    current_time = asyncio.get_event_loop().time()

                    current_placeholder_mdv2_has_failed_parsing = context.chat_data['mdv2_failed_for_msg_id'].get(
                        placeholder_message.message_id, False)

                    should_edit_now = (
                            current_message_text_on_telegram == initial_placeholder_text_for_gemini_interaction or
                            current_time - last_edit_time >= STREAM_UPDATE_INTERVAL or
                            len(chunk_raw) > 70
                    )

                    if accumulated_raw_text_for_current_segment.strip() and should_edit_now:
                        raw_text_to_process = accumulated_raw_text_for_current_segment
                        text_to_send_this_edit = ""
                        parse_mode_for_this_edit_attempt = None

                        if current_placeholder_mdv2_has_failed_parsing:
                            logger.debug(
                                f"Chat {chat_id} (Doc Stream): MDV2 previously failed for msg {placeholder_message.message_id}. Using TRANSFORMED PLAIN.")
                            text_to_send_this_edit = transform_markdown_fallback(raw_text_to_process)
                            parse_mode_for_this_edit_attempt = None
                        else:
                            text_to_send_this_edit = escape_markdown_v2(raw_text_to_process)
                            parse_mode_for_this_edit_attempt = constants.ParseMode.MARKDOWN_V2

                        if len(text_to_send_this_edit) > TELEGRAM_MAX_MESSAGE_LENGTH:
                            logger.info(
                                f"Chat {chat_id} (Doc Stream): Text for chosen format ({'MDV2' if parse_mode_for_this_edit_attempt else 'PLAIN'}) too long. Offloading.")

                            done_message_raw = get_template("response_continued_below", user_lang_code,
                                                            default_val="...(see new messages below)...")
                            try:
                                if placeholder_message.text != escape_markdown_v2(done_message_raw):
                                    await placeholder_message.edit_text(escape_markdown_v2(done_message_raw),
                                                                        parse_mode=constants.ParseMode.MARKDOWN_V2)
                            except BadRequest:
                                if placeholder_message.text != done_message_raw:
                                    await placeholder_message.edit_text(done_message_raw, parse_mode=None)

                            await send_long_message_fallback(update, context, raw_text_to_process)
                            accumulated_raw_text_for_current_segment = ""

                            if placeholder_message.message_id in context.chat_data['mdv2_failed_for_msg_id']:
                                del context.chat_data['mdv2_failed_for_msg_id'][placeholder_message.message_id]

                            continuing_raw = get_template("continuing_response", user_lang_code,
                                                          default_val="...continuing response...")
                            try:
                                placeholder_message = await update.message.reply_text(
                                    escape_markdown_v2(continuing_raw), parse_mode=constants.ParseMode.MARKDOWN_V2)
                                current_placeholder_parse_mode = constants.ParseMode.MARKDOWN_V2
                            except BadRequest:
                                placeholder_message = await update.message.reply_text(continuing_raw, parse_mode=None)
                                current_placeholder_parse_mode = None

                            initial_placeholder_text_for_gemini_interaction = placeholder_message.text
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
                                        context.chat_data['mdv2_failed_for_msg_id'][
                                            placeholder_message.message_id] = False
                                logger.debug(
                                    f"Chat {chat_id} (Doc Stream): Edit with {'ESCAPED MDV2' if parse_mode_for_this_edit_attempt else 'TRANSFORMED PLAIN'} successful.")
                            except BadRequest as e_edit_stream:
                                if "message is not modified" in str(e_edit_stream).lower():
                                    pass
                                elif parse_mode_for_this_edit_attempt == constants.ParseMode.MARKDOWN_V2 and \
                                        any(err_str in str(e_edit_stream).lower() for err_str in
                                            ["can't parse entities", "unescaped", "can't find end of",
                                             "nested entities"]):
                                    logger.warning(
                                        f"Chat {chat_id} (Doc Stream): ESCAPED MDV2 FAILED PARSING: {e_edit_stream}. Sticking to plain for msg_id {placeholder_message.message_id}."
                                    )
                                    context.chat_data['mdv2_failed_for_msg_id'][placeholder_message.message_id] = True

                                    transformed_retry = transform_markdown_fallback(raw_text_to_process)
                                    if len(transformed_retry) > TELEGRAM_MAX_MESSAGE_LENGTH:
                                        transformed_retry = transformed_retry[:TELEGRAM_MAX_MESSAGE_LENGTH]
                                    try:
                                        if transformed_retry != current_message_text_on_telegram:
                                            await context.bot.edit_message_text(
                                                transformed_retry, chat_id, placeholder_message.message_id,
                                                parse_mode=None
                                            )
                                            current_placeholder_parse_mode = None
                                            current_message_text_on_telegram = transformed_retry
                                        logger.info(
                                            f"Chat {chat_id} (Doc Stream): Retry edit with TRANSFORMED PLAIN successful.")
                                    except BadRequest as e_plain_retry_stream:
                                        if "message is not modified" not in str(e_plain_retry_stream).lower():
                                            logger.error(
                                                f"Chat {chat_id} (Doc Stream): TRANSFORMED PLAIN retry FAILED: {e_plain_retry_stream}")
                                else:
                                    logger.error(
                                        f"Chat {chat_id} (Doc Stream): Unhandled BadRequest during stream edit: {e_edit_stream}")

                        last_edit_time = current_time
                        await asyncio.sleep(0.05)

                # --- Final Edit/Message Handling ---
                logger.info(
                    f"Chat {chat_id} (Doc): Gemini stream finished. Full raw response length: {len(full_raw_response_for_history)}.")
                final_segment_raw = accumulated_raw_text_for_current_segment.strip()

                if final_segment_raw:
                    final_placeholder_mdv2_has_failed_parsing = context.chat_data['mdv2_failed_for_msg_id'].get(
                        placeholder_message.message_id, False)
                    text_for_final_edit = ""
                    parse_mode_for_final_edit_attempt = None

                    if final_placeholder_mdv2_has_failed_parsing:
                        text_for_final_edit = transform_markdown_fallback(final_segment_raw)
                        parse_mode_for_final_edit_attempt = None
                    else:
                        text_for_final_edit = escape_markdown_v2(final_segment_raw)
                        parse_mode_for_final_edit_attempt = constants.ParseMode.MARKDOWN_V2

                    if len(text_for_final_edit) > TELEGRAM_MAX_MESSAGE_LENGTH:
                        logger.info(
                            f"Chat {chat_id} (Doc Final): Final segment too long. Using send_long_message_fallback.")
                        done_message_raw = get_template("response_complete", user_lang_code,
                                                        default_val="✅ Analysis complete.")
                        try:
                            if placeholder_message.text != escape_markdown_v2(done_message_raw):
                                await placeholder_message.edit_text(escape_markdown_v2(done_message_raw),
                                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)
                        except:
                            if placeholder_message.text != done_message_raw:
                                await placeholder_message.edit_text(done_message_raw, parse_mode=None)
                        await send_long_message_fallback(update, context, final_segment_raw)
                    else:
                        try:
                            if text_for_final_edit != current_message_text_on_telegram:
                                feedback_keyboard = build_feedback_keyboard(placeholder_message.message_id)
                                await placeholder_message.edit_text(text_for_final_edit,
                                                                    parse_mode=parse_mode_for_final_edit_attempt,
                                                                    reply_markup=feedback_keyboard)
                            logger.info(
                                f"Chat {chat_id} (Doc Final): Final edit with {'ESCAPED MDV2' if parse_mode_for_final_edit_attempt else 'TRANSFORMED PLAIN'} successful.")
                        except BadRequest as e_f_edit:
                            if "message is not modified" in str(e_f_edit).lower():
                                pass
                            elif parse_mode_for_final_edit_attempt == constants.ParseMode.MARKDOWN_V2 and \
                                    any(err_str in str(e_f_edit).lower() for err_str in
                                        ["can't parse entities", "unescaped", "can't find end of", "nested entities"]):
                                logger.warning(
                                    f"Chat {chat_id} (Doc Final): Final Escaped MDV2 FAILED PARSING: {e_f_edit}. Trying transformed plain.")
                                transformed_final_fallback = transform_markdown_fallback(final_segment_raw)
                                if len(transformed_final_fallback) > TELEGRAM_MAX_MESSAGE_LENGTH:
                                    transformed_final_fallback = transformed_final_fallback[
                                                                 :TELEGRAM_MAX_MESSAGE_LENGTH]
                                try:
                                    if transformed_final_fallback != current_message_text_on_telegram:
                                        await placeholder_message.edit_text(transformed_final_fallback, parse_mode=None)
                                    logger.info(
                                        f"Chat {chat_id} (Doc Final): Final edit with TRANSFORMED PLAIN fallback successful.")
                                except BadRequest as e_f_plain_fb:
                                    if "message is not modified" not in str(e_f_plain_fb).lower():
                                        logger.error(
                                            f"Chat {chat_id} (Doc Final): Final TRANSFORMED PLAIN fallback FAILED: {e_f_plain_fb}")
                            else:
                                logger.error(f"Chat {chat_id} (Doc Final): Final edit failed: {e_f_edit}")
                elif placeholder_message.text == initial_placeholder_text_for_gemini_interaction and not full_raw_response_for_history.strip():
                    no_gemini_resp_raw = get_template("gemini_no_response_document", user_lang_code,
                                                      default_val="🤷 No analysis generated for the document.")
                    try:
                        await placeholder_message.edit_text(escape_markdown_v2(no_gemini_resp_raw),
                                                            parse_mode=constants.ParseMode.MARKDOWN_V2)
                    except:
                        await placeholder_message.edit_text(no_gemini_resp_raw, parse_mode=None)
                elif full_raw_response_for_history.strip():
                    done_message_raw = get_template("response_complete", user_lang_code,
                                                    default_val="✅ Analysis complete.")
                    try:
                        if placeholder_message.text != escape_markdown_v2(done_message_raw):
                            await placeholder_message.edit_text(escape_markdown_v2(done_message_raw),
                                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
                    except:
                        if placeholder_message.text != done_message_raw:
                            await placeholder_message.edit_text(done_message_raw, parse_mode=None)

                # --- Save to history ---
                if full_raw_response_for_history.strip() and not any(
                        err_msg in full_raw_response_for_history.lower() for err_msg in
                        ["sorry", "i can't", "unable to", "blocked", "guidelines", "cannot provide"]):
                    history_user_prompt = f"User uploaded document '{(doc.file_name or "untitled")}' for analysis."
                    conversation_history.append({'role': 'user', 'parts': [{'text': history_user_prompt}]})
                    conversation_history.append({'role': 'model', 'parts': [{'text': full_raw_response_for_history}]})
                    context.chat_data['conversation_history'] = conversation_history[-MAX_CONVERSATION_TURNS * 2:]
                    logger.debug(
                        f"Chat {chat_id} (Doc): Conversation history updated. Length: {len(context.chat_data['conversation_history'])}.")
                else:
                    logger.warning(
                        f"Chat {chat_id} (Doc): Gemini response was empty or refusal-like. Not saving. Preview: '{full_raw_response_for_history[:100].replace(chr(10), ' ')}...'")

        except Exception as e_process_doc:
            logger.error(f"Error processing document '{(doc.file_name or 'N/A')}': {e_process_doc}", exc_info=True)
            # CORRECTED: Pass raw filename, then escape
            error_msg_raw = get_template("document_processing_error", user_lang_code,
                                         file_name=(doc.file_name or "the file"))
            if placeholder_message:
                try:
                    await placeholder_message.edit_text(escape_markdown_v2(error_msg_raw),
                                                        parse_mode=constants.ParseMode.MARKDOWN_V2)
                except BadRequest:
                    await placeholder_message.edit_text(error_msg_raw, parse_mode=None)
        finally:
            if placeholder_message and placeholder_message.message_id in context.chat_data.get('mdv2_failed_for_msg_id',
                                                                                               {}):
                del context.chat_data['mdv2_failed_for_msg_id'][placeholder_message.message_id]
            if os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                    logger.debug(f"Cleaned up temporary document: {temp_file_path}")
                except Exception as e_remove:
                    logger.error(f"Error removing temporary document {temp_file_path}: {e_remove}")
    else:
        # CORRECTED: Pass raw filename, then escape
        download_fail_raw = get_template("download_failed_error", user_lang_code,
                                         file_name=(doc.file_name or "the document"))
        if placeholder_message:
            try:
                await placeholder_message.edit_text(escape_markdown_v2(download_fail_raw),
                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)
            except BadRequest:
                await placeholder_message.edit_text(download_fail_raw, parse_mode=None)
        else:
            await update.message.reply_text(escape_markdown_v2(download_fail_raw),
                                            parse_mode=constants.ParseMode.MARKDOWN_V2)

def escape_markdown_v2(text: str) -> str:
    """
    Escapes text for Telegram MarkdownV2.
    It deliberately does NOT escape '*' and '_' to allow for Gemini-produced bold/italic.
    It also does NOT escape '\' as it's assumed manual escapes are intentional.
    """
    if not isinstance(text, str):
        text = str(text)
    # Characters to escape (excluding * and _ for bold/italic, and \ for manual escapes)
    # Original list: _ * [ ] ( ) ~ ` > # + - = | { } . ! \
    # We escape:     [ ] ( ) ~ ` > # + - = | { } . !
    # REMOVED '\' from this pattern
    escape_chars_pattern = re.compile(r'([\[\]()~`>#+\-=|{}.!])') # Removed \\ from the char set
    escaped_text = escape_chars_pattern.sub(r'\\\1', text)
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
    await update.message.reply_text(escape_markdown_v2(full_welcome_message),
                                    parse_mode=constants.ParseMode.MARKDOWN_V2)

    reset_text = get_template("reset_history_prompt", initial_bot_lang_code)
    yes_button_text = get_template("yes_button_text", initial_bot_lang_code)
    no_button_text = get_template("no_button_text", initial_bot_lang_code)

    reset_keyboard = [[
        InlineKeyboardButton(yes_button_text, callback_data="confirm_start_reset_actions"),
        InlineKeyboardButton(no_button_text, callback_data="cancel_start_reset_actions"),
    ]]
    reset_reply_markup = InlineKeyboardMarkup(reset_keyboard)

    await update.message.reply_text(escape_markdown_v2(reset_text), reply_markup=reset_reply_markup,
                                    parse_mode=constants.ParseMode.MARKDOWN_V2)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username or user.first_name}) requested /help")

    # Determine language for help text
    current_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    # Note: The help_text_body in localization.py already has Markdown V2 style escapes (\\, \_)
    # So we don't need to call escape_markdown_v2() on it again if it's pre-escaped.
    # If it's plain text in templates, then you would escape it.
    # For this example, assuming help_text_body in templates is plain text.
    help_text_raw = get_template("help_text_body", current_lang_code)
    help_text_escaped = escape_markdown_v2(help_text_raw)
    # If your template is already escaped: help_text_to_send = get_template("help_text_body", current_lang_code)

    await update.message.reply_text(help_text_escaped, parse_mode=constants.ParseMode.MARKDOWN_V2)


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
        escape_markdown_v2(stats_text),
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
    confirmation_escaped = escape_markdown_v2(confirmation_raw)

    try:
        await update.message.reply_text(confirmation_escaped, parse_mode=constants.ParseMode.MARKDOWN_V2)
    except BadRequest as e:
        logger.warning(
            f"Chat {chat_id}: Failed to send MDV2 confirmation for new chat. Error: {e}. Falling back to plain text.")
        await update.message.reply_text(confirmation_raw, parse_mode=None)
    except Exception as e:
        logger.error(f"Chat {chat_id}: Unexpected error sending new chat confirmation: {e}", exc_info=True)

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

    if query.data.startswith("set_lang_") or query.data.startswith("lang_page_"):
        logger.warning(f"Chat {chat_id}: Lang CB {query.data} reached generic_button_cb.")
        await query.answer("Processing...")
        return

    await query.answer()
    callback_data = query.data
    logger.info(f"Chat {chat_id}: User {user_id} pressed button: {callback_data}")

    text_to_send_raw = ""  # Raw text from template
    response_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)
    response_lang_display_name = SUPPORTED_LANGUAGES.get(response_lang_code, "English").split(" (")[0]

    if callback_data == "confirm_start_reset_actions":
        context.chat_data.pop('conversation_history', None)
        logger.info(f"Chat {chat_id}: History reset. Language remains '{response_lang_display_name}'.")
        text_to_send_raw = get_template(
            "history_cleared_confirmation",
            response_lang_code,
            response_lang_display_name=response_lang_display_name
        )
    elif callback_data == "cancel_start_reset_actions":
        logger.info(f"Chat {chat_id}: Reset cancelled. Language remains '{response_lang_display_name}'.")
        text_to_send_raw = get_template(
            "reset_cancelled_confirmation",
            response_lang_code,
            response_lang_display_name=response_lang_display_name
        )

    if text_to_send_raw:
        try:
            await query.edit_message_text(
                text=escape_markdown_v2(text_to_send_raw),  # Escape after getting from template
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

@rate_limit()
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all incoming text messages. Acts as a router to determine if the message
    is a standard text query or a contextual reply to a previously sent media file.
    """
    # --- Start of function is unchanged ---
    if not update.message or not update.message.text:
        return

    # --- ROUTING LOGIC ---

    # ## ROUTE 1: Check for a URL in the message text ##
    # A simple regex to find URLs
    url_pattern = r'https?://[^\s/$.?#].[^\s]*'
    found_url = re.search(url_pattern, update.message.text)

    if found_url:
        logger.info(f"URL detected in message: {found_url.group(0)}")
        await _process_url(update, context, found_url.group(0))
        return  # Stop further processing

    # ## ROUTE 2: Check for a reply to a bot message (our previous summary) ##
    if update.message.reply_to_message and update.message.reply_to_message.from_user.is_bot:
        # Check if it's a follow-up to the last summarized URL
        if 'last_url_content' in context.chat_data:
            await _process_url_follow_up(update, context)
            return  # Stop further processing

        # Check for reply to photo (existing logic)
        if update.message.reply_to_message.photo:
            logger.info("User is replying to a photo. Routing to image processor.")
            file_id = update.message.reply_to_message.photo[-1].file_id
            new_prompt = update.message.text
            await _process_image(update, context, file_id, new_prompt)
            return

    # --- IF NO SPECIAL ROUTE WAS TAKEN, PROCEED WITH STANDARD TEXT HANDLING ---

    increment_stat(context, "messages_received")
    if 'mdv2_failed_for_msg_id' not in context.chat_data:
        context.chat_data['mdv2_failed_for_msg_id'] = {}
    if update.message.reply_to_message:
        replied_message = update.message.reply_to_message
        if replied_message.photo and update.message.text:
            logger.info("User is replying to a photo. Routing to image processor.")
            file_id = replied_message.photo[-1].file_id
            new_prompt = update.message.text
            await _process_image(update, context, file_id, new_prompt)
            return
    if not update.message.text:
        return
    user, message_text, chat_id = update.effective_user, update.message.text, update.effective_chat.id
    logger.info(f"Chat {chat_id}: User {user.id} handling standard text message: '{message_text[:100]}...'")
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)
    lang_name_prompt = SUPPORTED_LANGUAGES.get(user_lang_code, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE_CODE]).split(" (")[0]
    system_prompt = DEFAULT_SYSTEM_PROMPT_BASE + f"\n\nImportant: Please provide your entire response in {lang_name_prompt}."
    conversation_history = context.chat_data.get('conversation_history', [])
    if 'mdv2_failed_for_msg_id' not in context.chat_data:
        context.chat_data['mdv2_failed_for_msg_id'] = {}
    placeholder_message: Message | None = None
    current_placeholder_parse_mode: constants.ParseMode | None = constants.ParseMode.MARKDOWN_V2
    try:
        thinking_raw = get_template("thinking", user_lang_code, default_val="🧠 Thinking...")
        placeholder_message = await update.message.reply_text(escape_markdown_v2(thinking_raw),
                                                              parse_mode=constants.ParseMode.MARKDOWN_V2)
    except BadRequest:
        thinking_raw = get_template("thinking", user_lang_code, default_val="🧠 Thinking...")
        placeholder_message = await update.message.reply_text(thinking_raw, parse_mode=None)
        current_placeholder_parse_mode = None
    except Exception as e:
        logger.error(f"Chat {chat_id}: Failed to send initial placeholder for text message: {e}", exc_info=True)
        return
    if not placeholder_message:
        logger.error(f"Chat {chat_id}: placeholder_message is None after initial sending. Cannot proceed.")
        return
    initial_placeholder_text = placeholder_message.text
    current_message_text_on_telegram = placeholder_message.text
    accumulated_raw_text_for_current_segment = ""
    full_raw_response_for_history = ""
    last_edit_time = asyncio.get_event_loop().time()
    try:
        logger.debug(f"Chat {chat_id}: Calling ask_gemini_stream with tool support.")
        # --- Streaming loop is unchanged ---
        async for chunk in ask_gemini_stream(message_text, conversation_history, system_prompt):
            if isinstance(chunk, dict) and chunk.get("tool_call_start"):
                tool_name = chunk.get("tool_name", "unknown_tool")
                logger.info(f"Chat {chat_id}: Received tool call signal for '{tool_name}'.")
                if tool_name == "perform_web_search":
                    increment_stat(context, "web_searches")
                    searching_raw = get_template("searching_web", user_lang_code, default_val="Searching the web... 🌐")
                    try:
                        await placeholder_message.edit_text(escape_markdown_v2(searching_raw),
                                                            parse_mode=constants.ParseMode.MARKDOWN_V2)
                        current_placeholder_parse_mode = constants.ParseMode.MARKDOWN_V2
                    except BadRequest:
                        await placeholder_message.edit_text(searching_raw, parse_mode=None)
                        current_placeholder_parse_mode = None
                    initial_placeholder_text = placeholder_message.text
                    current_message_text_on_telegram = placeholder_message.text
                    accumulated_raw_text_for_current_segment = ""
                continue
            if not isinstance(chunk, str): continue
            chunk_raw = chunk
            full_raw_response_for_history += chunk_raw
            accumulated_raw_text_for_current_segment += chunk_raw
            current_time = asyncio.get_event_loop().time()
            current_placeholder_mdv2_has_failed_parsing = context.chat_data['mdv2_failed_for_msg_id'].get(placeholder_message.message_id, False)
            should_edit_now = (current_message_text_on_telegram == initial_placeholder_text or current_time - last_edit_time >= STREAM_UPDATE_INTERVAL or len(chunk_raw) > 70)
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
                    continue_message_raw = get_template("response_continued_below", user_lang_code, default_val="...(see new messages below)...")
                    try:
                        if placeholder_message.text != escape_markdown_v2(continue_message_raw):
                            await placeholder_message.edit_text(escape_markdown_v2(continue_message_raw), parse_mode=constants.ParseMode.MARKDOWN_V2)
                    except BadRequest:
                        if placeholder_message.text != continue_message_raw:
                            await placeholder_message.edit_text(continue_message_raw, parse_mode=None)
                    await send_long_message_fallback(update, context, raw_text_to_process)
                    accumulated_raw_text_for_current_segment = ""
                    if placeholder_message.message_id in context.chat_data['mdv2_failed_for_msg_id']:
                        del context.chat_data['mdv2_failed_for_msg_id'][placeholder_message.message_id]
                    continuing_raw = get_template("continuing_response", user_lang_code, default_val="...continuing response...")
                    try:
                        placeholder_message = await update.message.reply_text(escape_markdown_v2(continuing_raw), parse_mode=constants.ParseMode.MARKDOWN_V2)
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
                        logger.debug(f"Chat {chat_id} (Text Stream): Edit with {'MDV2' if parse_mode_for_this_edit_attempt else 'PLAIN'} successful.")
                    except BadRequest as e_edit_stream:
                        if "message is not modified" in str(e_edit_stream).lower():
                            pass
                        elif parse_mode_for_this_edit_attempt == constants.ParseMode.MARKDOWN_V2 and any(err_str in str(e_edit_stream).lower() for err_str in ["can't parse entities", "unescaped", "can't find end of", "nested entities"]):
                            logger.warning(f"Chat {chat_id} (Text Stream): MDV2 FAILED PARSING: {e_edit_stream}. Sticking to plain for msg_id {placeholder_message.message_id}.")
                            context.chat_data['mdv2_failed_for_msg_id'][placeholder_message.message_id] = True
                            transformed_retry = transform_markdown_fallback(raw_text_to_process)
                            if len(transformed_retry) > TELEGRAM_MAX_MESSAGE_LENGTH:
                                transformed_retry = transformed_retry[:TELEGRAM_MAX_MESSAGE_LENGTH]
                            try:
                                if transformed_retry != current_message_text_on_telegram:
                                    await context.bot.edit_message_text(transformed_retry, chat_id, placeholder_message.message_id, parse_mode=None)
                                    current_placeholder_parse_mode = None
                                    current_message_text_on_telegram = transformed_retry
                                logger.info(f"Chat {chat_id} (Text Stream): Retry edit with TRANSFORMED PLAIN successful.")
                            except BadRequest as e_plain_retry_stream:
                                if "message is not modified" not in str(e_plain_retry_stream).lower():
                                    logger.error(f"Chat {chat_id} (Text Stream): TRANSFORMED PLAIN retry FAILED: {e_plain_retry_stream}")
                        else:
                            logger.error(f"Chat {chat_id} (Text Stream): Unhandled BadRequest during stream edit: {e_edit_stream}")
                last_edit_time = current_time
                await asyncio.sleep(0.05)

        # --- Final Edit & History Saving ---
        logger.info(f"Chat {chat_id} (Text): Stream finished. Full raw response length: {len(full_raw_response_for_history)}.")
        final_segment_raw = accumulated_raw_text_for_current_segment.strip()

        if final_segment_raw:
            final_placeholder_mdv2_has_failed_parsing = context.chat_data['mdv2_failed_for_msg_id'].get(placeholder_message.message_id, False)
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
                    # #######################################################################
                    # ## THE FIX: REMOVED THE `if text_for_final_edit != ...` CONDITION ##
                    # #######################################################################
                    # This FORCES the final edit, which adds the buttons.
                    # The "message is not modified" error is handled gracefully below.
                    await placeholder_message.edit_text(text_for_final_edit,
                                                        parse_mode=parse_mode_for_final_edit,
                                                        reply_markup=feedback_keyboard)
                    logger.info(f"Chat {chat_id} (Text Final): Final edit with {'MDV2' if parse_mode_for_final_edit else 'PLAIN'} successful.")
                except BadRequest as e_f_edit:
                    if "message is not modified" in str(e_f_edit).lower():
                        # This is now expected and harmless. It means the text was already final,
                        # but the buttons were added successfully (or were already there).
                        pass
                    elif parse_mode_for_final_edit == constants.ParseMode.MARKDOWN_V2:
                        logger.warning(f"Chat {chat_id} (Text Final): Final MDV2 edit FAILED PARSING: {e_f_edit}. Trying plain fallback.")
                        transformed_final_fallback = transform_markdown_fallback(final_segment_raw)
                        if len(transformed_final_fallback) > TELEGRAM_MAX_MESSAGE_LENGTH:
                            transformed_final_fallback = transformed_final_fallback[:TELEGRAM_MAX_MESSAGE_LENGTH]
                        try:
                            await placeholder_message.edit_text(transformed_final_fallback, parse_mode=None, reply_markup=feedback_keyboard)
                            logger.info(f"Chat {chat_id} (Text Final): Final edit with TRANSFORMED PLAIN fallback successful.")
                        except BadRequest as e_f_plain_fb:
                            if "message is not modified" not in str(e_f_plain_fb).lower():
                                logger.error(f"Chat {chat_id} (Text Final): Final plain fallback FAILED: {e_f_plain_fb}")
                    else:
                        logger.error(f"Chat {chat_id} (Text Final): Final edit failed: {e_f_edit}")

        elif not full_raw_response_for_history.strip():
            no_response_raw = get_template("gemini_no_response_text", user_lang_code, default_val="🤷 No response generated.")
            try:
                if placeholder_message.text != escape_markdown_v2(no_response_raw):
                    await placeholder_message.edit_text(escape_markdown_v2(no_response_raw), parse_mode=constants.ParseMode.MARKDOWN_V2)
            except BadRequest:
                if placeholder_message.text != no_response_raw:
                    await placeholder_message.edit_text(no_response_raw, parse_mode=None)

        # --- History saving is unchanged ---
        if full_raw_response_for_history.strip() and not any(kw in full_raw_response_for_history.lower() for kw in ["i can't", "sorry", "unable to", "guidelines", "blocked", "cannot provide"]):
            conversation_history.append({'role': 'user', 'parts': [{'text': message_text}]})
            conversation_history.append({'role': 'model', 'parts': [{'text': full_raw_response_for_history}]})
            context.chat_data['conversation_history'] = conversation_history[-(MAX_CONVERSATION_TURNS * 2):]
            logger.debug(f"Chat {chat_id}: History updated. Len: {len(context.chat_data['conversation_history'])}.")
        else:
            logger.warning(f"Chat {chat_id}: AI response empty/refusal. Not saved. Preview: '{full_raw_response_for_history[:100].replace(chr(10), ' ')}...'")

    except Exception as e_outer:
        logger.error(f"Chat {chat_id}: Unhandled error in handle_message: {e_outer}", exc_info=True)
        err_proc_raw = get_template("unexpected_error_processing", user_lang_code, default_val="⚠️ An unexpected error occurred.")
        try:
            if placeholder_message and placeholder_message.text != escape_markdown_v2(err_proc_raw):
                await placeholder_message.edit_text(escape_markdown_v2(err_proc_raw), parse_mode=constants.ParseMode.MARKDOWN_V2)
        except Exception:
            pass
    finally:
        if placeholder_message and placeholder_message.message_id in context.chat_data.get('mdv2_failed_for_msg_id', {}):
            del context.chat_data['mdv2_failed_for_msg_id'][placeholder_message.message_id]
        logger.info(f"--- handle_message finished for chat {chat_id} ---")


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

async def set_bot_commands(application: Application):
    """
    Sets the bot's commands for multiple languages, mapping to Telegram's
    supported language codes and gracefully skipping any that are invalid.
    """
    # 1. Set the default commands in English first as a fallback
    try:
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

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CommandHandler("new", new_chat_command))

    # --- Callback Query Handlers ---
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