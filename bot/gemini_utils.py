# --- START OF FILE bot/gemini_utils.py ---
import asyncio
import google.generativeai as genai  # Main SDK import
from google.generativeai import types as genai_types  # For Part, StopCandidateException
from google.generativeai.types import HarmCategory, HarmBlockThreshold  # These are often directly on types

from google.api_core import exceptions as google_exceptions
import os
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type, RetryError

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME_FROM_ENV = os.getenv("GEMINI_MODEL_NAME", 'models/gemini-1.5-flash-latest')

if not GEMINI_API_KEY:
    logger.critical("CRITICAL: GEMINI_API_KEY not found in environment.")
    raise ValueError("GEMINI_API_KEY not found. Ensure .env is loaded or env var is set.")

try:
    genai.configure(api_key=GEMINI_API_KEY)
    logger.info("Gemini API key configured successfully.")
except Exception as e:
    logger.critical(f"CRITICAL: Failed to configure Gemini API: {e}")
    raise

model_instance = None
try:
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    }
    model_instance = genai.GenerativeModel(
        MODEL_NAME_FROM_ENV,
        safety_settings=safety_settings,
    )
    logger.info(f"Successfully initialized Gemini model: {MODEL_NAME_FROM_ENV}")
except Exception as e:
    logger.critical(f"CRITICAL: Could not initialize Gemini model '{MODEL_NAME_FROM_ENV}'. Error: {e}")
    raise


@retry(
    wait=wait_exponential(multiplier=1, min=2, max=45),
    stop=stop_after_attempt(5),
    retry=(
            retry_if_exception_type(google_exceptions.ResourceExhausted) |
            retry_if_exception_type(google_exceptions.InternalServerError) |
            retry_if_exception_type(google_exceptions.ServiceUnavailable) |
            retry_if_exception_type(google_exceptions.Aborted) |
            retry_if_exception_type(google_exceptions.DeadlineExceeded)
    ),
    before_sleep=lambda retry_state: logger.warning(
        f"Retrying Gemini API call due to {type(retry_state.outcome.exception()).__name__}, attempt {retry_state.attempt_number}, waiting {retry_state.next_action.sleep}s..."
    )
)
def _generate_content_with_retry(model_contents: list, stream: bool = False):
    if not model_instance:
        raise RuntimeError("Gemini model_instance is not initialized.")
    logger.debug(
        f"Calling model_instance.generate_content (stream={stream}). Input preview: {str(model_contents)[:300]}...")
    return model_instance.generate_content(model_contents, stream=stream)


