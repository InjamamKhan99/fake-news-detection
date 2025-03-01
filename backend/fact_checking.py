import os
import requests
import logging
from json import JSONDecodeError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load Google Fact Check API Key
GOOGLE_FACT_CHECK_API_KEY = os.getenv("GOOGLE_FACT_CHECK_API_KEY")
FACT_CHECK_API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

def fact_check_news(news_text):
    """
    Queries Google Fact Check API for the given news text.
    """
    if not GOOGLE_FACT_CHECK_API_KEY:
        logging.error("Google Fact Check API key is missing.")
        return {"error": "Google Fact Check API key is not configured."}

    params = {
        "query": news_text,
        "key": GOOGLE_FACT_CHECK_API_KEY
    }

    try:
        response = requests.get(FACT_CHECK_API_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        claims = data.get("claims", [])
        if not claims:
            return {"result": "No relevant fact-checks found."}

        # Extract the most relevant fact-check
        claim = claims[0]
        text = claim.get("text", "No claim text available.")
        claimant = claim.get("claimant", "Unknown source")
        rating = claim.get("claimReview", [{}])[0].get("textualRating", "No rating available")
        
        return {
            "query": news_text,
            "fact_check": {
                "claim": text,
                "source": claimant,
                "rating": rating
            }
        }
    except requests.Timeout:
        logging.error("Fact check request timed out.")
        return {"error": "Fact check service timed out."}
    except requests.RequestException as e:
        logging.error(f"Error connecting to Fact Check API: {e}")
        return {"error": "Failed to fetch fact-check data."}
    except JSONDecodeError:
        logging.error("Invalid JSON response from Google Fact Check API.")
        return {"error": "Unexpected response format from Fact Check API."}

# Example usage
if __name__ == "__main__":
    news = "COVID-19 vaccines contain microchips."
    result = fact_check_news(news)
    print(result)
