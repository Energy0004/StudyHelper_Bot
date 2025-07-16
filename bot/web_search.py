# --- bot/web_search.py ---

import os
import asyncio
import logging
import httpx
from bs4 import BeautifulSoup
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

# Load credentials from environment variables
GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")


# --- NEW: Helper function to scrape a single URL ---
async def scrape_url_content(url: str, client: httpx.AsyncClient) -> str:
    """
    Asynchronously scrapes the main text content from a given URL.
    Returns the text content or a string indicating failure.
    """
    try:
        logger.info(f"Scraping content from: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = await client.get(url, headers=headers, timeout=10, follow_redirects=True)
        response.raise_for_status()

        if 'text/html' not in response.headers.get('Content-Type', ''):
            logger.warning(f"Skipping non-HTML content at {url}")
            return "[Content is not a webpage]"

        soup = BeautifulSoup(response.content, 'html.parser')

        # A more robust text extraction strategy
        for element in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
            element.decompose()  # Remove irrelevant tags

        text = ' '.join(p.get_text(strip=True) for p in soup.find_all('p'))

        if not text:
            return "[No meaningful paragraph text found on this page]"

        return text[:3000]  # Return up to 3000 characters to keep it concise

    except Exception as e:
        logger.error(f"Failed to scrape URL {url}: {e}")
        return f"[Error scraping page: {e}]"


# --- MODIFIED: The main function is now a research agent ---
async def perform_web_search(search_query: str, num_results_to_scrape: int = 2) -> str:
    """
    Performs a web search, then scrapes the top results to provide a rich context.

    Args:
        search_query: The string to search for.
        num_results_to_scrape: The number of top search results to visit and scrape.

    Returns:
        A detailed, formatted string containing search snippets and scraped page content.
    """
    logger.info(f"Performing deep web search for: '{search_query}'")

    if not GOOGLE_SEARCH_API_KEY or not GOOGLE_SEARCH_ENGINE_ID:
        error_message = "Google Search API Key or Search Engine ID is not configured."
        logger.error(error_message)
        return f"[Search Configuration Error]: {error_message}"

    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": GOOGLE_SEARCH_ENGINE_ID,
        "q": search_query,
        "num": max(num_results_to_scrape, 5),  # Get a few more links than we plan to scrape
    }

    try:
        async with httpx.AsyncClient() as client:
            # 1. Perform the initial Google Search
            google_response = await client.get(url, params=params)
            google_response.raise_for_status()
            search_data = google_response.json()
            search_items: List[Dict[str, Any]] = search_data.get("items", [])

            if not search_items:
                logger.warning(f"Google Search for '{search_query}' returned no results.")
                return "Web search returned no results."

            # 2. Asynchronously scrape the top N results
            tasks = []
            for item in search_items[:num_results_to_scrape]:
                link = item.get('link')
                if link:
                    tasks.append(scrape_url_content(link, client))

            scraped_contents = await asyncio.gather(*tasks)

            # 3. Format all the collected information for the AI
            final_report = f"Research report for the query: '{search_query}'\n\n"
            final_report += "--- Search Snippets ---\n"
            for i, item in enumerate(search_items[:num_results_to_scrape]):
                title = item.get('title', 'No Title')
                snippet = item.get('snippet', 'No snippet.').replace("\n", " ")
                final_report += f"{i + 1}. {title}: {snippet}\n"

            final_report += "\n--- Detailed Content from Top Pages ---\n"
            for i, content in enumerate(scraped_contents):
                final_report += f"\n\n>> Content from Result {i + 1}:\n"
                final_report += content + "\n"

            final_report += "\n--- End of Report ---\nBased on the comprehensive information above, please provide a direct answer to the user's original query."

            logger.debug(f"Generated research report for Gemini. Length: {len(final_report)} chars.")
            return final_report

    except httpx.HTTPStatusError as e:
        error_body = e.response.text
        logger.error(f"HTTP error during Google Search for '{search_query}': {e}\nResponse: {error_body}")
        return f"An error occurred while contacting the search service: {e}"
    except Exception as e:
        logger.error(f"An unexpected error occurred during Google Search for '{search_query}': {e}", exc_info=True)
        return f"An unexpected error occurred during the web search: {e}"