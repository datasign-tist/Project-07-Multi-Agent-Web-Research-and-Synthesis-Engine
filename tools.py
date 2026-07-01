from langchain.tools import tool # Adding tools
import requests # Because of Web Scraping external requests

from bs4 import BeautifulSoup #Web Scraping
from tavily import TavilyClient # connecting tavily tool creation

import os
from dotenv import load_dotenv # loading api keys

load_dotenv()

## Creating Tavily API Key

tavily = TavilyClient(api_key = os.getenv("TAVILY_API_KEY")) # loading tavily api key

## adding tool decorator

@tool
def web_search(query: str) -> str:
    """
    Search the web for the latest information using Tavily.
    Returns structured results including titles, URLs, and relevant content snippets.
    """
    try:
        # Perform the search
        results = tavily.search(query=query, search_depth="advanced", max_results=5)
        
        # Check if results exist
        if not results.get('results'):
            return "No search results found for this query."

        # Format output for the LLM
        formatted_results = []
        for r in results['results']:
            # Cleaning the snippet: stripping whitespace and handling potential empty content
            snippet = " ".join(r.get('content', '').split())
            
            result_str = (
                f"Title: {r.get('title', 'No Title')}\n"
                f"URL: {r.get('url', 'No URL')}\n"
                f"Snippet: {snippet[:400]}" # Slightly increased to 400 for more context
            )
            formatted_results.append(result_str)

        return "\n\n---\n\n".join(formatted_results)

    except Exception as e:
        return f"An error occurred during web search: {str(e)}"

## adding the 2nd - Web Scraper tool - using beautiful_soup

@tool
def scrape_url(url: str) -> str:
    """
    Scrape and return clean text content from a URL.
    Use this when the LLM needs deeper information beyond search snippets.
    """
    try:
        # 1. Added a reasonable User-Agent to avoid immediate 403 blocks
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, timeout=10, headers=headers) # timeout for waiting time, headers to act as a human
        resp.raise_for_status() # Check for HTTP errors

        # 2. Parse and clean
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Remove noise-heavy elements that distract the LLM
        for element in soup(["script", "style", "nav", "footer", "header", "noscript"]): # denoise parts
            element.decompose()

        # 3. Get text, clean whitespace, and limit to ~3000 chars 
        # (Tokens represent ~0.75 words, so 3000 chars is efficient for context windows)
        text = soup.get_text(separator=" ", strip=True)
        return " ".join(text.split())[:3000]

    except requests.exceptions.RequestException as e:
        return f"Error scraping {url}: {str(e)}"
    except Exception as e:
        return f"An unexpected error occurred while processing {url}: {str(e)}"