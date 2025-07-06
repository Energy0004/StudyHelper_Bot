# --- START OF FINAL bot/gemini_utils.py ---

import os
import logging
import asyncio
from typing import AsyncGenerator, List, Dict, Any, Union

import google.generativeai as genai
# Use only the imports that are guaranteed to exist in your environment
from google.generativeai.types import GenerationConfig, Tool, FunctionDeclaration, PartDict

from .web_search import perform_web_search

logger = logging.getLogger(__name__)

# --- API Key Configuration ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError("CRITICAL: GEMINI_API_KEY not found.")
genai.configure(api_key=GEMINI_API_KEY)

web_search_tool = Tool(
    function_declarations=[
        FunctionDeclaration(
            name="perform_web_search",
            description=(
                "**MANDATORY:** This is your ONLY connection to the internet for real-time, up-to-date information. You MUST use it to answer any user query that cannot be answered with your static, pre-trained knowledge."
                "\n\n**Use this tool for questions about:**"
                "\n- **Current Events & News:** Any news, political situations, recent developments."
                "\n- **Recent Facts & Data:** Sports scores (like F1, football), award winners (like the Oscars, Grammys), stock prices, weather forecasts."
                "\n- **Recent Releases:** New movies, games, books, or product announcements (Apple, Google, etc.)."
                "\n- **Anything with a specific, recent date.**"
                "\n\n**CRITICAL INSTRUCTION:** Do NOT, under any circumstances, tell the user you cannot access real-time information or recommend they search on their own. That is a failure. You MUST formulate a search query and call this function instead."
            ),
            parameters={
                "type": "OBJECT",
                "properties": {"search_query": {"type": "STRING", "description": "An effective search query based on the user's question (e.g., 'Best Picture Oscar winner 2024', 'latest F1 Grand Prix results')."}},
                "required": ["search_query"],
            },
        )
    ]
)

TOOL_REGISTRY = {"perform_web_search": perform_web_search}

# --- Main Orchestrator Function ---
async def ask_gemini_stream(
        current_question: str,
        conversation_history: List[Dict[str, Any]],
        system_prompt: str,
) -> AsyncGenerator[Union[str, Dict[str, Any]], None]:
    """
    Handles a conversation with Gemini, including tool calls and manual retries.
    This version uses 'auto' tool-calling mode, relying on a strong system
    prompt to guide the model, which can prevent tool-looping behavior.
    """
    model_name = "gemini-1.5-flash-latest"

    # --- The Final Change: Use 'auto' mode ---
    # This lets the model choose between calling a tool or generating text directly.
    # Our strong system prompt should guide it to make the correct choice.
    auto_tool_config = {"function_calling_config": {"mode": "auto"}}

    model = genai.GenerativeModel(
        model_name,
        system_instruction=system_prompt,
        generation_config=GenerationConfig(temperature=0.7),
        tools=[web_search_tool],
        tool_config=auto_tool_config
    )

    max_retries = 3
    initial_delay = 1.5

    for attempt in range(max_retries):
        try:
            # Each attempt starts with a clean session to prevent state corruption
            chat_session = model.start_chat(history=conversation_history)
            logger.debug(f"Attempt {attempt + 1}/{max_retries}: Sending prompt...")

            # --- API Call #1 ---
            response_stream_1 = await chat_session.send_message_async(current_question, stream=True)

            function_call_to_execute = None
            text_from_stream_1 = ""

            # This loop correctly handles text and tool calls from the first response
            async for chunk in response_stream_1:
                if chunk.parts and chunk.parts[0].function_call:
                    function_call_to_execute = chunk.parts[0].function_call
                elif chunk.text:
                    text_from_stream_1 += chunk.text
                    yield chunk.text

            await response_stream_1.resolve()

            # --- Process the result of the first stream ---
            if function_call_to_execute:
                tool_name, tool_args = function_call_to_execute.name, dict(function_call_to_execute.args)
                logger.info(f"Gemini requested tool call: '{tool_name}' with args: {tool_args}")
                yield {"tool_call_start": True, "tool_name": tool_name}

                if tool_name in TOOL_REGISTRY:
                    tool_response_content = await TOOL_REGISTRY[tool_name](**tool_args)

                    # --- API Call #2 ---
                    response_stream_2 = await chat_session.send_message_async(
                        {"parts": [
                            {"function_response": {"name": tool_name, "response": {"result": tool_response_content}}}]},
                        stream=True
                    )

                    # Process the second stream, yielding text and ignoring any further tool calls
                    async for final_chunk in response_stream_2:
                        if final_chunk.parts and final_chunk.parts[0].function_call:
                            logger.warning(
                                f"Model requested a second function call: {final_chunk.parts[0].function_call.name}. Ignoring.")
                        elif final_chunk.text:
                            yield final_chunk.text

                    await response_stream_2.resolve()

                else:  # Handle unknown tool name
                    yield f"[AI ERROR: AI tried to use an unknown tool: {tool_name}]"

            else:  # This block now handles the case where the AI chose not to call a tool
                logger.warning("Model chose not to call a tool, yielding its direct text response.")
                # The text was already yielded in the loop above, so we just log and finish.
                if not text_from_stream_1:
                    logger.error("Model did not call a tool and did not return any text.")
                    yield "[AI ERROR: The AI did not generate a response.]"

            # If the 'try' block completed, we're done. Exit the retry loop.
            return

        except Exception as e:
            from google.api_core import exceptions
            if isinstance(e,
                          (exceptions.ServiceUnavailable, exceptions.ResourceExhausted)) and attempt < max_retries - 1:
                delay = initial_delay * (2 ** attempt)
                logger.warning(f"Temporary API error: {e}. Retrying in {delay:.1f} seconds...")
                await asyncio.sleep(delay)
                continue
            else:
                logger.error(f"A final, non-retryable error occurred in ask_gemini_stream: {e}", exc_info=True)
                yield f"\n\n[AI ERROR: An unexpected error occurred: {e}]"
                return

# --- Vision Model Function ---
async def ask_gemini_vision_stream(
        prompt_text: str,
        image_bytes: bytes,
        image_mime_type: str,
        conversation_history: List[Dict[str, Any]],
        system_prompt: str
) -> AsyncGenerator[str, None]:
    model_name = "gemini-1.5-flash-latest"
    logger.info(f"Using vision model: {model_name}")
    model = genai.GenerativeModel(model_name, system_instruction=system_prompt)

    # Use PartDict here which is confirmed to be available in your environment
    image_part = PartDict(inline_data=PartDict(data=image_bytes, mime_type=image_mime_type))
    prompt_parts = [prompt_text, image_part]

    try:
        response = await model.generate_content_async(prompt_parts, stream=True)
        async for chunk in response:
            if chunk.text:
                yield chunk.text
    except Exception as e:
        logger.error(f"Error during Gemini Vision API call: {e}", exc_info=True)
        yield f"\n\n[AI ERROR: Could not analyze the image. The AI service reported an error.]"

# --- END OF FINAL bot/gemini_utils.py ---