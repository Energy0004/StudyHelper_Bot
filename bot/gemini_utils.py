# --- START OF FILE bot/gemini_utils.py ---

import os
import logging
from typing import AsyncGenerator, List, Dict, Any, Union
import google.generativeai as genai
from google.generativeai.types import (
    GenerationConfig,
    ContentDict,
    PartDict,
    Tool,
    FunctionDeclaration,
)
# Import the web search function from your other file
from .web_search import perform_web_search

logger = logging.getLogger(__name__)  # This will be 'bot.gemini_utils'

# --- API Key Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    logger.critical("CRITICAL: GEMINI_API_KEY not found in environment variables.")
    # In a production app, you might raise an error to prevent the bot from starting.
    raise EnvironmentError("GEMINI_API_KEY not found. The bot cannot function without it.")
else:
    genai.configure(api_key=GEMINI_API_KEY)

# --- Tool Definition for Gemini ---
# Here we define the structure of our `perform_web_search` function so Gemini knows what it is,
# what it does, and what arguments it takes.
web_search_tool = Tool(
    function_declarations=[
        FunctionDeclaration(
            name="perform_web_search",
            # This description is the most critical part. Let's make it more explicit.
            description=(
                "Use this tool to get real-time, up-to-date information from the internet. "
                "This is ESSENTIAL for any questions about recent events, current affairs, "
                "news, the latest results of sports games, recent product announcements (like from Apple, Google, etc.), "
                "or any topic where the information is likely to have changed since the model's last training cut-off. "
                "Do NOT say you cannot access real-time information; use this tool instead."
            ),
            parameters={
                "type": "OBJECT",
                "properties": {
                    "search_query": {
                        "type": "STRING",
                        "description": "A clear, concise, and effective search query that will find the relevant information on the web.",
                    }
                },
                "required": ["search_query"],
            },
        )
    ]
)

# A mapping from the function name (as known by Gemini) to our actual callable Python function.
TOOL_REGISTRY = {
    "perform_web_search": perform_web_search,
}


# --- Internal Helper for Streaming Text Chunks ---
async def _handle_gemini_response_stream(
        response: AsyncGenerator[Any, None], is_vision: bool = False
) -> AsyncGenerator[str, None]:
    """
    An internal helper to process and yield text from a Gemini stream response.
    This function itself doesn't know about tools; it just extracts text.
    """
    full_response_text = ""
    try:
        async for chunk in response:
            if chunk.text:
                full_response_text += chunk.text
                yield chunk.text
    except Exception as e:
        logger.error(f"Error while streaming Gemini response: {e}", exc_info=True)
        error_message = f"\n\n[AI ERROR: An error occurred while generating the response: {e}]"
        yield error_message
        full_response_text += error_message
    finally:
        # This part of the logic for token counting from streaming responses can be tricky
        # and may vary by library version. We'll attempt it safely.
        prompt_tokens = 0
        output_tokens = 0
        total_tokens = 0
        try:
            # For streaming, prompt_feedback might be available after the first chunk
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                usage_metadata = response.prompt_feedback.usage_metadata
                prompt_tokens = usage_metadata.prompt_token_count
                # In streaming, candidates_token_count accumulates, so we take the final value if available
                output_tokens = usage_metadata.candidates_token_count
                total_tokens = usage_metadata.total_token_count
        except (AttributeError, Exception):
            # Silently ignore if token information is not available in this context
            pass

        if total_tokens > 0:
            logger.info(
                f"Gemini Usage ({'image' if is_vision else 'text'} response): "
                f"Prompt Tokens={prompt_tokens}, Output Tokens={output_tokens}, Total Tokens={total_tokens}"
            )

        logger.info(
            f"Finished streaming {'image' if is_vision else 'text'} response from Gemini. Final raw length: {len(full_response_text)}")


