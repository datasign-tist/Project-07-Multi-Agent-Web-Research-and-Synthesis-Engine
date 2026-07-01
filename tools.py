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
def web_search(query : str) -> str:

    """ Search the web for latest imformation
        Returns --> Titles, URL's and Snippets """
    
    results = tavily.search(query = query, max_results = 5) # query will pass through tavily for web search with max_results to save tokens

    ## Fetching results output in a clean way
    outputs = []
    for r in results['results'] :
        outputs.append(
                       f"Title : {r['title']}\nURL  : {r['url']}\nSnippet : {r['content'][:300]}\r"
                      )

    return "\n----\n".join(outputs)

print(web_search("What is a data scientist?"))


    
