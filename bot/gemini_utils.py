# --- START OF FILE bot/gemini_utils.py ---
import asyncio

import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold, generation_types
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
    # You can also add generation_config here if needed, e.g. for temperature
    # generation_config = genai.types.GenerationConfig(temperature=0.7)
    model_instance = genai.GenerativeModel(
        MODEL_NAME_FROM_ENV,
        safety_settings=safety_settings,
        # generation_config=generation_config
    )
    logger.info(f"Successfully initialized Gemini model: {MODEL_NAME_FROM_ENV}")
except Exception as e:
    logger.critical(f"CRITICAL: Could not initialize Gemini model '{MODEL_NAME_FROM_ENV}'. Error: {e}")
    raise

@retry(
    wait=wait_exponential(multiplier=1, min=2, max=30),
    stop=stop_after_attempt(4),
    retry=(
        retry_if_exception_type(google_exceptions.ResourceExhausted) |
        retry_if_exception_type(google_exceptions.InternalServerError) |
        retry_if_exception_type(google_exceptions.ServiceUnavailable)
    ),
    before_sleep=lambda retry_state: logger.warning(
        f"Retrying Gemini API call due to {type(retry_state.outcome.exception()).__name__}, attempt {retry_state.attempt_number}, waiting {retry_state.next_action.sleep}s..."
    )
)
def _generate_content_with_retry(messages_to_send: list, stream: bool = False):
    """Internal function to call Gemini API, wrapped with tenacity for retries."""
    if not model_instance:
        raise RuntimeError("Gemini model_instance is not initialized.")
    logger.debug(f"Calling model_instance.generate_content (stream={stream}) with {len(messages_to_send)} message parts.")
    # Pass the stream argument to the actual API call
    return model_instance.generate_content(messages_to_send, stream=stream)


# This function will now be an async generator if streaming is requested
async def ask_gemini_stream(current_question: str, conversation_history: list = None, system_prompt: str = None):
    """
    Sends a prompt to Gemini and yields chunks of the response if streaming.
    If not streaming (though this function is designed for it), it would yield a single item.
    """

    if not model_instance:
        logger.error("Gemini model is not initialized. Cannot process request.")
        yield "Sorry, the AI model is not available right now." # Yield error message
        return

    messages_for_gemini = []
    if system_prompt: # System prompt now includes Markdown instruction
        messages_for_gemini.extend([
            {'role': 'user', 'parts': [{'text': system_prompt}]},
            {'role': 'model', 'parts': [{'text': "Okay, I understand. I will use Markdown for formatting where appropriate. How can I help you?"}]}
        ])
    if conversation_history:
        messages_for_gemini.extend(conversation_history)
    messages_for_gemini.append({'role': 'user', 'parts': [{'text': current_question}]})

    logger.info(f"Preparing to stream to Gemini (model: {MODEL_NAME_FROM_ENV}): Last user part: '{current_question[:100]}...'")

    full_response_text = ""
    try:
        # Always call with stream=True for this generator function
        response_stream = await asyncio.get_running_loop().run_in_executor(
            None, _generate_content_with_retry, messages_for_gemini, True # Pass stream=True
        )

        for chunk in response_stream:
            # Log usage metadata if available (usually at the end of a stream or if error)
            if hasattr(chunk, 'usage_metadata') and chunk.usage_metadata:
                prompt_tokens = getattr(chunk.usage_metadata, 'prompt_token_count', 0)
                candidates_tokens = getattr(chunk.usage_metadata, 'candidates_token_count', 0)
                total_tokens = getattr(chunk.usage_metadata, 'total_token_count', prompt_tokens + candidates_tokens)
                logger.info(
                    f"Gemini Usage (from stream chunk): Prompt Tokens={prompt_tokens}, Output Tokens={candidates_tokens}, Total Tokens={total_tokens}")

            if chunk.prompt_feedback and chunk.prompt_feedback.block_reason:
                block_reason_message = chunk.prompt_feedback.block_reason_message or chunk.prompt_feedback.block_reason.name
                logger.warning(f"Stream blocked by Gemini. Reason: {block_reason_message}.")
                yield f"I'm sorry, my response was blocked due to content guidelines (Reason: {block_reason_message})."
                return # Stop generation

            if chunk.parts:
                chunk_text = "".join(part.text for part in chunk.parts if hasattr(part, 'text'))
                if chunk_text:
                    full_response_text += chunk_text
                    yield chunk_text # Yield the actual text chunk
            elif chunk.candidates and chunk.candidates[0].finish_reason != generation_types.FinishReason.STOP : # Check for non-stop finish if no parts
                candidate = chunk.candidates[0]
                finish_reason = candidate.finish_reason
                logger.warning(f"Gemini stream ended prematurely. Finish Reason: {finish_reason.name}.")
                if finish_reason == generation_types.FinishReason.SAFETY:
                    yield "My response was cut short due to safety guidelines."
                elif finish_reason == generation_types.FinishReason.MAX_TOKENS:
                    yield "...my response was cut short as it reached the maximum length."
                elif finish_reason == generation_types.FinishReason.RECITATION:
                    yield "...my response was cut short as it closely matched a source."
                else:
                    yield f"...my response ended unexpectedly (Reason: {finish_reason.name})."
                return # Stop generation

        logger.info(f"Finished streaming from Gemini. Total length: {len(full_response_text)}")

    except RetryError as e:
        last_exception = e.last_attempt.exception()
        if isinstance(last_exception, google_exceptions.ResourceExhausted):
            logger.error(f"Quota likely exceeded for Gemini stream after all retries: {last_exception}", exc_info=False)
            yield "I'm currently experiencing high demand. Please try again in a few moments."
        else:
            logger.error(f"Retries failed for Gemini stream: {e}", exc_info=True)
            yield "Sorry, I had trouble connecting to my AI brain after several attempts."
    except generation_types.StopCandidateException as e:
        logger.warning(f"Gemini stream stopped by StopCandidateException: {e}")
        yield "My response was stopped, possibly due to content guidelines. Please try rephrasing."
    except Exception as e:
        logger.error(f"Unexpected ERROR during Gemini stream: {e}", exc_info=True)
        yield "Sorry, an unexpected issue occurred while generating my response."

# --- END OF FILE bot/gemini_utils.py ---