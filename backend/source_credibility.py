import os
import requests
import logging
from functools import lru_cache
from json import JSONDecodeError

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load API Key from Environment Variables
GOOGLE_FACT_CHECK_API_KEY = os.getenv("GOOGLE_FACT_CHECK_API_KEY")

# Google Fact Check API Endpoint
FACT_CHECK_API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

@lru_cache(maxsize=50)  # Cache up to 50 sources for efficiency
def check_source_credibility(source_url):
    """
    Checks the credibility of a news source using Google Fact Check API.
    """
    if not GOOGLE_FACT_CHECK_API_KEY:
        logging.error("Google Fact Check API key is missing!")
        return {"error": "Missing API key"}

    params = {
        "query": source_url,
        "key": GOOGLE_FACT_CHECK_API_KEY
    }

    try:
        logging.info(f"Checking credibility for: {source_url}")
        response = requests.get(FACT_CHECK_API_URL, params=params, timeout=5)
        response.raise_for_status()
        
        try:
            data = response.json()
        except JSONDecodeError:
            logging.error("Invalid JSON response from Google Fact Check API")
            return {"error": "Invalid API response"}

        claims = data.get("claims", [])
        if claims:
            return {
                "source": source_url,
                "credibility_score": "Verified",
                "trustworthiness": claims[0].get("textualRating", "Unknown"),
                "api_used": "Google Fact Check API"
            }

    except requests.Timeout:
        logging.error("Request to Google Fact Check API timed out")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error with Google Fact Check API: {e}")

    return {"source": source_url, "credibility_score": "Unverified"}

# Example usage
if __name__ == "__main__":
    source = "https://example-news-site.com"
    credibility_info = check_source_credibility(source)
    print(credibility_info)