# --- Main Text Generation Function with Tool Orchestration ---
async def ask_gemini_stream(
        current_question: str,
        conversation_history: List[Dict[str, Any]],
        system_prompt: str,
) -> AsyncGenerator[Union[str, Dict[str, Any]], None]:
    """
    Handles a conversation with Gemini, including tool calls for web search.
    This version uses basic dictionaries for maximum compatibility.
    """
    model_name = "gemini-1.5-flash-latest"
    model = genai.GenerativeModel(
        model_name,
        system_instruction=system_prompt,
        generation_config=GenerationConfig(temperature=0.7),
        tools=[web_search_tool]
    )
    chat_session = model.start_chat(history=conversation_history)

    logger.debug(f"Sending prompt to Gemini. Prompt: '{current_question[:100]}...'")

    try:
        response_stream = await chat_session.send_message_async(current_question, stream=True)

        function_call_to_execute = None
        tool_name = None
        tool_args = None

        async for chunk in response_stream:
            # CORRECT ORDER: Check for a function call first.
            if chunk.parts and chunk.parts[0].function_call:
                logger.info("Function call received in stream.")
                function_call_to_execute = chunk.parts[0].function_call
                tool_name = function_call_to_execute.name
                tool_args = dict(function_call_to_execute.args)
                break

            # Then, check for text.
            if chunk.text:
                yield chunk.text

        if function_call_to_execute:
            logger.info(f"Gemini requested tool call: '{tool_name}' with args: {tool_args}")
            yield {"tool_call_start": True, "tool_name": tool_name}

            if tool_name in TOOL_REGISTRY:
                tool_function = TOOL_REGISTRY[tool_name]
                tool_response_content = await tool_function(**tool_args)

                logger.debug("Sending tool response back to Gemini using a basic dictionary.")

                # --- THE MOST COMPATIBLE METHOD: A PLAIN DICTIONARY ---
                # This bypasses all problematic helper classes.
                response_after_tool = await chat_session.send_message_async(
                    {
                        "parts": [{
                            "function_response": {
                                "name": tool_name,
                                "response": {"result": tool_response_content}
                            }
                        }]
                    },
                    stream=True
                )

                async for final_chunk in response_after_tool:
                    if final_chunk.text:
                        yield final_chunk.text
            else:
                logger.error(f"Gemini requested an unknown tool: '{tool_name}'")
                yield f"[ERROR: AI tried to use a tool named '{tool_name}' that is not defined.]"
        else:
            logger.info("Stream finished without a tool call request.")

    except Exception as e:
        logger.error(f"An error occurred in the main ask_gemini_stream orchestrator: {e}", exc_info=True)
        yield f"\n\n[AI ERROR: An unexpected error occurred while communicating with the AI: {e}]"

# --- Vision Model Function (kept separate and simple) ---
async def ask_gemini_vision_stream(
        prompt_text: str,
        image_bytes: bytes,
        image_mime_type: str,
        conversation_history: List[Dict[str, Any]],
        system_prompt: str
) -> AsyncGenerator[str, None]:
    """
    Generates content from Gemini based on a prompt and an image.
    """
    # --- THIS IS THE ONLY LINE THAT CHANGES ---
    # The old, deprecated model is replaced with a new, powerful one.
    model_name = "gemini-1.5-flash-latest"

    logger.info(f"Using vision model: {model_name}")  # Added a log for better debugging
    model = genai.GenerativeModel(model_name, system_instruction=system_prompt)

    # Your existing logic for preparing the prompt is correct and compatible.
    image_part = PartDict(inline_data=PartDict(data=image_bytes, mime_type=image_mime_type))
    prompt_parts = [prompt_text, image_part]

    try:
        response = await model.generate_content_async(prompt_parts, stream=True)
        # Your existing logic for handling the response stream is also correct.
        async for chunk in _handle_gemini_response_stream(response, is_vision=True):
            yield chunk
    except Exception as e:
        logger.error(f"Error during Gemini Vision API call: {e}", exc_info=True)
        # Your existing error handling is perfect.
        yield f"\n\n[AI ERROR: Could not analyze the image. The AI service reported an error.]"

# --- END OF FILE bot/gemini_utils.py ---