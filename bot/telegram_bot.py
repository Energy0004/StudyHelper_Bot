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
    MAX_CONVERSATION_TURNS = int(os.getenv("MAX_CONVERSATION_TURNS", "5"))
except ValueError:
    logger.warning("MAX_CONVERSATION_TURNS in .env is not valid. Using default 5.")
    MAX_CONVERSATION_TURNS = 5

DEFAULT_SYSTEM_PROMPT_BASE = os.getenv(
    "DEFAULT_SYSTEM_PROMPT_BASE",
    """You are a helpful, accurate, and meticulous AI Study Helper. Your primary goal is to provide correct information and clear explanations.
+ When solving problems, especially mathematical or scientific ones, break down the solution into clear, logical steps.
+ Double-check your formulas and calculations. If you are deriving a formula, explain the reasoning behind each step of the derivation.
+ If you are unsure about a specific detail or formula, it is better to state that you are unsure or guide the user to verify from a reliable source rather than providing potentially incorrect information.
+ Prioritize correctness and clarity above all else. Please use Markdown formatting to make your explanations clear, structured, and visually appealing.
You can use:
- Headings: Start a line with #, ##, or ### followed by a space and your heading text.
- Bold: *bold text*
- Italics: _italic text_
- Inline code: `code`
- Code blocks: ```language\ncode block here\n```
- Bullet lists: Start lines with `* ` or `- ` (ensure a space after the bullet marker).
- Numbered lists: Start lines with `1. ` (ensure a space after the number and period).
Ensure Markdown is well-formed. For example, make sure lists have a space after the bullet/number. Avoid unescaped special characters like '.', '!', '-' within contexts where Telegram might misinterpret them if not part of standard Markdown constructs like lists or code blocks."""
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


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.photo:
        logger.warning("handle_photo called without a message or photo.")
        return

    user = update.effective_user
    chat_id = update.effective_chat.id
    photo_file_id = update.message.photo[-1].file_id
    message_id_for_uniqueness = update.message.message_id

    logger.info(
        f"User {user.id} in chat {chat_id} (msg_id: {message_id_for_uniqueness}) sent photo {photo_file_id} for general multimodal analysis.")

    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)

    if not os.path.exists(TEMP_DIR):
        try:
            os.makedirs(TEMP_DIR)
        except OSError as e:
            logger.error(f"Could not create TEMP_DIR '{TEMP_DIR}': {e}")
            err_storage_raw = get_template("error_temp_storage", user_lang_code,
                                           default_val="⚠️ Server error: Cannot create temporary storage.")
            await update.message.reply_text(escape_markdown_v2(err_storage_raw),
                                            parse_mode=constants.ParseMode.MARKDOWN_V2)
            return

    temp_file_name = f"{chat_id}_{user.id}_{photo_file_id}_{message_id_for_uniqueness}.jpg"
    temp_file_path = os.path.join(TEMP_DIR, temp_file_name)

    # --- MODIFIED PLACEHOLDER INITIALIZATION ---
    placeholder_text_raw = get_template("analyzing_image", user_lang_code,
                                        default_val="Analyzing image... 🖼️✨")
    placeholder_text_escaped = escape_markdown_v2(placeholder_text_raw)

    placeholder_message: Message | None = None
    try:
        placeholder_message = await update.message.reply_text(
            placeholder_text_escaped,
            parse_mode=constants.ParseMode.MARKDOWN_V2
        )
    except BadRequest as e_bad_placeholder:
        logger.error(
            f"Chat {chat_id}: Failed to send MDV2 placeholder '{placeholder_text_escaped}'. Error: {e_bad_placeholder}. Trying plain.")
        try:
            placeholder_message = await update.message.reply_text(placeholder_text_raw, parse_mode=None)
        except Exception as e_plain_placeholder:
            logger.error(
                f"Chat {chat_id}: Failed to send plain text placeholder '{placeholder_text_raw}'. Error: {e_plain_placeholder}")
            return
    except Exception as e_other_placeholder:
        logger.error(f"Chat {chat_id}: Other error sending placeholder: {e_other_placeholder}")
        return

    if not placeholder_message:
        logger.error(f"Chat {chat_id}: placeholder_message is None after attempting to send. Cannot proceed.")
        return
    # --- END OF MODIFIED PLACEHOLDER INITIALIZATION ---

    if await download_telegram_file(context.bot, photo_file_id, temp_file_path):
        image_bytes_content = None
        actual_mime_type = None
        # Store the actual text of the placeholder that was successfully sent
        initial_placeholder_text_on_telegram = placeholder_message.text
        current_message_text_on_telegram = initial_placeholder_text_on_telegram

        try:
            with open(temp_file_path, "rb") as image_file_bytes_io:
                image_bytes_content = image_file_bytes_io.read()

            pil_image = Image.open(temp_file_path)
            image_format = pil_image.format
            pil_image.close()

            if image_format == "JPEG":
                actual_mime_type = "image/jpeg"
            elif image_format == "PNG":
                actual_mime_type = "image/png"
            elif image_format == "WEBP":
                actual_mime_type = "image/webp"
            else:
                logger.warning(f"Photo format {image_format} for {temp_file_path}. Attempting to convert to PNG.")
                try:
                    pil_image_conv = Image.open(temp_file_path)
                    with io.BytesIO() as img_byte_arr_converted:  # Use with for BytesIO
                        pil_image_conv.save(img_byte_arr_converted, format="PNG")
                        image_bytes_content = img_byte_arr_converted.getvalue()
                    actual_mime_type = "image/png"
                    pil_image_conv.close()
                    logger.info(f"Converted image from {image_format} to PNG for Gemini.")
                except Exception as e_conv:
                    logger.error(f"Failed to convert image from {image_format} to PNG: {e_conv}")
                    err_conv_raw = get_template("unidentified_image_error", user_lang_code,
                                                offending_format=image_format,  # If template uses this
                                                default_val=f"⚠️ Could not process image (format: {image_format}). Try JPEG/PNG.")
                    await placeholder_message.edit_text(escape_markdown_v2(err_conv_raw),
                                                        parse_mode=constants.ParseMode.MARKDOWN_V2)
                    if os.path.exists(temp_file_path): os.remove(temp_file_path)
                    return

            if not image_bytes_content or not actual_mime_type:
                err_prep_raw = get_template("image_data_error", user_lang_code,
                                            default_val="⚠️ Could not prepare image data after download.")
                await placeholder_message.edit_text(escape_markdown_v2(err_prep_raw),
                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)
                if os.path.exists(temp_file_path): os.remove(temp_file_path)
                return

            vision_prompt_raw = get_template("gemini_vision_prompt_general", user_lang_code,
                                             default_val="Please analyze this image and its content (including any text or diagrams). Explain the key concepts, objects, or information present. If it seems to be a problem or question, help me understand it and how to approach it. Act as a study helper.")
            language_name_for_prompt = \
            SUPPORTED_LANGUAGES.get(user_lang_code, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE_CODE]).split(" (")[0]
            system_prompt_for_vision = DEFAULT_SYSTEM_PROMPT_BASE + f"\n\nImportant: Please provide your entire response in {language_name_for_prompt}."

            logger.info(
                f"Calling ask_gemini_vision_stream for image {photo_file_id}, mime: {actual_mime_type} with prompt.")

            accumulated_raw_text = ""
            full_raw_response_for_history = ""  # Still accumulate full response for potential history
            last_edit_time = asyncio.get_event_loop().time()

            # current_message_text_on_telegram is already set to initial_placeholder_text_on_telegram

            async for chunk_raw in ask_gemini_vision_stream(
                    prompt_text=vision_prompt_raw,  # Using the localized prompt
                    image_bytes=image_bytes_content,
                    image_mime_type=actual_mime_type,
                    conversation_history=context.chat_data.get('conversation_history', []),
                    system_prompt=system_prompt_for_vision
            ):
                full_raw_response_for_history += chunk_raw
                accumulated_raw_text += chunk_raw  # This accumulates for the current edit
                current_time = asyncio.get_event_loop().time()

                # Your original conditions for editing
                should_edit_now = (
                        current_message_text_on_telegram == initial_placeholder_text_on_telegram or
                        current_time - last_edit_time >= STREAM_UPDATE_INTERVAL or
                        len(chunk_raw) > 70  # Your original threshold
                )

                if accumulated_raw_text.strip() and should_edit_now:
                    text_for_this_edit_raw = accumulated_raw_text  # This is the current accumulated raw text

                    # Avoid re-editing if content hasn't visually changed
                    # (This is a simplification; a proper check would involve current_bot_message_is_plain state)
                    if text_for_this_edit_raw == current_message_text_on_telegram and \
                            current_message_text_on_telegram != initial_placeholder_text_on_telegram:
                        last_edit_time = current_time
                        continue

                        # Tiered approach for sending stream edits (from your original handle_photo)
                    # This part does not use send_long_message_fallback during the stream, it truncates.
                    try:  # Attempt 1: Raw Gemini output as MarkdownV2 (assuming Gemini gives good MD)
                        # Your code sends raw gemini output directly. For safety, it should be escaped.
                        escaped_attempt_1 = escape_markdown_v2(text_for_this_edit_raw)
                        await context.bot.edit_message_text(
                            escaped_attempt_1[:TELEGRAM_MAX_MESSAGE_LENGTH],
                            chat_id,
                            placeholder_message.message_id,
                            parse_mode=constants.ParseMode.MARKDOWN_V2
                        )
                        current_message_text_on_telegram = escaped_attempt_1[:TELEGRAM_MAX_MESSAGE_LENGTH]
                        logger.debug(f"Chat {chat_id} (Vision Stream): Edit with ESCAPED MDV2 successful.")
                    except BadRequest as e_esc_md_1:
                        if "message is not modified" in str(e_esc_md_1).lower():
                            pass  # Content was already this
                        else:
                            logger.warning(
                                f"Chat {chat_id} (Vision Stream): ESCAPED MDV2 FAILED: {e_esc_md_1}. Trying transformed plain.")
                            try:  # Attempt 2: Transformed plain text
                                transformed_text = transform_markdown_fallback(text_for_this_edit_raw)
                                await context.bot.edit_message_text(
                                    transformed_text[:TELEGRAM_MAX_MESSAGE_LENGTH],
                                    chat_id,
                                    placeholder_message.message_id,
                                    parse_mode=None  # Plain text
                                )
                                current_message_text_on_telegram = transformed_text[:TELEGRAM_MAX_MESSAGE_LENGTH]
                                logger.info(f"Chat {chat_id} (Vision Stream): Edit with TRANSFORMED PLAIN successful.")
                            except BadRequest as e_plain:
                                if "message is not modified" not in str(e_plain).lower():
                                    logger.error(
                                        f"Chat {chat_id} (Vision Stream): TRANSFORMED PLAIN FAILED: {e_plain}. Last resort: original raw plain.")
                                    try:  # Attempt 3: Original Raw Plain (truncated)
                                        await context.bot.edit_message_text(
                                            text_for_this_edit_raw[:TELEGRAM_MAX_MESSAGE_LENGTH],
                                            chat_id,
                                            placeholder_message.message_id,
                                            parse_mode=None
                                        )
                                        current_message_text_on_telegram = text_for_this_edit_raw[
                                                                           :TELEGRAM_MAX_MESSAGE_LENGTH]
                                    except Exception as e_ultra_plain:
                                        logger.error(
                                            f"Chat {chat_id} (Vision Stream): ORIGINAL RAW PLAIN FAILED: {e_ultra_plain}")
                    last_edit_time = current_time
                    await asyncio.sleep(0.05)  # Your original sleep

            logger.info(f"Gemini Vision final response length: {len(full_raw_response_for_history)}")
            # Use full_raw_response_for_history for the final complete text
            final_text_to_send_raw = full_raw_response_for_history.strip()

            if final_text_to_send_raw:
                # Check if the *final complete response* is too long for a single message
                # If so, use send_long_message_fallback which handles splitting and plain text
                final_transformed_check = transform_markdown_fallback(final_text_to_send_raw)
                final_escaped_check = escape_markdown_v2(final_text_to_send_raw)

                if len(final_transformed_check) > TELEGRAM_MAX_MESSAGE_LENGTH:  # Check transformed length for fallback
                    logger.info(
                        f"Chat {chat_id} (Vision Final): Full response too long ({len(final_transformed_check)} transformed chars). Using send_long_message_fallback.")
                    # Update original placeholder to "Done" or similar, as new messages will follow
                    done_raw = get_template("response_complete", user_lang_code, default_val="✅ Analysis complete.")
                    try:
                        if placeholder_message.text != escape_markdown_v2(done_raw):
                            await placeholder_message.edit_text(escape_markdown_v2(done_raw),
                                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
                    except Exception:
                        pass
                    await send_long_message_fallback(update, context, final_text_to_send_raw)

                # If not too long for send_long_message_fallback, try direct edit with tiered strategy
                elif final_text_to_send_raw == current_message_text_on_telegram and \
                        final_text_to_send_raw != initial_placeholder_text_on_telegram:
                    logger.info(
                        f"Chat {chat_id} (Vision): Final text identical to last stream edit. No final edit needed.")
                else:  # Attempt final direct edit with tiered strategy
                    try:  # Attempt 1: Escaped MDV2
                        await placeholder_message.edit_text(final_escaped_check,
                                                            parse_mode=constants.ParseMode.MARKDOWN_V2)
                        logger.info(f"Chat {chat_id} (Vision Final): Final edit with ESCAPED MDV2 successful.")
                    except BadRequest as e_f_esc:
                        if "message is not modified" not in str(e_f_esc).lower():
                            logger.warning(
                                f"Chat {chat_id} (Vision Final): Escaped MDV2 FAILED: {e_f_esc}. Trying transformed plain.")
                            try:  # Attempt 2: Transformed Plain
                                await placeholder_message.edit_text(final_transformed_check, parse_mode=None)
                                logger.info(f"Chat {chat_id} (Vision Final): Transformed Plain successful.")
                            except BadRequest as e_f_plain:
                                if "message is not modified" not in str(e_f_plain).lower():
                                    logger.warning(
                                        f"Chat {chat_id} (Vision Final): Transformed Plain FAILED: {e_f_plain}. Trying raw plain.")
                                    try:  # Attempt 3: Raw Plain
                                        await placeholder_message.edit_text(final_text_to_send_raw, parse_mode=None)
                                        logger.info(f"Chat {chat_id} (Vision Final): Raw Plain successful.")
                                    except Exception as e_f_raw_plain:
                                        logger.error(
                                            f"Chat {chat_id} (Vision Final): All final edit attempts failed. Last error (raw plain): {e_f_raw_plain}")

            elif placeholder_message.text == initial_placeholder_text_on_telegram:  # No response from Gemini Vision
                no_response_text_raw = get_template("gemini_no_vision_response", user_lang_code,
                                                    default_val="🤷 I couldn't get a specific analysis for this image.")
                await placeholder_message.edit_text(escape_markdown_v2(no_response_text_raw),
                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)

        except UnidentifiedImageError:
            logger.error(f"Pillow could not identify image: {temp_file_path}")
            err_raw = get_template("unidentified_image_error", user_lang_code,
                                   default_val="⚠️ Could not identify image format.")
            await placeholder_message.edit_text(escape_markdown_v2(err_raw), parse_mode=constants.ParseMode.MARKDOWN_V2)
        except Exception as e:
            logger.error(f"Error processing photo {photo_file_id} with Vision: {e}", exc_info=True)
            err_raw = get_template("unexpected_image_error", user_lang_code,
                                   default_val="⚠️ Error analyzing image.")
            await placeholder_message.edit_text(escape_markdown_v2(err_raw), parse_mode=constants.ParseMode.MARKDOWN_V2)
        finally:
            if os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path); logger.debug(f"Cleaned up: {temp_file_path}")
                except Exception as e_remove:
                    logger.error(f"Error removing temp file {temp_file_path}: {e_remove}")
    else:  # Download failed
        err_raw = get_template("download_failed_error", user_lang_code,
                               file_name=escape_markdown_v2("the image"),
                               default_val="⚠️ Could not download the image.")
        if placeholder_message:  # Check if placeholder_message was successfully created
            await placeholder_message.edit_text(escape_markdown_v2(err_raw), parse_mode=constants.ParseMode.MARKDOWN_V2)
        else:  # Should ideally not happen if initial placeholder logic is robust
            await update.message.reply_text(escape_markdown_v2(err_raw), parse_mode=constants.ParseMode.MARKDOWN_V2)

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

    user = update.effective_user
    doc = update.message.document
    chat_id = update.effective_chat.id
    message_id_for_uniqueness = update.message.message_id  # For temp filename

    logger.info(
        f"User {user.id} in chat {chat_id} (msg_id: {message_id_for_uniqueness}) sent document: {doc.file_name} (MIME: {doc.mime_type})")

    if not os.path.exists(TEMP_DIR):
        try:
            os.makedirs(TEMP_DIR)
        except OSError as e:
            logger.error(f"Could not create TEMP_DIR '{TEMP_DIR}': {e}")
            await update.message.reply_text(
                escape_markdown_v2("Server error: Cannot create temporary storage."))  # Consider localizing
            return

    # Construct a unique temporary file path
    base_name, ext = os.path.splitext(doc.file_name or f"file_{doc.file_id}")
    temp_file_name = f"{chat_id}_{user.id}_{doc.file_id}_{message_id_for_uniqueness}{ext}"
    temp_file_path = os.path.join(TEMP_DIR, temp_file_name)

    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)  # For localized messages

    placeholder_text_raw = get_template("processing_document", user_lang_code,
                                        file_name=escape_markdown_v2(doc.file_name or "document"))
    placeholder_message: telegram.Message = await update.message.reply_text(
        escape_markdown_v2(placeholder_text_raw),
        parse_mode=constants.ParseMode.MARKDOWN_V2
    )

    if await download_telegram_file(context.bot, doc.file_id, temp_file_path):
        extracted_text = ""
        extraction_successful = False
        try:
            if doc.mime_type == "application/pdf" or doc.file_name.lower().endswith(".pdf"):
                with fitz.open(temp_file_path) as pdf_doc:
                    for page_num, page in enumerate(pdf_doc):
                        extracted_text += page.get_text("text")  # Get plain text
                        if len(extracted_text) > 300000:  # Safety break for extremely large PDFs
                            logger.warning(
                                f"PDF {doc.file_name} text extraction stopped at 300k chars (page {page_num + 1}).")
                            extracted_text += "\n[...Content truncated due to length...]"
                            break
                logger.info(
                    f"Extracted text from PDF '{doc.file_name}': {len(extracted_text)} chars. Preview: '{extracted_text[:100]}...'")
                extraction_successful = True

            elif doc.mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or \
                    doc.file_name.lower().endswith(".docx"):
                docx_doc = DocxDocument(temp_file_path)
                for para in docx_doc.paragraphs:
                    extracted_text += para.text + "\n"
                logger.info(
                    f"Extracted text from DOCX '{doc.file_name}': {len(extracted_text)} chars. Preview: '{extracted_text[:100]}...'")
                extraction_successful = True

            elif doc.mime_type == "text/plain" or doc.file_name.lower().endswith(".txt"):
                with open(temp_file_path, 'r', encoding='utf-8', errors='ignore') as txt_file:
                    extracted_text = txt_file.read()
                logger.info(
                    f"Read text from TXT '{doc.file_name}': {len(extracted_text)} chars. Preview: '{extracted_text[:100]}...'")
                extraction_successful = True

            else:
                unsupported_msg_raw = get_template("unsupported_document_type", user_lang_code,
                                                   file_type=escape_markdown_v2(doc.mime_type or doc.file_name))
                await placeholder_message.edit_text(escape_markdown_v2(unsupported_msg_raw),
                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)
                if os.path.exists(temp_file_path): os.remove(temp_file_path)
                return

            if not extracted_text.strip() and extraction_successful:
                no_text_msg_raw = get_template("no_text_in_document", user_lang_code,
                                               file_name=escape_markdown_v2(doc.file_name))
                await placeholder_message.edit_text(escape_markdown_v2(no_text_msg_raw),
                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)

            elif extracted_text.strip():
                # --- Start Gemini Interaction (logic similar to handle_message) ---
                snippet_info_raw = get_template("extracted_text_snippet_info", user_lang_code,
                                                file_name=escape_markdown_v2(doc.file_name),
                                                chars_count=min(1000, len(extracted_text)))
                await placeholder_message.edit_text(
                    f"{escape_markdown_v2(snippet_info_raw)}\n```\n{escape_markdown_v2(extracted_text[:1000])}\n```\n{escape_markdown_v2(get_template('asking_ai_analysis', user_lang_code))}",
                    parse_mode=constants.ParseMode.MARKDOWN_V2
                )

                conversation_history = context.chat_data.get('conversation_history', [])
                language_name_for_prompt = \
                SUPPORTED_LANGUAGES.get(user_lang_code, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE_CODE]).split(" (")[0]
                system_prompt = DEFAULT_SYSTEM_PROMPT_BASE + f"\n\nImportant: Please provide your entire response in {language_name_for_prompt}."

                # Prepare the question for Gemini
                gemini_question = (
                    f"The user has uploaded a document named '{escape_markdown_v2(doc.file_name)}'. "
                    f"Here is the text content extracted from it. Please act as an AI Study Helper: analyze this text, "
                    f"explain key concepts, summarize it, or answer potential questions a student might have about it. "
                    f"Prioritize correctness and clarity in your explanation.\n\n"
                    f"Extracted Text:\n---\n{extracted_text}\n---"
                )
                # Truncate gemini_question if too long for the prompt itself, though extracted_text is the main part
                # Max input tokens for gemini-1.5-flash is large, but good to be mindful.
                # For this example, we send the full extracted_text.

                accumulated_raw_text = ""
                full_raw_response_for_history = ""
                last_edit_time = asyncio.get_event_loop().time()
                initial_placeholder_text_for_gemini = placeholder_message.text  # The "Extracted text..." message
                current_message_text_on_telegram = placeholder_message.text  # Tracks current displayed content
                current_content_is_transformed_plain = False  # Tracks if current_message_text_on_telegram is plain

                logger.debug(f"Chat {chat_id}: Calling ask_gemini_stream for document '{doc.file_name}' content.")
                async for chunk_raw in ask_gemini_stream(
                        current_question=gemini_question,
                        conversation_history=conversation_history,  # Pass relevant history
                        system_prompt=system_prompt
                ):
                    full_raw_response_for_history += chunk_raw
                    accumulated_raw_text += chunk_raw
                    current_time = asyncio.get_event_loop().time()
                    should_edit_now = (
                            current_message_text_on_telegram == initial_placeholder_text_for_gemini or
                            current_time - last_edit_time >= STREAM_UPDATE_INTERVAL or
                            len(chunk_raw) > 70
                    )

                    if accumulated_raw_text.strip() and should_edit_now:
                        text_for_this_edit = accumulated_raw_text
                        if text_for_this_edit == current_message_text_on_telegram and \
                                current_message_text_on_telegram != initial_placeholder_text_for_gemini:
                            last_edit_time = current_time
                            continue

                        try:
                            await context.bot.edit_message_text(
                                text_for_this_edit[:TELEGRAM_MAX_MESSAGE_LENGTH],
                                chat_id,
                                placeholder_message.message_id,
                                parse_mode=constants.ParseMode.MARKDOWN_V2
                            )
                            current_message_text_on_telegram = text_for_this_edit[:TELEGRAM_MAX_MESSAGE_LENGTH]
                            current_content_is_transformed_plain = False
                            logger.debug(f"Chat {chat_id} (Doc Stream): Edit with RAW GEMINI MDV2 successful.")
                        except BadRequest as e_md:
                            if "Message is too long" in str(e_md):
                                logger.info(
                                    f"Chat {chat_id} (Doc Stream): Text too long for edit. Sending part via fallback.")
                                await send_long_message_fallback(update, text_for_this_edit,
                                                                 is_escaped=False)  # Send current accumulated
                                accumulated_raw_text = ""  # Reset accumulated
                                # Placeholder message is now multiple messages, edit the last one or send new.
                                # For simplicity, send a new "continuing" message for the next part of the stream.
                                # The original placeholder_message is now "orphaned" if content was split.
                                placeholder_message = await update.message.reply_text(  # New placeholder
                                    escape_markdown_v2(get_template("continuing_analysis", user_lang_code)),
                                    parse_mode=constants.ParseMode.MARKDOWN_V2
                                )
                                initial_placeholder_text_for_gemini = placeholder_message.text
                                current_message_text_on_telegram = placeholder_message.text
                                current_content_is_transformed_plain = False
                            elif "message is not modified" in str(e_md).lower():
                                logger.debug(f"Chat {chat_id} (Doc Stream): RAW MDV2 message not modified.")
                            else:
                                logger.warning(
                                    f"Chat {chat_id} (Doc Stream): RAW GEMINI MDV2 FAILED: {e_md}. Preview: '{text_for_this_edit[:70]}'. Trying transformed plain.")
                                transformed_text = transform_markdown_fallback(text_for_this_edit)
                                try:
                                    if transformed_text != current_message_text_on_telegram or not current_content_is_transformed_plain:
                                        await context.bot.edit_message_text(
                                            transformed_text[:TELEGRAM_MAX_MESSAGE_LENGTH],
                                            chat_id,
                                            placeholder_message.message_id,
                                            parse_mode=None
                                        )
                                        current_message_text_on_telegram = transformed_text[
                                                                           :TELEGRAM_MAX_MESSAGE_LENGTH]
                                        current_content_is_transformed_plain = True
                                        logger.info(
                                            f"Chat {chat_id} (Doc Stream): Edit with TRANSFORMED PLAIN successful.")
                                except BadRequest as e_plain:
                                    if "message is not modified" not in str(e_plain).lower():
                                        logger.error(
                                            f"Chat {chat_id} (Doc Stream): TRANSFORMED PLAIN FAILED: {e_plain}")
                        last_edit_time = current_time
                        await asyncio.sleep(0.05)

                # --- Final Edit Attempt for Document Content ---
                logger.info(
                    f"Chat {chat_id} (Doc): Gemini stream finished. Full raw response length: {len(full_raw_response_for_history)}.")
                final_text_raw = accumulated_raw_text.strip()  # What's left from the stream for the current placeholder_message

                done_message_raw = get_template("analysis_complete", user_lang_code)  # e.g., "✅ Analysis complete."

                if final_text_raw:  # If there's remaining text for the current placeholder_message
                    # Check if content is same as already displayed
                    is_final_same_as_current_md = (
                                final_text_raw == current_message_text_on_telegram and not current_content_is_transformed_plain and current_message_text_on_telegram != initial_placeholder_text_for_gemini)
                    is_final_same_as_current_plain = (transform_markdown_fallback(
                        final_text_raw) == current_message_text_on_telegram and current_content_is_transformed_plain and current_message_text_on_telegram != initial_placeholder_text_for_gemini)

                    if is_final_same_as_current_md or is_final_same_as_current_plain:
                        logger.info(
                            f"Chat {chat_id} (Doc Final): Final text for current message segment is identical. No final edit for this segment.")
                        # If the placeholder_message was one of the "...continuing..." ones, update it to "Done"
                        if initial_placeholder_text_for_gemini != placeholder_message.text and (
                                "continuing" in initial_placeholder_text_for_gemini.lower() or "processing" in initial_placeholder_text_for_gemini.lower()):
                            try:
                                await placeholder_message.edit_text(escape_markdown_v2(done_message_raw),
                                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)
                            except BadRequest:
                                pass  # Ignore if not modified
                    else:
                        try:  # Attempt 1: Final raw MDV2
                            await context.bot.edit_message_text(final_text_raw, chat_id, placeholder_message.message_id,
                                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
                            logger.info(f"Chat {chat_id} (Doc Final): Edit with RAW MDV2 successful.")
                        except BadRequest as e_f_raw_md:
                            if "Message is too long" in str(e_f_raw_md):
                                logger.info(
                                    f"Chat {chat_id} (Doc Final): Final segment too long. Sending via fallback.")
                                await send_long_message_fallback(update, final_text_raw, is_escaped=False)
                                # Original placeholder_message is now "orphaned" or was a "...continuing..." one
                                # We can try to edit it to a "Done" message if it wasn't the primary display
                                if placeholder_message.text == initial_placeholder_text_for_gemini or "...continuing" in placeholder_message.text:
                                    try:
                                        await placeholder_message.edit_text(escape_markdown_v2(done_message_raw),
                                                                            parse_mode=constants.ParseMode.MARKDOWN_V2)
                                    except BadRequest:
                                        pass  # Ignore
                            elif "message is not modified" not in str(e_f_raw_md).lower():
                                logger.warning(
                                    f"Chat {chat_id} (Doc Final): RAW MDV2 FAILED: {e_f_raw_md}. Trying transformed plain.")
                                final_transformed = transform_markdown_fallback(final_text_raw)
                                try:  # Attempt 2: Final transformed plain
                                    await context.bot.edit_message_text(final_transformed, chat_id,
                                                                        placeholder_message.message_id, parse_mode=None)
                                    logger.info(f"Chat {chat_id} (Doc Final): Edit with TRANSFORMED PLAIN successful.")
                                except BadRequest as e_f_plain:
                                    if "message is not modified" not in str(e_f_plain).lower():
                                        logger.error(
                                            f"Chat {chat_id} (Doc Final): All final edit attempts failed. Last error (plain): {e_f_plain}")

                elif (
                        placeholder_message.text == initial_placeholder_text_for_gemini or "...continuing" in placeholder_message.text) and full_raw_response_for_history.strip():
                    # Case: No final_text_raw (all sent via fallback or last chunk was empty) but got a response
                    try:
                        await placeholder_message.edit_text(escape_markdown_v2(done_message_raw),
                                                            parse_mode=constants.ParseMode.MARKDOWN_V2)
                    except BadRequest:
                        pass  # Ignore if not modified

                elif placeholder_message.text == initial_placeholder_text_for_gemini and not full_raw_response_for_history.strip():
                    # Case: Original placeholder, and Gemini produced absolutely nothing
                    no_gemini_resp_raw = get_template("gemini_no_response_document", user_lang_code)
                    await placeholder_message.edit_text(escape_markdown_v2(no_gemini_resp_raw),
                                                        parse_mode=constants.ParseMode.MARKDOWN_V2)

                # Save to history
                if full_raw_response_for_history.strip() and not any(
                        err_msg in full_raw_response_for_history.lower() for err_msg in
                        ["sorry", "i can't", "unable to", "blocked", "guidelines"]):
                    # Use a generic prompt for history for documents, as extracted_text can be huge
                    history_user_prompt = f"User uploaded document '{doc.file_name}' for analysis."
                    conversation_history.append({'role': 'user', 'parts': [{'text': history_user_prompt}]})
                    conversation_history.append(
                        {'role': 'model', 'parts': [{'text': full_raw_response_for_history}]})  # Save full response
                    context.chat_data['conversation_history'] = conversation_history[-MAX_CONVERSATION_TURNS * 2:]
                    logger.debug(
                        f"Chat {chat_id} (Doc): Conversation history updated. Length: {len(context.chat_data['conversation_history'])}.")
                else:
                    logger.warning(
                        f"Chat {chat_id} (Doc): Gemini response for document was empty or refusal-like. Not saving to history. Response: '{full_raw_response_for_history[:100]}...'")
            # --- End Gemini Interaction ---

        except Exception as e_process:  # Catch errors during PDF/DOCX parsing itself
            logger.error(f"Error parsing or processing document '{doc.file_name}': {e_process}", exc_info=True)
            error_msg_raw = get_template("document_processing_error", user_lang_code,
                                         file_name=escape_markdown_v2(doc.file_name))
            await placeholder_message.edit_text(escape_markdown_v2(error_msg_raw),
                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
        finally:
            if os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                    logger.debug(f"Cleaned up temporary document: {temp_file_path}")
                except Exception as e_remove:
                    logger.error(f"Error removing temporary document {temp_file_path}: {e_remove}")
    else:  # Download failed
        download_fail_raw = get_template("download_failed_error", user_lang_code,
                                         file_name=escape_markdown_v2(doc.file_name or "document"))
        await placeholder_message.edit_text(escape_markdown_v2(download_fail_raw),
                                            parse_mode=constants.ParseMode.MARKDOWN_V2)


def escape_markdown_v2(text: str) -> str:
    """
    Escapes text for Telegram MarkdownV2.
    Stricter version: escapes most special characters, including '-', '#', '.', '!', etc.
    It deliberately does NOT escape '*' and '_' to allow for Gemini-produced bold/italic.
    """
    if not isinstance(text, str):
        text = str(text)
    # Characters to escape (excluding * and _ for bold/italic)
    # Full list: _ * [ ] ( ) ~ ` > # + - = | { } . ! \
    # We escape:   [ ] ( ) ~ ` > # + - = | { } . ! \
    escape_chars_pattern = re.compile(r'([_*\[\]()~`>#+\-=|{}.!\\])')  # Added _ back
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
    """
    if not text:
        return ""

    _logger = logger
    _logger.debug(f"Transforming text for fallback. Original starts: '{text[:100].replace(chr(10), ' ')}...'")

    transformed_text = text

    # 1. Normalize line endings and remove leading/trailing whitespace from the whole text
    transformed_text = transformed_text.replace('\r\n', '\n').strip()

    # 2. Handle code blocks (simple removal of backticks, keep content)
    transformed_text = re.sub(r'```(?:[a-zA-Z0-9_.-]*)?\n(.*?)\n```', r'\1', transformed_text,
                              flags=re.DOTALL | re.MULTILINE)
    transformed_text = re.sub(r'```(.*?)```', r'\1', transformed_text, flags=re.DOTALL)

    # 3. Handle inline code `code` (simple removal of backticks)
    transformed_text = re.sub(r'`(.*?)`', r'\1', transformed_text)

    # 4. Handle bold and italics
    transformed_text = re.sub(r'\*\*(.*?)\*\*', r'"\1"', transformed_text)  # **bold** to "bold"
    transformed_text = re.sub(r'__(.*?)__', r'"\1"', transformed_text)  # __underline__ to "quoted"
    transformed_text = re.sub(r'\*(.*?)\*', r'\1', transformed_text)  # *italic* to plain
    transformed_text = re.sub(r'_(.*?)_', r'\1', transformed_text)  # _italic_ to plain

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

        item_content = ""  # To store the main content of the list item

        if bullet_match:
            indentation, original_content = bullet_match.group(1), bullet_match.group(2).strip()
            if not original_content:
                if in_list_context: processed_lines.append(indentation.rstrip('\n'))
                continue

            item_content = original_content
            is_new_list_context = True
            if processed_lines:
                last_meaningful_line = next(
                    (processed_lines[j].strip() for j in range(len(processed_lines) - 1, -1, -1) if
                     processed_lines[j].strip()), "")
                if re.match(r"^\s*\d+\.\s+", last_meaningful_line): is_new_list_context = False
            list_item_counter = 1 if is_new_list_context else list_item_counter + 1

            # MODIFICATION HERE: Check and add space after "Title:"
            item_content_final = re.sub(r'^("[^"]+:")(\S)', r'\1 \2', item_content)

            processed_lines.append(f"{indentation}{list_item_counter}. {item_content_final}")
            in_list_context = True

        elif numbered_list_match:
            indentation, number_str, original_content = numbered_list_match.group(1), numbered_list_match.group(
                2), numbered_list_match.group(3).strip()
            if not original_content:
                if in_list_context: processed_lines.append(indentation.rstrip('\n'))
                continue

            item_content = original_content
            is_new_list_context = True
            if processed_lines:
                last_meaningful_line = next(
                    (processed_lines[j].strip() for j in range(len(processed_lines) - 1, -1, -1) if
                     processed_lines[j].strip()), "")
                if re.match(r"^\s*\d+\.\s+", last_meaningful_line): is_new_list_context = False

            current_item_number = 0
            if is_new_list_context:
                try:
                    current_item_number = int(number_str)
                except ValueError:
                    current_item_number = 1
                list_item_counter = current_item_number  # Sync counter
            else:
                list_item_counter += 1
                current_item_number = list_item_counter  # Use our consistent counter

            # MODIFICATION HERE: Check and add space after "Title:"
            item_content_final = re.sub(r'^("[^"]+:")(\S)', r'\1 \2', item_content)

            processed_lines.append(f"{indentation}{current_item_number}. {item_content_final}")
            in_list_context = True
        else:
            if stripped_line:
                processed_lines.append(line)
                in_list_context = False
            else:
                processed_lines.append(line)

    transformed_text_final = "\n".join(processed_lines)

    # 8. Final cleanup:
    transformed_text_final = re.sub(r'\n\s*\n', '\n\n', transformed_text_final)  # Consolidate multiple blank lines

    _logger.debug(f"Transformed text fallback result starts: '{transformed_text_final[:100].replace(chr(10), ' ')}...'")
    return transformed_text_final.strip()


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.critical(f"--- handle_message entered for chat {update.effective_chat.id} ---")
    if not update.message or not update.message.text:
        logger.warning(
            f"Chat {update.effective_chat.id if update.effective_chat else '?'}: handle_message with no message/text.")
        return

    user, message_text, chat_id = update.effective_user, update.message.text, update.effective_chat.id
    logger.info(f"Chat {chat_id}: User {user.id} ('{user.username or user.first_name}'): '{message_text[:100]}...'")

    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)
    lang_name_prompt = SUPPORTED_LANGUAGES.get(user_lang_code, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE_CODE]).split(" (")[
        0]
    system_prompt = DEFAULT_SYSTEM_PROMPT_BASE + f"\n\nImportant: Provide response in {lang_name_prompt}."
    conversation_history = context.chat_data.get('conversation_history', [])

    # --- Placeholders from localization (ensure these keys exist in your get_template) ---
    thinking_raw = get_template("thinking", user_lang_code, default_val="🧠 Thinking...")
    continue_raw = get_template("continuing_response", user_lang_code, default_val="...continuing response...")
    done_raw = get_template("response_complete", user_lang_code, default_val="✅ Done.")
    no_response_raw = get_template("gemini_no_response_text", user_lang_code, default_val="🤷 No response generated.")
    response_continued_below_raw = get_template("response_continued_below", user_lang_code,
                                                default_val="...(see new messages below)...")

    initial_placeholder_text_escaped = escape_markdown_v2(thinking_raw)
    current_bot_message: Message | None = None
    try:
        current_bot_message = await update.message.reply_text(initial_placeholder_text_escaped,
                                                              parse_mode=constants.ParseMode.MARKDOWN_V2)
        logger.debug(f"Chat {chat_id}: Sent '{thinking_raw}'. Msg ID: {current_bot_message.message_id}")
    except Exception as e:
        logger.error(f"Chat {chat_id}: Failed to send '{thinking_raw}': {e}", exc_info=True)
        err_init_raw = get_template("error_initiating_response", user_lang_code, default_val="⚠️ Error starting.")
        try:
            await update.message.reply_text(escape_markdown_v2(err_init_raw),
                                            parse_mode=constants.ParseMode.MARKDOWN_V2)
        except Exception:
            pass
        return

    active_placeholder_text_escaped = initial_placeholder_text_escaped  # Tracks text of current_bot_message if it's a placeholder
    accumulated_raw_text_for_edit = ""
    full_raw_response_for_history = ""
    last_edit_time = asyncio.get_event_loop().time()
    current_bot_message_is_plain = False  # Assume MDV2 initially for the placeholder

    try:
        logger.debug(f"Chat {chat_id}: Calling ask_gemini_stream.")
        async for chunk_raw in ask_gemini_stream(message_text, conversation_history, system_prompt):
            full_raw_response_for_history += chunk_raw
            accumulated_raw_text_for_edit += chunk_raw
            current_time = asyncio.get_event_loop().time()

            is_active_placeholder = current_bot_message and current_bot_message.text == active_placeholder_text_escaped
            time_to_update = current_time - last_edit_time >= STREAM_UPDATE_INTERVAL
            significant_chunk = len(chunk_raw) > 70

            should_edit_now = (
                    current_bot_message and accumulated_raw_text_for_edit.strip() and
                    (is_active_placeholder or time_to_update or significant_chunk)
            )

            if should_edit_now:
                raw_text_attempt = accumulated_raw_text_for_edit

                if not is_active_placeholder:
                    if current_bot_message_is_plain:
                        if transform_markdown_fallback(raw_text_attempt) == current_bot_message.text:
                            logger.debug(f"Chat {chat_id}: Stream (Plain): Content same; skipping.")
                            last_edit_time = current_time;
                            continue
                    else:
                        if escape_markdown_v2(raw_text_attempt) == current_bot_message.text:
                            logger.debug(f"Chat {chat_id}: Stream (MDV2): Content same; skipping.")
                            last_edit_time = current_time;
                            continue

                transformed_check = transform_markdown_fallback(raw_text_attempt)

                if len(transformed_check) > TELEGRAM_MAX_MESSAGE_LENGTH:
                    logger.info(
                        f"Chat {chat_id}: Stream: Transformed text long ({len(transformed_check)}). Offloading.")
                    if current_bot_message:
                        try:
                            continued_below_esc = escape_markdown_v2(response_continued_below_raw)
                            if current_bot_message.text != continued_below_esc:
                                await context.bot.edit_message_text(continued_below_esc, chat_id,
                                                                    current_bot_message.message_id,
                                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)
                        except Exception as e_cont_edit:
                            logger.warning(f"Chat {chat_id}: Fail edit 'continued below': {e_cont_edit}")

                    await send_long_message_fallback(update, context, raw_text_attempt)
                    accumulated_raw_text_for_edit = ""

                    try:
                        continue_placeholder_esc = escape_markdown_v2(continue_raw)
                        current_bot_message = await update.message.reply_text(continue_placeholder_esc,
                                                                              parse_mode=constants.ParseMode.MARKDOWN_V2)
                        active_placeholder_text_escaped = continue_placeholder_esc
                        current_bot_message_is_plain = False
                        logger.debug(
                            f"Chat {chat_id}: Sent new placeholder '{continue_raw}'. Msg ID: {current_bot_message.message_id}")
                    except Exception as e_new_ph:
                        logger.error(
                            f"Chat {chat_id}: Fail send new '{continue_raw}' placeholder: {e_new_ph}. Halting edits.")
                        current_bot_message = None;
                        break
                else:
                    text_to_edit_this_round, parse_mode_this_round, edit_made_plain = "", None, False
                    if current_bot_message_is_plain:
                        text_to_edit_this_round = transform_markdown_fallback(raw_text_attempt)
                        parse_mode_this_round, edit_made_plain = None, True
                        logger.debug(f"Chat {chat_id}: Stream: Current is plain, attempting transformed plain edit.")
                    else:
                        text_to_edit_this_round = escape_markdown_v2(raw_text_attempt)
                        parse_mode_this_round, edit_made_plain = constants.ParseMode.MARKDOWN_V2, False
                        logger.debug(f"Chat {chat_id}: Stream: Attempting Escaped MDV2 edit.")

                    try:
                        if len(text_to_edit_this_round) > TELEGRAM_MAX_MESSAGE_LENGTH:
                            text_to_edit_this_round = text_to_edit_this_round[:TELEGRAM_MAX_MESSAGE_LENGTH]
                        await context.bot.edit_message_text(text_to_edit_this_round, chat_id,
                                                            current_bot_message.message_id,
                                                            parse_mode=parse_mode_this_round)
                        current_bot_message_is_plain = edit_made_plain
                        logger.info(
                            f"Chat {chat_id}: Stream edit successful (Mode: {'PLAIN' if current_bot_message_is_plain else 'MDV2'}).")
                    except BadRequest as e_edit:
                        if "message is not modified" in str(e_edit).lower():
                            logger.debug(
                                f"Chat {chat_id}: Stream edit: Not modified (Mode attempted: {'PLAIN' if edit_made_plain else 'MDV2'}).")
                        elif not current_bot_message_is_plain:
                            logger.warning(
                                f"Chat {chat_id}: Stream edit (Escaped MDV2) failed: {e_edit}. Trying TRANSFORMED PLAIN fallback.")
                            transformed_fallback = transform_markdown_fallback(raw_text_attempt)
                            plain_fallback = transformed_fallback if len(
                                transformed_fallback) <= TELEGRAM_MAX_MESSAGE_LENGTH else raw_text_attempt[
                                                                                          :TELEGRAM_MAX_MESSAGE_LENGTH]
                            try:
                                if plain_fallback != current_bot_message.text:
                                    await context.bot.edit_message_text(plain_fallback, chat_id,
                                                                        current_bot_message.message_id, parse_mode=None)
                                current_bot_message_is_plain = True
                                logger.info(f"Chat {chat_id}: Stream edit (Fallback to TRANSFORMED PLAIN) successful.")
                            except Exception as e_ultra:
                                logger.error(
                                    f"Chat {chat_id}: Stream edit (Fallback to TRANSFORMED PLAIN) ALSO FAILED: {e_ultra}")
                        else:
                            logger.error(f"Chat {chat_id}: Stream edit (TRANSFORMED PLAIN attempt) FAILED: {e_edit}")
                last_edit_time = current_time
                await asyncio.sleep(0.05)

        # --- End of Gemini Stream ---
        logger.debug(f"COMPLETE RAW GEMINI RESPONSE: >>>{full_raw_response_for_history}<<<")
        logger.debug(f"Chat {chat_id}: Stream finished. Full raw history len: {len(full_raw_response_for_history)}")
        final_raw_text_segment = accumulated_raw_text_for_edit.strip()

        if not current_bot_message:
            logger.error(f"Chat {chat_id}: No current_bot_message at end of stream.")
        elif final_raw_text_segment:
            text_final, parse_final = "", None
            if current_bot_message_is_plain:
                logger.info(f"Chat {chat_id}: Final segment: Opting for TRANSFORMED PLAIN.")
                transformed_final = transform_markdown_fallback(final_raw_text_segment)
                text_final = transformed_final if len(
                    transformed_final) <= TELEGRAM_MAX_MESSAGE_LENGTH else final_raw_text_segment[
                                                                           :TELEGRAM_MAX_MESSAGE_LENGTH]
                parse_final = None
            else:
                escaped_final = escape_markdown_v2(final_raw_text_segment)
                if len(escaped_final) > TELEGRAM_MAX_MESSAGE_LENGTH:
                    logger.info(f"Chat {chat_id}: Final segment (escaped) too long ({len(escaped_final)}). Offloading.")
                    if current_bot_message.text != escape_markdown_v2(done_raw):
                        try:
                            await context.bot.edit_message_text(escape_markdown_v2(done_raw), chat_id,
                                                                current_bot_message.message_id,
                                                                parse_mode=constants.ParseMode.MARKDOWN_V2)
                        except Exception:
                            pass
                    await send_long_message_fallback(update, context, final_raw_text_segment)
                    text_final = ""  # Handled by fallback
                else:
                    text_final, parse_final = escaped_final, constants.ParseMode.MARKDOWN_V2

            if text_final:
                is_final_placeholder = current_bot_message.text == active_placeholder_text_escaped
                visually_same = False
                if not is_final_placeholder:
                    if parse_final is None:
                        visually_same = (text_final == current_bot_message.text)
                    else:
                        visually_same = (text_final == current_bot_message.text and not current_bot_message_is_plain)

                if visually_same:
                    logger.info(f"Chat {chat_id}: Final segment visually identical. No final edit.")
                else:
                    try:
                        await context.bot.edit_message_text(text_final, chat_id, current_bot_message.message_id,
                                                            parse_mode=parse_final)
                        logger.info(
                            f"Chat {chat_id}: Final edit (Mode: {'PLAIN' if parse_final is None else 'MDV2'}) successful.")
                    except BadRequest as e_f_edit:
                        if "message is not modified" not in str(e_f_edit).lower():
                            logger.warning(
                                f"Chat {chat_id}: Final edit (Mode: {'PLAIN' if parse_final is None else 'MDV2'}) failed: {e_f_edit}.")
                            if parse_final == constants.ParseMode.MARKDOWN_V2:  # MDV2 failed, try plain
                                transformed_ult = transform_markdown_fallback(final_raw_text_segment)
                                plain_ult = transformed_ult if len(
                                    transformed_ult) <= TELEGRAM_MAX_MESSAGE_LENGTH else final_raw_text_segment[
                                                                                         :TELEGRAM_MAX_MESSAGE_LENGTH]
                                try:
                                    if plain_ult != current_bot_message.text:
                                        await context.bot.edit_message_text(plain_ult, chat_id,
                                                                            current_bot_message.message_id,
                                                                            parse_mode=None)
                                    logger.info(f"Chat {chat_id}: Final edit (PLAIN fallback) successful.")
                                except Exception as e_f_pf:
                                    logger.error(f"Chat {chat_id}: Final plain fallback edit FAILED: {e_f_pf}")
        elif current_bot_message and current_bot_message.text == active_placeholder_text_escaped:
            final_placeholder = escape_markdown_v2(
                done_raw if full_raw_response_for_history.strip() else no_response_raw)
            if current_bot_message.text != final_placeholder:
                try:
                    await context.bot.edit_message_text(final_placeholder, chat_id, current_bot_message.message_id,
                                                        parse_mode=constants.ParseMode.MARKDOWN_V2)
                except Exception as e_f_ph:
                    logger.warning(f"Chat {chat_id}: Failed edit final placeholder: {e_f_ph}")

        # --- Save to Conversation History ---
        if full_raw_response_for_history.strip() and not any(
                kw in full_raw_response_for_history.lower() for kw in
                ["i can't", "sorry", "unable to", "guidelines", "blocked"]):
            conversation_history.append({'role': 'user', 'parts': [{'text': message_text}]})
            conversation_history.append({'role': 'model', 'parts': [{'text': full_raw_response_for_history}]})
            context.chat_data['conversation_history'] = conversation_history[-(MAX_CONVERSATION_TURNS * 2):]
            logger.debug(f"Chat {chat_id}: History updated. Len: {len(context.chat_data['conversation_history'])}.")
        else:
            logger.warning(
                f"Chat {chat_id}: AI response empty/refusal. Not saved. Preview: '{full_raw_response_for_history[:100].replace(chr(10), ' ')}...'")

    except Exception as e_outer:
        logger.error(f"Chat {chat_id}: Unhandled error in handle_message (after placeholder): {e_outer}", exc_info=True)
        err_proc_raw = get_template("unexpected_error_processing", user_lang_code, default_val="⚠️ Unexpected error.")
        err_proc_esc = escape_markdown_v2(err_proc_raw)
        try:
            if current_bot_message and current_bot_message.text != err_proc_esc:
                await context.bot.edit_message_text(err_proc_esc, chat_id, current_bot_message.message_id,
                                                    parse_mode=constants.ParseMode.MARKDOWN_V2)
            elif not current_bot_message:
                await update.message.reply_text(err_proc_esc, parse_mode=constants.ParseMode.MARKDOWN_V2)
        except Exception:
            pass
    finally:
        logger.critical(f"--- handle_message finished for chat {chat_id} ---")


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


def get_application_with_persistence(persistence: BasePersistence) -> Application:
    logger.info("Building Telegram application with persistence...")  # Log from bot.telegram_bot

    # --- Temporarily remove custom HTTPXRequest for diagnostics ---
    # httpx_request = HTTPXRequest(http_version="1.1")
    # application = Application.builder().token(TELEGRAM_BOT_TOKEN).persistence(persistence).request(
    #     httpx_request).build()

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).persistence(persistence).build()
    logger.info(
        f"Application built. Token used (last 6 chars): ...{TELEGRAM_BOT_TOKEN[-6:] if TELEGRAM_BOT_TOKEN and len(TELEGRAM_BOT_TOKEN) > 5 else 'TOKEN_TOO_SHORT_OR_NONE'}")

    # --- Add the all_updates_logger as the VERY FIRST handler (group -1) ---
    # This ensures it sees updates before any other handler, even if others consume the update.
    # Using MessageHandler with filters.ALL to catch everything.
    application.add_handler(MessageHandler(filters.ALL, all_updates_logger), group=-1)
    logger.info("Raw update logger (all_updates_logger) registered with group -1.")

    # Regular handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("language", language_command))
    application.add_handler(CallbackQueryHandler(language_set_callback_handler, pattern=r"^set_lang_"))
    application.add_handler(CallbackQueryHandler(language_page_callback_handler, pattern=r"^lang_page_"))
    application.add_handler(CallbackQueryHandler(button_callback_handler))  # General catch-all for other buttons
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    application.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    logger.info("Application object and handlers registered in get_application_with_persistence.")  # Modified log
    return application

# --- END OF FILE telegram_bot.py ---