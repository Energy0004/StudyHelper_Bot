# --- START OF FILE telegram_bot.py ---

import re
from collections import OrderedDict
import os
import logging
import asyncio
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
    To ensure your answers are easy to study from, you MUST structure them for clarity. Avoid long, unbroken "walls of text".
    - **Use Headings:** Use bold text (`*Heading*`) to introduce different sections of your answer.
    - **Use Lists:** For steps, examples, or multiple points, ALWAYS use bulleted (`* `) or numbered (`1. `) lists.
    - **Use Whitespace:** Separate distinct ideas and paragraphs with an empty line to give the text "breathing room".
    - **Highlight Keywords:** Emphasize important terms using `*bold*` or `_italics_` to draw the user's attention.
    - **Data Comparison:** When comparing items, present the information under separate, clearly bolded headings for each item.
    - **DO NOT** create tables using plain text characters like `|` and `-`. This formatting breaks in chat applications.
    - **INSTEAD**, if a table is needed, use proper Markdown table syntax. Example:
      | Feature    | Item A    | Item B    |
      |------------|-----------|-----------|
      | Property   | Value A   | Value B   |

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
    If uncertain about a complex formatting, prefer simpler, well-formed Markdown or plain text for that segment."""
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

SCRIPT_TO_LANG_MAP = {
    "Latin": "eng",              # English, Spanish, French, German, Portuguese, Italian, Dutch, Polish, Swedish, Finnish, Norwegian, Danish, Romanian, Turkish, Hungarian, Czech, Malay, Indonesian
    "Cyrillic": "rus",           # Russian, Ukrainian, Uzbek, Kazakh (assumes Russian is default for Cyrillic)
    "Han": "chi_sim",            # Simplified Chinese
    "Hant": "chi_tra",           # Traditional Chinese
    "Hiragana": "jpn",           # Japanese
    "Katakana": "jpn",           # Japanese
    "Hangul": "kor",             # Korean
    "Arabic": "ara",             # Arabic
    "Devanagari": "hin",         # Hindi
    "Greek": "ell",              # Greek
    "Hebrew": "heb",             # Hebrew
    "Thai": "tha",               # Thai
    "Vietnamese": "vie",         # Vietnamese
    "Bopomofo": "chi_tra",       # Taiwanese Chinese with Bopomofo
    # Optional: Fallbacks or specific mappings
    "Kana": "jpn",
    "Common": "eng",             # For symbols, numbers, etc.
    "Inherited": "eng",          # For diacritics or inherited marks
}

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
                        await placeholder_message.edit_text(escape_markdown_v2(full_raw_response_for_history),
                                                            parse_mode=constants.ParseMode.MARKDOWN_V2)
                    except BadRequest:
                        await placeholder_message.edit_text(transform_markdown_fallback(full_raw_response_for_history),
                                                            parse_mode=None)
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
async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.document:
        logger.warning("handle_document called without a message or document.")
        return

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
                                await placeholder_message.edit_text(text_for_final_edit,
                                                                    parse_mode=parse_mode_for_final_edit_attempt)
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
    Transforms Gemini's Markdown-like output into a plainer text format
    when MarkdownV2 parsing fails or is undesirable.
    Converts headings, lists, bold, italics to simpler plain text representations.
    Includes a step to neutralize potentially problematic standalone underscores.
    """
    if not text:
        return ""

    # Use a passed-in logger or a default one if not available globally
    # This is safer if the function is ever moved or used in a different context.
    # For now, assuming 'logger' is available from the global scope of telegram_bot.py
    _logger = logger

    _logger.debug(f"Transforming text for fallback. Original starts: '{text[:100].replace(chr(10), ' ')}...'")

    transformed_text = text

    # 0. Normalize line endings (do this early)
    transformed_text = transformed_text.replace('\r\n', '\n')

    # NEW STEP A: Attempt to neutralize problematic underscores.
    UNDERSCORE_PLACEHOLDER = "❮USPH❯"
    transformed_text = re.sub(r'(?<=\w)_(?=\w)', UNDERSCORE_PLACEHOLDER, transformed_text)

    # 1. Strip leading/trailing whitespace from the whole text AFTER initial underscore handling
    transformed_text = transformed_text.strip()

    # 2. Handle code blocks (simple removal of backticks, keep content)
    # Important: Do this before italic/bold processing to protect content within code blocks.
    transformed_text = re.sub(r'```(?:[a-zA-Z0-9_.-]*)?\n(.*?)\n```', r'\1', transformed_text,
                              flags=re.DOTALL | re.MULTILINE)
    # --- THIS WAS THE LINE WITH THE ERROR ---
    transformed_text = re.sub(r'```(.*?)```', r'\1', transformed_text, flags=re.DOTALL)  # Simpler ```code```
    # --- END OF FIX ---
    transformed_text = re.sub(r'`(.*?)`', r'\1', transformed_text)  # Inline `code`

    # 4. Handle bold and italics (Order can matter)
    # Process paired underscores/asterisks first
    transformed_text = re.sub(r'\*\*(.*?)\*\*', r'"\1"', transformed_text)  # **bold** to "bold"
    transformed_text = re.sub(r'__(.*?)__', r'"\1"',
                              transformed_text)  # __underline__ to "quoted" (often used as alternative bold)

    # For single asterisks/underscores for italics:
    transformed_text = re.sub(r'\*(.*?)\*', r'\1', transformed_text)  # *italic* to plain
    transformed_text = re.sub(r'_(.*?)_', r'\1', transformed_text)  # _italic_ to plain

    # NEW STEP B: Convert placeholder back to underscores
    transformed_text = transformed_text.replace(UNDERSCORE_PLACEHOLDER, "_")

    # 5. Handle strikethrough ~strikethrough~ (remove it)
    transformed_text = re.sub(r'~(.*?)~', r'\1', transformed_text)

    # 6. Handle headings (###, ##, #) by making them "Quoted Title:"
    transformed_text = re.sub(r'^\s*###\s*(.*?)\s*$', r'"\1:"', transformed_text, flags=re.MULTILINE)
    transformed_text = re.sub(r'^\s*##\s*(.*?)\s*$', r'"\1:"', transformed_text, flags=re.MULTILINE)
    transformed_text = re.sub(r'^\s*#\s*(.*?)\s*$', r'"\1:"', transformed_text, flags=re.MULTILINE)

    # 7. Process lists and renumber them consistently
    lines = transformed_text.splitlines()
    processed_lines = []
    list_item_counter = 0
    in_list_context = False

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        bullet_match = re.match(r"^(\s*)(?:[*\-+]|\u2022)\s+(.*)", line)
        numbered_list_match = re.match(r"^(\s*)(\d+)\.\s+(.*)", line)

        item_content = ""

        if bullet_match:
            indentation = bullet_match.group(1)
            original_content = bullet_match.group(2).strip()

            if not original_content:
                if in_list_context:
                    processed_lines.append(indentation.rstrip('\n'))
                continue

            item_content = original_content
            is_new_list_block = True
            if processed_lines:
                for j in range(len(processed_lines) - 1, -1, -1):
                    if processed_lines[j].strip():
                        if re.match(r"^\s*\d+\.\s+", processed_lines[j]):
                            is_new_list_block = False
                        break

            if is_new_list_block:
                list_item_counter = 1
            else:
                list_item_counter += 1

            item_content_final = re.sub(r'^("[^"]+:")(\S)', r'\1 \2', item_content)
            processed_lines.append(f"{indentation}{list_item_counter}. {item_content_final}")
            in_list_context = True

        elif numbered_list_match:
            indentation = numbered_list_match.group(1)
            original_number_str = numbered_list_match.group(2)
            original_content = numbered_list_match.group(3).strip()

            if not original_content:
                if in_list_context:
                    processed_lines.append(indentation.rstrip('\n'))
                continue

            item_content = original_content
            is_new_list_block = True
            current_item_number_from_text = int(original_number_str)

            if processed_lines:
                for j in range(len(processed_lines) - 1, -1, -1):
                    if processed_lines[j].strip():
                        if re.match(r"^\s*\d+\.\s+", processed_lines[j]):
                            is_new_list_block = False
                        break

            if is_new_list_block:
                list_item_counter = current_item_number_from_text
            else:
                list_item_counter += 1

            item_content_final = re.sub(r'^("[^"]+:")(\S)', r'\1 \2', item_content)
            processed_lines.append(f"{indentation}{list_item_counter}. {item_content_final}")
            in_list_context = True
        else:
            if stripped_line:
                processed_lines.append(line)
            elif processed_lines and processed_lines[-1].strip():
                processed_lines.append("")
            in_list_context = False

    transformed_text_final = "\n".join(processed_lines)

    # 8. Final cleanup:
    transformed_text_final = re.sub(r'\n{3,}', '\n\n', transformed_text_final)

    _logger.debug(f"Transformed text fallback result starts: '{transformed_text_final[:100].replace(chr(10), ' ')}...'")
    return transformed_text_final.strip()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles all incoming text messages. Acts as a router to determine if the message
    is a standard text query or a contextual reply to a previously sent media file.
    """
    # Preliminary check to ensure there's a message to process.
    if not update.message:
        return

    if 'mdv2_failed_for_msg_id' not in context.chat_data:
        context.chat_data['mdv2_failed_for_msg_id'] = {}

    # --- NEW: CONTEXTUAL REPLY ROUTING LOGIC ---
    if update.message.reply_to_message:
        replied_message = update.message.reply_to_message

        # Route 1: Is it a reply to a photo with a new text prompt?
        if replied_message.photo and update.message.text:
            logger.info("User is replying to a photo. Routing to image processor.")

            # Get the file_id of the REPLIED-TO photo and the new prompt text.
            file_id = replied_message.photo[-1].file_id
            new_prompt = update.message.text

            # Call the central image processor and then stop this handler's execution.
            await _process_image(update, context, file_id, new_prompt)
            return

        # (Future Enhancement) Route 2: Is it a reply to a document?
        # if replied_message.document and update.message.text:
        #     # ... logic to re-process document ...
        #     return

    # --- EXISTING: STANDARD TEXT AND TOOL CALL HANDLING ---
    # If the message is not a contextual reply, or not a reply at all, proceed.

    if not update.message.text:
        # This handles cases like sending a sticker directly.
        return

    user, message_text, chat_id = update.effective_user, update.message.text, update.effective_chat.id
    logger.info(f"Chat {chat_id}: User {user.id} handling standard text message: '{message_text[:100]}...'")

    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)
    lang_name_prompt = SUPPORTED_LANGUAGES.get(user_lang_code, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE_CODE]).split(" (")[
        0]
    system_prompt = DEFAULT_SYSTEM_PROMPT_BASE + f"\n\nImportant: Please provide your entire response in {lang_name_prompt}."
    conversation_history = context.chat_data.get('conversation_history', [])

    # Initialize state trackers
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

        async for chunk in ask_gemini_stream(message_text, conversation_history, system_prompt):
            if isinstance(chunk, dict) and chunk.get("tool_call_start"):
                tool_name = chunk.get("tool_name", "unknown_tool")
                logger.info(f"Chat {chat_id}: Received tool call signal for '{tool_name}'.")

                if tool_name == "perform_web_search":
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

            current_placeholder_mdv2_has_failed_parsing = context.chat_data['mdv2_failed_for_msg_id'].get(
                placeholder_message.message_id, False)

            should_edit_now = (
                    current_message_text_on_telegram == initial_placeholder_text or
                    current_time - last_edit_time >= STREAM_UPDATE_INTERVAL or
                    len(chunk_raw) > 70
            )

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
                        elif parse_mode_for_this_edit_attempt == constants.ParseMode.MARKDOWN_V2 and \
                                any(err_str in str(e_edit_stream).lower() for err_str in
                                    ["can't parse entities", "unescaped", "can't find end of", "nested entities"]):
                            logger.warning(
                                f"Chat {chat_id} (Text Stream): MDV2 FAILED PARSING: {e_edit_stream}. Sticking to plain for msg_id {placeholder_message.message_id}.")
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
        logger.info(
            f"Chat {chat_id} (Text): Stream finished. Full raw response length: {len(full_raw_response_for_history)}.")
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
                try:
                    if text_for_final_edit != current_message_text_on_telegram:
                        await placeholder_message.edit_text(text_for_final_edit, parse_mode=parse_mode_for_final_edit)
                    logger.info(
                        f"Chat {chat_id} (Text Final): Final edit with {'MDV2' if parse_mode_for_final_edit else 'PLAIN'} successful.")
                except BadRequest as e_f_edit:
                    if "message is not modified" in str(e_f_edit).lower():
                        pass
                    elif parse_mode_for_final_edit == constants.ParseMode.MARKDOWN_V2:
                        logger.warning(
                            f"Chat {chat_id} (Text Final): Final MDV2 edit FAILED PARSING: {e_f_edit}. Trying plain fallback.")
                        transformed_final_fallback = transform_markdown_fallback(final_segment_raw)
                        if len(transformed_final_fallback) > TELEGRAM_MAX_MESSAGE_LENGTH:
                            transformed_final_fallback = transformed_final_fallback[:TELEGRAM_MAX_MESSAGE_LENGTH]
                        try:
                            if transformed_final_fallback != current_message_text_on_telegram:
                                await placeholder_message.edit_text(transformed_final_fallback, parse_mode=None)
                            logger.info(
                                f"Chat {chat_id} (Text Final): Final edit with TRANSFORMED PLAIN fallback successful.")
                        except BadRequest as e_f_plain_fb:
                            if "message is not modified" not in str(e_f_plain_fb).lower():
                                logger.error(
                                    f"Chat {chat_id} (Text Final): Final plain fallback FAILED: {e_f_plain_fb}")
                    else:
                        logger.error(f"Chat {chat_id} (Text Final): Final edit failed: {e_f_edit}")

        elif not full_raw_response_for_history.strip():
            no_response_raw = get_template("gemini_no_response_text", user_lang_code,
                                           default_val="🤷 No response generated.")
            try:
                if placeholder_message.text != escape_markdown_v2(no_response_raw):
                    await placeholder_message.edit_text(escape_markdown_v2(no_response_raw),
                                                        parse_mode=constants.ParseMode.MARKDOWN_V2)
            except BadRequest:
                if placeholder_message.text != no_response_raw:
                    await placeholder_message.edit_text(no_response_raw, parse_mode=None)

        # --- Save to Conversation History ---
        if full_raw_response_for_history.strip() and not any(
                kw in full_raw_response_for_history.lower() for kw in
                ["i can't", "sorry", "unable to", "guidelines", "blocked", "cannot provide"]):
            conversation_history.append({'role': 'user', 'parts': [{'text': message_text}]})
            conversation_history.append({'role': 'model', 'parts': [{'text': full_raw_response_for_history}]})
            context.chat_data['conversation_history'] = conversation_history[-(MAX_CONVERSATION_TURNS * 2):]
            logger.debug(f"Chat {chat_id}: History updated. Len: {len(context.chat_data['conversation_history'])}.")
        else:
            logger.warning(
                f"Chat {chat_id}: AI response empty/refusal. Not saved. Preview: '{full_raw_response_for_history[:100].replace(chr(10), ' ')}...'")

    except Exception as e_outer:
        logger.error(f"Chat {chat_id}: Unhandled error in handle_message: {e_outer}", exc_info=True)
        err_proc_raw = get_template("unexpected_error_processing", user_lang_code,
                                    default_val="⚠️ An unexpected error occurred.")
        try:
            if placeholder_message and placeholder_message.text != escape_markdown_v2(err_proc_raw):
                await placeholder_message.edit_text(escape_markdown_v2(err_proc_raw),
                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)
        except Exception:
            pass
    finally:
        if placeholder_message and placeholder_message.message_id in context.chat_data.get('mdv2_failed_for_msg_id',
                                                                                           {}):
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
    Splits a long raw text message and sends it in parts.
    PRIORITIZES sending transformed plain text for readability of lists.
    Falls back to Escaped MarkdownV2 or raw plain if transformed plain fails.
    Returns the last message object sent by this function, or None.
    """
    logger.debug(f"send_long_message_fallback called. Raw text length: {len(text_to_send_raw)}")

    parts_raw = []
    current_text_raw = str(text_to_send_raw)

    if not current_text_raw.strip():
        logger.info("send_long_message_fallback: called with empty/whitespace text. Nothing to send.")
        return None

    # Splitting logic (operates on raw text to find good break points)
    # This tries to create raw segments that, after transformation, might fit.
    # A simple approach is to split raw text based on max_length, as transformation
    # length is unpredictable without doing it first.
    while len(current_text_raw) > 0:
        potential_split_len = max_length  # Split raw based on this
        if len(current_text_raw) > potential_split_len:
            part_segment_raw = current_text_raw[:potential_split_len]
            # Try to find a natural break point (newline or space) near the end
            last_newline = part_segment_raw.rfind('\n', max(0, potential_split_len - 500))  # Look back
            last_space = part_segment_raw.rfind(' ', max(0, potential_split_len - 500))

            split_at = potential_split_len  # Default split point
            if last_newline != -1:
                split_at = last_newline + 1
            elif last_space != -1:
                split_at = last_space + 1

            parts_raw.append(current_text_raw[:split_at])
            current_text_raw = current_text_raw[split_at:].lstrip()
        else:  # Remaining part is small enough
            parts_raw.append(current_text_raw)
            break

    if not parts_raw:
        logger.warning("send_long_message_fallback: No parts were generated. Original text: '%s...'",
                       text_to_send_raw[:100].replace('\n', ' '))
        return None

    last_sent_message_object: Message | None = None
    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    for i, segment_raw_orig in enumerate(parts_raw):
        segment_raw = segment_raw_orig.strip()
        if not segment_raw:
            logger.debug(f"Fallback: Skipping empty segment {i + 1}/{len(parts_raw)}.")
            continue

        log_segment_preview = segment_raw[:70].replace('\n', ' ') + ('...' if len(segment_raw) > 70 else '')
        logger.debug(
            f"Fallback: Processing raw segment {i + 1}/{len(parts_raw)}, raw_len {len(segment_raw)}. Preview: '{log_segment_preview}'")

        sent_successfully = False
        current_segment_message: Message | None = None

        # --- MODIFIED PRIORITY: Attempt Transformed Plain Text FIRST ---
        transformed_segment = transform_markdown_fallback(segment_raw)

        try:
            text_to_send_plain = transformed_segment
            if len(transformed_segment) > max_length:
                logger.warning(
                    f"Fallback: Transformed segment {i + 1} too long ({len(transformed_segment)} chars). Sending original raw (truncated).")
                text_to_send_plain = segment_raw[:max_length]  # Fallback to truncated original raw text

            current_segment_message = await update.message.reply_text(text_to_send_plain, parse_mode=None)
            logger.info(f"Fallback: Sent segment {i + 1}/{len(parts_raw)} as TRANSFORMED PLAIN (or truncated raw).")
            sent_successfully = True
        except Exception as e_plain_fail:
            logger.error(
                f"Fallback: TRANSFORMED PLAIN send FAILED for segment {i + 1}. Error: {e_plain_fail}. Trying Escaped MDV2 as next fallback.")

            # Fallback Attempt 2: Escaped MarkdownV2
            try:
                segment_escaped = escape_markdown_v2(segment_raw)
                text_to_send_md = segment_escaped
                parse_mode_for_md_fallback = constants.ParseMode.MARKDOWN_V2

                if len(segment_escaped) > max_length:
                    logger.warning(
                        f"Fallback: Escaped MDV2 for segment {i + 1} too long ({len(segment_escaped)}). Trying original raw (truncated) as plain.")
                    text_to_send_md = segment_raw[:max_length]  # Ultra fallback to truncated raw plain
                    parse_mode_for_md_fallback = None  # Send as plain

                current_segment_message = await update.message.reply_text(text_to_send_md,
                                                                          parse_mode=parse_mode_for_md_fallback)
                logger.info(
                    f"Fallback: Sent segment {i + 1}/{len(parts_raw)} as ESCAPED MDV2 (or raw plain if MDV2 too long) after plain transformed failed.")
                sent_successfully = True
            except Exception as e_md_ultra_fallback:
                logger.error(
                    f"Fallback: ESCAPED MDV2/RAW PLAIN send ALSO FAILED for segment {i + 1}. Error: {e_md_ultra_fallback}.")

        # Update last sent message object
        if current_segment_message:
            last_sent_message_object = current_segment_message

        # Handle failure to send by any method
        if not sent_successfully:
            logger.critical(
                f"Fallback: FAILED TO SEND segment {i + 1}/{len(parts_raw)} by any method. Preview: '{log_segment_preview}'")
            try:
                # Use a default message if template is missing to avoid further errors
                error_template_key = "error_displaying_response_part"
                default_error_text = "⚠️ Error: A part of the response could not be displayed."
                err_msg_raw = get_template(error_template_key, user_lang_code, default_val=default_error_text)

                err_msg_esc = escape_markdown_v2(err_msg_raw)

                error_confirmation_msg = await context.bot.send_message(
                    chat_id=update.effective_chat.id, text=err_msg_esc, parse_mode=constants.ParseMode.MARKDOWN_V2
                )
                if error_confirmation_msg: last_sent_message_object = error_confirmation_msg
            except Exception as e_generic_error_send:
                logger.error(f"Failed to send 'part lost' error message to user: {e_generic_error_send}")

        # Delay if not the last part and sent successfully
        if i < len(parts_raw) - 1 and sent_successfully:
            await asyncio.sleep(0.35)

    return last_sent_message_object

async def set_bot_commands(application: Application):
    commands = [
        BotCommand("start", "Welcome & clear chat history option"),
        BotCommand("help", "Show help message and commands"),
        BotCommand("language", "Choose your preferred language"),
    ]
    try:
        await application.bot.set_my_commands(commands)
        logger.info("Bot commands successfully set/updated.")
    except Exception as e:
        logger.error(f"Failed to set bot commands: {e}")


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
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("language", language_command))

    # --- Callback Query Handlers ---
    application.add_handler(CallbackQueryHandler(language_set_callback_handler, pattern=r"^set_lang_"))
    application.add_handler(CallbackQueryHandler(language_page_callback_handler, pattern=r"^lang_page_"))
    application.add_handler(CallbackQueryHandler(button_callback_handler))

    # --- Message Handlers ---
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("All command, callback, and message handlers have been successfully registered.")

# --- END OF FILE telegram_bot.py ---