async def _handle_gemini_response_stream(response_stream_iterator, context_message="response"):
    full_response_text = ""
    for chunk in response_stream_iterator:
        if hasattr(chunk, 'usage_metadata') and chunk.usage_metadata:
            prompt_tokens = getattr(chunk.usage_metadata, 'prompt_token_count', 0)
            candidates_tokens = getattr(chunk.usage_metadata, 'candidates_token_count', 0)
            total_tokens = getattr(chunk.usage_metadata, 'total_token_count', prompt_tokens + candidates_tokens)
            logger.info(
                f"Gemini Usage ({context_message}): Prompt Tokens={prompt_tokens}, Output Tokens={candidates_tokens}, Total Tokens={total_tokens}")

        if chunk.prompt_feedback and chunk.prompt_feedback.block_reason:
            block_reason_message = chunk.prompt_feedback.block_reason_message or chunk.prompt_feedback.block_reason.name
            logger.warning(f"Stream ({context_message}) blocked by Gemini. Reason: {block_reason_message}.")
            yield f"I'm sorry, my {context_message} was blocked due to content guidelines (Reason: {block_reason_message})."
            return

        chunk_text_parts = []
        if chunk.parts:
            for part in chunk.parts:
                if hasattr(part, 'text'):
                    chunk_text_parts.append(part.text)

        current_chunk_text = "".join(chunk_text_parts)
        if current_chunk_text:
            full_response_text += current_chunk_text
            yield current_chunk_text

        # Try accessing FinishReason from the main 'genai' module
        if chunk.candidates and hasattr(genai, 'FinishReason') and \
                chunk.candidates[0].finish_reason != genai.FinishReason.STOP:
            if not current_chunk_text:
                candidate = chunk.candidates[0]
                finish_reason_value = candidate.finish_reason
                finish_reason_name = "UNKNOWN"
                try:
                    finish_reason_name = genai.FinishReason(finish_reason_value).name
                except ValueError:
                    logger.warning(f"Unknown finish_reason integer value: {finish_reason_value}")
                except AttributeError:  # If genai.FinishReason wasn't what we thought
                    logger.error("genai.FinishReason is not the correct enum. Check SDK.")
                    yield f"...my {context_message} ended with an unknown status."
                    return

                logger.warning(
                    f"Gemini stream ({context_message}) may have ended prematurely. Finish Reason: {finish_reason_name} (Value: {finish_reason_value}).")
                if finish_reason_value == genai.FinishReason.SAFETY:
                    yield f"My {context_message} was cut short due to safety guidelines."
                elif finish_reason_value == genai.FinishReason.MAX_TOKENS:
                    yield f"...my {context_message} was cut short as it reached the maximum length."
                elif finish_reason_value == genai.FinishReason.RECITATION:
                    yield f"...my {context_message} was cut short as it closely matched a source."
                elif finish_reason_value == genai.FinishReason.OTHER:
                    yield f"...my {context_message} ended for an unspecified reason."
                else:
                    yield f"...my {context_message} ended unexpectedly (Reason: {finish_reason_name})."
                return
    logger.info(f"Finished streaming {context_message} from Gemini. Total length: {len(full_response_text)}")


async def ask_gemini_stream(current_question: str, conversation_history: list = None, system_prompt: str = None):
    if not model_instance:
        logger.error("Gemini model is not initialized. Cannot process text request.")
        yield "Sorry, the AI model is not available right now."
        return

    messages_for_gemini = []
    if system_prompt:
        messages_for_gemini.extend([
            {'role': 'user', 'parts': [{'text': system_prompt}]},
            {'role': 'model', 'parts': [{
                                            'text': "Okay, I understand. I will use Markdown for formatting where appropriate. How can I help you?"}]}
        ])
    if conversation_history:
        messages_for_gemini.extend(conversation_history)
    messages_for_gemini.append({'role': 'user', 'parts': [{'text': current_question}]})

    logger.info(
        f"Preparing to stream TEXT to Gemini (model: {MODEL_NAME_FROM_ENV}). User question: '{current_question[:100]}...'")

    try:
        sync_response_iterator = await asyncio.get_running_loop().run_in_executor(
            None, _generate_content_with_retry, messages_for_gemini, True
        )
        async for chunk_text in _handle_gemini_response_stream(sync_response_iterator, "text response"):
            yield chunk_text
    except RetryError as e:
        last_exception = e.last_attempt.exception()
        error_yield_message = "Sorry, I had trouble connecting to my AI brain after several attempts."
        if isinstance(last_exception, google_exceptions.ResourceExhausted):
            logger.error(f"Quota likely exceeded for Gemini text stream: {last_exception}", exc_info=False)
            error_yield_message = "I'm currently experiencing high demand. Please try again in a few moments."
        else:
            logger.error(f"Retries failed for Gemini text stream: {e}", exc_info=True)
        yield error_yield_message
    except genai_types.StopCandidateException as e:
        logger.warning(f"Gemini text stream stopped by StopCandidateException: {e}", exc_info=True)
        yield "My response was stopped, possibly due to content guidelines. Please try rephrasing."
    except Exception as e:
        logger.error(f"Unexpected ERROR during Gemini text stream: {e}", exc_info=True)
        yield "Sorry, an unexpected issue occurred while generating my response."


