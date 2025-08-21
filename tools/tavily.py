


import os
import httpx
from typing import List, Dict
from dotenv import load_dotenv
from core.utils import log

# Load environment variables
load_dotenv()

# Base configuration
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
TAVILY_ENDPOINT = "https://api.tavily.com/search"

def tavily_search(query: str, k: int = 5) -> List[Dict]:
    if not TAVILY_API_KEY:
        raise ValueError("TAVILY_API_KEY is not set in your environment variables.")

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "basic",
        "max_results": int(k),
        "include_answer": True
    }

    log("tavily", f"Sending search request for: {query}")
    
    try:
        response = httpx.post(TAVILY_ENDPOINT, json=payload, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        log("tavily", f"Error during Tavily search: {e}")
        return []
