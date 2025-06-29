# --- START OF FINAL, FINAL, CORRECTED bot/web_search.py ---

import logging
from duckduckgo_search import DDGS

logger = logging.getLogger(__name__)

# This function is now synchronous internally, but it's called with `await` from an async function,
# which is fine. The event loop can handle it.
async def perform_web_search(search_query: str, num_results: int = 5) -> str:
    """
    Performs a web search using DuckDuckGo and returns a formatted string of results.
    This version uses the synchronous call which is most compatible.
    """
    logger.info(f"Performing web search for: '{search_query}'")
    try:
        # --- THE FINAL CORRECTION ---
        # Call .text() as a regular, synchronous function. It returns a list directly.
        with DDGS() as ddgs:
            results = ddgs.text(search_query, max_results=num_results)

        if not results:
            logger.warning(f"Web search for '{search_query}' returned no results.")
            return "Web search returned no results."

        # Format the results into a single string for Gemini to process
        formatted_results = "Web search results:\n\n"
        for i, res in enumerate(results):
            title = res.get('title', 'No Title')
            href = res.get('href', 'No URL')
            body = res.get('body', 'No snippet available.')
            formatted_results += f"Result {i + 1}:\n"
            formatted_results += f"  Title: {title}\n"
            formatted_results += f"  URL: {href}\n"
            formatted_results += f"  Snippet: {body}\n\n"

        logger.debug(f"Formatted search results for Gemini:\n{formatted_results[:500]}...")
        return formatted_results

    except Exception as e:
        logger.error(f"An error occurred during web search for '{search_query}': {e}", exc_info=True)
        return f"An error occurred while trying to perform the web search: {e}"

# --- END OF FINAL, FINAL, CORRECTED bot/web_search.py ---