async def ask_gemini_vision_stream(
        prompt_text: str,
        image_bytes: bytes,
        image_mime_type: str,
        conversation_history: list = None,
        system_prompt: str = None
):
    if not model_instance:
        logger.error("Gemini (multimodal) model is not initialized. Cannot process vision request.")
        yield "Sorry, the AI model for images is not available right now."
        return

    try:
        image_part = genai_types.Part.from_data(data=image_bytes, mime_type=image_mime_type)
    except Exception as e_part:
        logger.error(f"Failed to create image Part for Gemini: {e_part}", exc_info=True)
        yield "Sorry, there was an issue preparing your image for the AI (invalid image data or MIME type?)."
        return

    model_contents_for_vision = []
    if system_prompt or conversation_history:
        if system_prompt:
            model_contents_for_vision.extend([
                {'role': 'user', 'parts': [genai_types.Part.from_text(system_prompt)]},
                {'role': 'model',
                 'parts': [genai_types.Part.from_text("Okay, I understand the instructions for analyzing the image.")]}
            ])
        if conversation_history:
            model_contents_for_vision.extend(conversation_history)

        current_user_parts = []
        if prompt_text:
            current_user_parts.append(genai_types.Part.from_text(prompt_text))
        current_user_parts.append(image_part)
        model_contents_for_vision.append({'role': 'user', 'parts': current_user_parts})
        logger.info(
            f"Preparing to stream MULTIMODAL (chat-style) to Gemini. Text: '{prompt_text[:50]}...', Image MIME: {image_mime_type}")
    else:
        model_contents_for_vision.append(image_part)
        if prompt_text:
            model_contents_for_vision.append(genai_types.Part.from_text(prompt_text))
        else:
            model_contents_for_vision.append(genai_types.Part.from_text("Describe this image or explain its content."))
        logger.info(
            f"Preparing to stream MULTIMODAL (direct parts) to Gemini. Text: '{prompt_text[:50]}...', Image MIME: {image_mime_type}")

    if not model_contents_for_vision or \
            (isinstance(model_contents_for_vision[0], dict) and not model_contents_for_vision[0].get("parts")) or \
            (isinstance(model_contents_for_vision, list) and not model_contents_for_vision):
        logger.error("No content parts to send to Gemini for vision stream.")
        yield "Nothing to process for the image."
        return

    try:
        sync_response_iterator = await asyncio.get_running_loop().run_in_executor(
            None, _generate_content_with_retry, model_contents_for_vision, True
        )
        async for chunk_text in _handle_gemini_response_stream(sync_response_iterator, "image response"):
            yield chunk_text

    except RetryError as e:
        last_exception = e.last_attempt.exception()
        error_yield_message = "Sorry, I had trouble analyzing the image after several attempts."
        if isinstance(last_exception, google_exceptions.ResourceExhausted):
            logger.error(f"Quota likely exceeded for Gemini vision stream: {last_exception}", exc_info=False)
            error_yield_message = "I'm currently experiencing high demand for image analysis. Please try again in a few moments."
        elif isinstance(last_exception, google_exceptions.InvalidArgument):
            logger.error(f"Invalid argument for Gemini vision stream: {last_exception}", exc_info=True)
            error_yield_message = "There was an issue with the image format or content (e.g., unsupported type, corrupted data, or prompt structure). Please try a different image or prompt."
        else:
            logger.error(f"Retries failed for Gemini vision stream: {e}", exc_info=True)
        yield error_yield_message
    except genai_types.StopCandidateException as e:
        logger.warning(f"Gemini vision stream stopped by StopCandidateException: {e}", exc_info=True)
        yield "My response to the image was stopped, possibly due to content guidelines."
    except Exception as e:
        logger.error(f"Unexpected ERROR during Gemini vision stream: {e}", exc_info=True)
        yield "Sorry, an unexpected issue occurred while analyzing the image."

# --- END OF FILE bot/gemini_utils.py ---