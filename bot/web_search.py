# --- START OF NEW bot/web_search.py ---

import os
import logging
import httpx
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Load credentials from environment variables
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

async def perform_web_search(search_query: str, num_results: int = 5) -> str:
    """
    Performs a web search using the Google Custom Search JSON API.

    Args:
        search_query: The string to search for.
        num_results: The maximum number of results to return (max 10 for this API).

    Returns:
        A formatted string containing search results, or an error message.
    """
    logger.info(f"Performing Google web search for: '{search_query}'")

    if not GOOGLE_SEARCH_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        error_message = "Google Search API Key or Search Engine ID is not configured."
        logger.error(error_message)
        return f"[Search Configuration Error]: {error_message}"

    # The API endpoint and parameters
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": GOOGLE_SEARCH_ENGINE_ID,
        "q": search_query,
        "num": min(num_results, 10),  # API allows a max of 10 results per page
    }

    try:
        # Use httpx for an async request
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        data = response.json()
        search_items: List[Dict[str, Any]] = data.get("items", [])

        if not search_items:
            logger.warning(f"Google Search for '{search_query}' returned no results.")
            return "Web search returned no results."

        # Format the results into a single string for Gemini to process
        formatted_results = "Web search results:\n\n"
        for i, item in enumerate(search_items):
            title = item.get('title', 'No Title')
            link = item.get('link', 'No URL')
            snippet = item.get('snippet', 'No snippet available.').replace("\n", " ")
            formatted_results += f"Result {i + 1}:\n"
            formatted_results += f"  Title: {title}\n"
            formatted_results += f"  URL: {link}\n"
            formatted_results += f"  Snippet: {snippet}\n\n"

        logger.debug(f"Formatted Google Search results for Gemini:\n{formatted_results[:500]}...")
        return formatted_results

    except httpx.HTTPStatusError as e:
        error_body = e.response.text
        logger.error(f"HTTP error during Google Search for '{search_query}': {e}\nResponse: {error_body}", exc_info=True)
        return f"An error occurred while contacting the search service: {e}"
    except Exception as e:
        logger.error(f"An unexpected error occurred during Google Search for '{search_query}': {e}", exc_info=True)
        return f"An unexpected error occurred during the web search: {e}"

# --- END OF NEW bot/web_search.py ---