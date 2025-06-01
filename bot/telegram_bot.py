# --- START OF FILE telegram_bot.py ---
import os
import logging
import asyncio
import re
from collections import OrderedDict

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
from .gemini_utils import ask_gemini_stream

logger = logging.getLogger(__name__)  # This will be 'bot.telegram_bot'

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
    """You are a helpful AI Study Helper. Please use Markdown formatting to make your explanations clear, structured, and visually appealing.
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


def escape_markdown_v2(text: str) -> str:
    if not isinstance(text, str):
        text = str(text)
    escape_chars_pattern = re.compile(r'([_*\[\]()~`>#+\-=|{}.!\\])')
    return escape_chars_pattern.sub(r'\\\1', text)


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
    if not text: return ""
    logger.debug(f"Transforming text. Original starts: '{text[:70].replace(chr(10), ' ')}...'")
    transformed_text = re.sub(r'\*\*(.*?)\*\*', r'"\1"', text)  # Simple bold to quotes
    # Convert *- style bullets to 1. 2. 3. style lists
    lines = transformed_text.splitlines()
    processed_lines = []
    list_item_counter = 0  # 0 means not in a list, >0 means current list item number
    for i, line in enumerate(lines):
        bullet_match = re.match(r"^(\s*)([*-])\s+(.*)", line)  # Matches * or -
        if bullet_match:
            if list_item_counter == 0: list_item_counter = 1  # Start of a new list
            indentation, content = bullet_match.group(1), bullet_match.group(3)
            processed_lines.append(f"{indentation}{list_item_counter}. {content}")
            list_item_counter += 1
        else:
            # If the line is not a bullet, reset the counter if we were in a list
            if list_item_counter > 0: list_item_counter = 0
            processed_lines.append(line)
    transformed_text = "\n".join(processed_lines)
    logger.debug(f"Transformed text result starts: '{transformed_text[:70].replace(chr(10), ' ')}...'")
    return transformed_text


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.critical(f"--- handle_message entered for chat {update.effective_chat.id} ---")
    user = update.effective_user
    message_text = update.message.text
    chat_id = update.effective_chat.id
    logger.info(
        f"Chat {chat_id}: Received message from user {user.id} ({user.username or user.first_name}): '{message_text[:100]}...'")

    user_lang_code = context.user_data.get('selected_language', DEFAULT_LANGUAGE_CODE)
    language_name_for_prompt = \
        SUPPORTED_LANGUAGES.get(user_lang_code, SUPPORTED_LANGUAGES[DEFAULT_LANGUAGE_CODE]).split(" (")[0]
    current_system_prompt = DEFAULT_SYSTEM_PROMPT_BASE
    current_system_prompt += f"\n\nImportant: Please provide your entire response in {language_name_for_prompt}."
    logger.debug(f"Chat {chat_id}: Using system prompt for Gemini (last 100 chars): ...{current_system_prompt[-100:]}")

    conversation_history = context.chat_data.get('conversation_history', [])
    initial_placeholder_escaped = escape_markdown_v2("🧠 Thinking...")
    current_bot_message = None
    try:
        logger.debug(f"Chat {chat_id}: Attempting to send 'Thinking...' placeholder.")
        current_bot_message = await update.message.reply_text(
            initial_placeholder_escaped,
            parse_mode=constants.ParseMode.MARKDOWN_V2
        )
        logger.debug(f"Chat {chat_id}: 'Thinking...' placeholder sent. Message ID: {current_bot_message.message_id}")
    except Exception as e_placeholder:
        logger.error(f"Chat {chat_id}: Failed to send 'Thinking...' placeholder: {e_placeholder}", exc_info=True)
        try:
            await update.message.reply_text(
                escape_markdown_v2("⚠️ Error: Could not initiate response processing. Please try again."),
                parse_mode=constants.ParseMode.MARKDOWN_V2)
        except Exception as e_reply_fail:
            logger.error(
                f"Chat {chat_id}: Failed to send error message to user after placeholder failure: {e_reply_fail}",
                exc_info=True)
        return

    accumulated_raw_text = ""
    full_raw_response_for_history = ""
    last_edit_time = asyncio.get_event_loop().time()
    current_content_is_transformed_plain = False

    try:
        logger.debug(f"Chat {chat_id}: About to call ask_gemini_stream.")
        async for chunk_raw in ask_gemini_stream(message_text, conversation_history, current_system_prompt):
            full_raw_response_for_history += chunk_raw
            accumulated_raw_text += chunk_raw
            current_time = asyncio.get_event_loop().time()
            should_edit_now = (
                    current_bot_message.text == initial_placeholder_escaped or
                    current_time - last_edit_time >= STREAM_UPDATE_INTERVAL or
                    len(chunk_raw) > 50
            )

            if accumulated_raw_text.strip() and should_edit_now:
                text_for_this_edit = accumulated_raw_text
                if text_for_this_edit == current_bot_message.text and current_bot_message.text != initial_placeholder_escaped:
                    logger.debug(f"Chat {chat_id}: Stream content for edit same as current; skipping.")
                    last_edit_time = current_time
                    continue
                try:
                    await context.bot.edit_message_text(
                        text=text_for_this_edit, chat_id=chat_id,
                        message_id=current_bot_message.message_id, parse_mode=constants.ParseMode.MARKDOWN_V2
                    )
                    current_content_is_transformed_plain = False
                    logger.debug(f"Chat {chat_id}: Stream edit with RAW MarkdownV2 successful.")
                except BadRequest as e_md:
                    log_preview = text_for_this_edit[:70].replace(chr(10), ' ') + '...'
                    logger.warning(
                        f"Chat {chat_id}: Stream edit with RAW MDV2 failed: {e_md}. Preview: '{log_preview}'")
                    if "Message is too long" in str(e_md):
                        logger.info(f"Chat {chat_id}: Stream text too long. Sending accumulated (RAW) via fallback.")
                        await send_long_message_fallback(update, text_for_this_edit, is_escaped=False)
                        accumulated_raw_text = ""
                        current_bot_message = await update.message.reply_text(
                            escape_markdown_v2("...continuing"), parse_mode=constants.ParseMode.MARKDOWN_V2
                        )
                        current_content_is_transformed_plain = False
                    elif "Message is not modified" in str(e_md):
                        logger.debug(f"Chat {chat_id}: Stream edit (RAW MDV2): Message not modified.")
                    else:
                        logger.warning(f"Chat {chat_id}: Stream RAW MDV2 failed. Attempting TRANSFORMED PLAIN.")
                        transformed_fallback_text = transform_markdown_fallback(text_for_this_edit)
                        try:
                            if transformed_fallback_text != current_bot_message.text or not current_content_is_transformed_plain:
                                await context.bot.edit_message_text(
                                    text=transformed_fallback_text, chat_id=chat_id,
                                    message_id=current_bot_message.message_id, parse_mode=None
                                )
                                current_content_is_transformed_plain = True
                                logger.info(f"Chat {chat_id}: Stream edit with TRANSFORMED PLAIN text successful.")
                            else:
                                logger.debug(
                                    f"Chat {chat_id}: Stream edit (TRANSFORMED PLAIN): Content same as current; skipping.")
                        except BadRequest as e_plain:
                            if "Message is not modified" in str(e_plain):
                                logger.debug(f"Chat {chat_id}: Stream edit (TRANSFORMED PLAIN): Message not modified.")
                                current_content_is_transformed_plain = True
                            else:
                                logger.error(
                                    f"Chat {chat_id}: Stream edit with TRANSFORMED PLAIN text ALSO FAILED: {e_plain}. Sending original raw as plain.")
                                try:
                                    if text_for_this_edit != current_bot_message.text:
                                        await context.bot.edit_message_text(text=text_for_this_edit, chat_id=chat_id,
                                                                            message_id=current_bot_message.message_id,
                                                                            parse_mode=None)
                                        current_content_is_transformed_plain = True
                                        logger.info(
                                            f"Chat {chat_id}: Stream edit with ORIGINAL RAW PLAIN text successful.")
                                except Exception as e_ultra_fallback:
                                    logger.error(
                                        f"Chat {chat_id}: Stream edit with ORIGINAL RAW PLAIN also failed: {e_ultra_fallback}")
                last_edit_time = current_time
                await asyncio.sleep(0.05)

        logger.debug(
            f"Chat {chat_id}: Gemini stream finished. Full raw response length: {len(full_raw_response_for_history)}")
        final_text_to_send_raw = accumulated_raw_text.strip()
        done_message_escaped = escape_markdown_v2("✅ Done.")

        if final_text_to_send_raw:
            is_final_same_as_current_md = (
                    final_text_to_send_raw == current_bot_message.text and
                    not current_content_is_transformed_plain and
                    current_bot_message.text != initial_placeholder_escaped
            )
            is_final_same_as_current_plain = (
                    transform_markdown_fallback(final_text_to_send_raw) == current_bot_message.text and
                    current_content_is_transformed_plain and
                    current_bot_message.text != initial_placeholder_escaped
            )

            if is_final_same_as_current_md or is_final_same_as_current_plain:
                logger.info(f"Chat {chat_id}: Final text is identical to current message content. No final edit.")
            else:
                try:
                    await context.bot.edit_message_text(
                        text=final_text_to_send_raw, chat_id=chat_id,
                        message_id=current_bot_message.message_id, parse_mode=constants.ParseMode.MARKDOWN_V2
                    )
                    logger.info(f"Chat {chat_id}: Final edit with RAW MarkdownV2 successful.")
                except BadRequest as e_final_md:
                    logger.warning(f"Chat {chat_id}: Final edit with RAW MDV2 failed: {e_final_md}.")
                    if "Message is too long" in str(e_final_md):
                        logger.info(f"Chat {chat_id}: Final text too long. Sending (RAW) via fallback.")
                        await send_long_message_fallback(update, final_text_to_send_raw, is_escaped=False)
                        if current_bot_message.text == initial_placeholder_escaped or "...continuing" in current_bot_message.text:
                            await context.bot.edit_message_text(
                                text=done_message_escaped, chat_id=chat_id,
                                message_id=current_bot_message.message_id, parse_mode=constants.ParseMode.MARKDOWN_V2)
                    elif "Message is not modified" in str(e_final_md):
                        logger.info(f"Chat {chat_id}: Final edit (RAW MDV2): Message not modified.")
                    else:
                        logger.warning(f"Chat {chat_id}: Final RAW MDV2 failed. Attempting TRANSFORMED PLAIN.")
                        final_transformed_text = transform_markdown_fallback(final_text_to_send_raw)
                        try:
                            if final_transformed_text != current_bot_message.text or not current_content_is_transformed_plain:
                                await context.bot.edit_message_text(
                                    text=final_transformed_text, chat_id=chat_id,
                                    message_id=current_bot_message.message_id, parse_mode=None
                                )
                                logger.info(f"Chat {chat_id}: Final edit with TRANSFORMED PLAIN text successful.")
                            else:
                                logger.info(
                                    f"Chat {chat_id}: Final edit (TRANSFORMED PLAIN): Content same or already plain; skipping.")
                        except BadRequest as e_final_plain:
                            if "Message is not modified" in str(e_final_plain):
                                logger.info(f"Chat {chat_id}: Final edit (TRANSFORMED PLAIN): Message not modified.")
                            else:
                                logger.error(
                                    f"Chat {chat_id}: Final edit with TRANSFORMED PLAIN text ALSO FAILED: {e_final_plain}. Sending original raw as plain.")
                                try:
                                    if final_text_to_send_raw != current_bot_message.text:
                                        await context.bot.edit_message_text(text=final_text_to_send_raw,
                                                                            chat_id=chat_id,
                                                                            message_id=current_bot_message.message_id,
                                                                            parse_mode=None)
                                        logger.info(
                                            f"Chat {chat_id}: Final edit with ORIGINAL RAW PLAIN text successful.")
                                except Exception as e_ultra_final:
                                    logger.error(
                                        f"Chat {chat_id}: Final edit with ORIGINAL RAW PLAIN also failed: {e_ultra_final}")
                        except Exception as e_ultimate_final_other:
                            logger.error(
                                f"Chat {chat_id}: Unexpected error during final transformed plain edit: {e_ultimate_final_other}",
                                exc_info=True)

        elif (
                current_bot_message.text == initial_placeholder_escaped or "...continuing" in current_bot_message.text) and full_raw_response_for_history.strip():
            logger.debug(
                f"Chat {chat_id}: No final accumulated text, but had a response. Updating placeholder to 'Done'.")
            await context.bot.edit_message_text(
                text=done_message_escaped, chat_id=chat_id,
                message_id=current_bot_message.message_id, parse_mode=constants.ParseMode.MARKDOWN_V2)
        elif current_bot_message.text == initial_placeholder_escaped and not full_raw_response_for_history.strip():
            logger.info(f"Chat {chat_id}: Gemini produced no response. Updating placeholder to 'no response'.")
            no_response_escaped = escape_markdown_v2("I couldn't generate a response for that.")
            await context.bot.edit_message_text(
                text=no_response_escaped, chat_id=chat_id,
                message_id=current_bot_message.message_id, parse_mode=constants.ParseMode.MARKDOWN_V2)

        logger.info(
            f"Chat {chat_id}: Finished handling message. Full raw AI response length: {len(full_raw_response_for_history)}")
        if full_raw_response_for_history.strip() and not any(
                err_msg in full_raw_response_for_history.lower() for err_msg in
                ["sorry", "i can't", "not available", "guidelines", "blocked", "unable to", "i am unable",
                 "cannot provide", "cannot create"]):
            conversation_history.append({'role': 'user', 'parts': [{'text': message_text}]})
            conversation_history.append({'role': 'model', 'parts': [{'text': full_raw_response_for_history}]})
            if len(conversation_history) > MAX_CONVERSATION_TURNS * 2:
                conversation_history = conversation_history[-(MAX_CONVERSATION_TURNS * 2):]
            context.chat_data['conversation_history'] = conversation_history
            logger.debug(f"Chat {chat_id}: Conversation history updated. Length: {len(conversation_history)} items.")
        else:
            logger.warning(
                f"Chat {chat_id}: AI response empty or potentially a refusal. Not saving to history. Response: '{full_raw_response_for_history[:100].replace(chr(10), ' ')}...'")

    except Exception as e:
        logger.error(f"Chat {chat_id}: Unhandled error in handle_message (after placeholder sent): {e}", exc_info=True)
        error_msg_escaped = escape_markdown_v2(
            "⚠️ An unexpected error occurred while processing your request. Please try again.")
        try:
            if current_bot_message and current_bot_message.text != error_msg_escaped:
                await context.bot.edit_message_text(
                    error_msg_escaped, chat_id=chat_id,
                    message_id=current_bot_message.message_id, parse_mode=constants.ParseMode.MARKDOWN_V2)
        except Exception as e_err_send:
            logger.error(f"Chat {chat_id}: Failed to send/edit final error message: {e_err_send}", exc_info=True)
            try:
                await update.message.reply_text("An error occurred processing your request.")
            except Exception as e_super_final:
                logger.critical(f"Chat {chat_id}: Could not even send a plain text error message: {e_super_final}")


async def send_long_message_fallback(update: Update, text_to_send: str, max_length: int = TELEGRAM_MAX_MESSAGE_LENGTH,
                                     is_escaped: bool = False):
    logger.debug(f"send_long_message_fallback called. is_escaped: {is_escaped}, text length: {len(text_to_send)}")
    parts = []
    current_text = str(text_to_send)

    if not current_text.strip():
        logger.info("send_long_message_fallback: called with empty or whitespace-only text. Nothing to send.")
        return

    while len(current_text) > 0:
        if len(current_text) > max_length:
            part_to_send_segment = current_text[:max_length]
            last_newline = part_to_send_segment.rfind('\n', max(0, max_length - 300))
            last_space = part_to_send_segment.rfind(' ', max(0, max_length - 300))
            split_at = max_length
            if last_newline != -1:
                split_at = last_newline + 1
            elif last_space != -1:
                split_at = last_space + 1
            parts.append(current_text[:split_at])
            current_text = current_text[split_at:].lstrip()
        else:
            parts.append(current_text)
            break

    if not parts:
        logger.warning("send_long_message_fallback: No parts were generated. Original text: '%s...'",
                       text_to_send[:100].replace('\n', ' '))
        return

    for i, segment_to_send_orig in enumerate(parts):
        segment_to_send_raw = segment_to_send_orig.strip()
        if not segment_to_send_raw:
            logger.debug(f"Fallback: Skipping empty segment {i + 1}/{len(parts)}.")
            continue

        log_segment_preview = segment_to_send_raw[:70].replace('\n', ' ') + (
            '...' if len(segment_to_send_raw) > 70 else '')
        logger.debug(
            f"Fallback: Attempting to send segment {i + 1}/{len(parts)}, length {len(segment_to_send_raw)}. is_escaped: {is_escaped}. Preview: '{log_segment_preview}'")
        sent_successfully = False

        try:
            if is_escaped:
                await update.message.reply_text(segment_to_send_raw, parse_mode=constants.ParseMode.MARKDOWN_V2)
                logger.debug(
                    f"Fallback (is_escaped=True): Sent pre-escaped segment {i + 1}/{len(parts)} as MarkdownV2.")
                sent_successfully = True
            else:  # is_escaped is False, so segment_to_send_raw is raw Markdown
                await update.message.reply_text(segment_to_send_raw, parse_mode=constants.ParseMode.MARKDOWN_V2)
                logger.debug(f"Fallback (is_escaped=False): Sent raw segment {i + 1}/{len(parts)} as MarkdownV2.")
                sent_successfully = True
        except BadRequest as e_md_fail:
            logger.warning(
                f"Fallback (is_escaped={is_escaped}): MarkdownV2 send failed for segment {i + 1}/{len(parts)}. Error: {e_md_fail}. "
                f"Preview: '{log_segment_preview}'. Attempting TRANSFORMED PLAIN text.")
            text_to_try_plain = segment_to_send_raw
            if not is_escaped:  # If it was raw MD, transform it for plain sending
                text_to_try_plain = transform_markdown_fallback(segment_to_send_raw)
            try:
                await update.message.reply_text(text_to_try_plain, parse_mode=None)  # Send as plain
                logger.info(
                    f"Fallback (is_escaped={is_escaped}, transformed_if_raw={not is_escaped}): Sent segment {i + 1}/{len(parts)} as PLAIN text after MDV2 BadRequest. "
                    f"Preview: '{text_to_try_plain[:70].replace(chr(10), ' ')}...'")
                sent_successfully = True
            except Exception as e_plain_fail:
                logger.error(
                    f"Fallback (is_escaped={is_escaped}, transformed_if_raw={not is_escaped}): PLAIN text send ALSO FAILED for segment {i + 1}/{len(parts)}. Error: {e_plain_fail}. "
                    f"Preview: '{text_to_try_plain[:70].replace(chr(10), ' ')}...'")
        except Exception as e_other_initial_send_fail:  # Other errors not BadRequest
            logger.error(
                f"Fallback (is_escaped={is_escaped}): Other critical error during initial send of segment {i + 1}/{len(parts)}. Error: {e_other_initial_send_fail}. "
                f"Preview: '{log_segment_preview}'. Attempting original raw as PLAIN text as last resort.")
            try:  # Last ditch: send original segment_to_send_raw as plain
                await update.message.reply_text(segment_to_send_raw, parse_mode=None)
                logger.info(
                    f"Fallback (is_escaped={is_escaped}): Sent segment {i + 1}/{len(parts)} as ORIGINAL RAW PLAIN text after other critical MDV2 error. "
                    f"Preview: '{log_segment_preview}'")
                sent_successfully = True
            except Exception as e_plain_fail_after_other:
                logger.error(
                    f"Fallback (is_escaped={is_escaped}): ORIGINAL RAW PLAIN text send ALSO FAILED for segment {i + 1}/{len(parts)} after other critical MDV2 error. Error: {e_plain_fail_after_other}. "
                    f"Preview: '{log_segment_preview}'")

        if not sent_successfully:
            logger.critical(
                f"Fallback: FAILED TO SEND segment {i + 1}/{len(parts)} by any method. Preview: '{log_segment_preview}'")
            try:
                error_update_text_escaped = escape_markdown_v2(
                    "⚠️ Error: A part of my response could not be displayed correctly.")
                await update.message.reply_text(error_update_text_escaped, parse_mode=constants.ParseMode.MARKDOWN_V2)
            except Exception as e_generic_error_send:
                logger.error(f"Failed to send generic 'part lost' error message to user: {e_generic_error_send}")

        if i < len(parts) - 1 and sent_successfully:
            await asyncio.sleep(0.3)  # Small delay between sending multiple parts


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

    logger.info("Application object and handlers registered in get_application_with_persistence.")  # Modified log
    return application

# --- END OF FILE telegram_bot.py ---