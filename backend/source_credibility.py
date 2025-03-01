import os 
import requests
import logging
from functools import lru_cache
from json import JSONDecodeError
from urllib.parse import urlparse

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load API Key from Environment Variables
GOOGLE_FACT_CHECK_API_KEY = os.getenv("GOOGLE_FACT_CHECK_API_KEY")

# Google Fact Check API Endpoint
FACT_CHECK_API_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

@lru_cache(maxsize=50)  # Cache up to 50 sources for efficiency
def check_source_credibility(source_url):
    """
    Checks the credibility of a news source by determining whether it appears in Google Fact Check results.
    """
    if not GOOGLE_FACT_CHECK_API_KEY:
        logging.error("Google Fact Check API key is missing!")
        return {"error": "Missing API key"}

    # Extract domain name from URL
    parsed_url = urlparse(source_url)
    domain = parsed_url.netloc or source_url

    params = {
        "query": domain,
        "key": GOOGLE_FACT_CHECK_API_KEY
    }

    try:
        logging.info(f"Checking credibility for: {domain}")
        response = requests.get(FACT_CHECK_API_URL, params=params, timeout=5)
        response.raise_for_status()

        try:
            data = response.json()
        except JSONDecodeError:
            logging.error("Invalid JSON response from Google Fact Check API")
            return {"error": "Invalid API response"}

        claims = data.get("claims", [])
        if not claims:
            logging.info(f"No fact-checks found for {domain}")
            return {"source": domain, "credibility_score": "Unverified"}

        # Extract credibility info from claims
        fact_check_results = []
        for claim in claims:
            claim_reviews = claim.get("claimReview", [])
            if claim_reviews:
                review = claim_reviews[0]
                textual_rating = review.get("textualRating", "No rating available")
                publisher = review.get("publisher", {}).get("name", "Unknown publisher")
                review_url = review.get("url", "No URL available")

                fact_check_results.append({
                    "rating": textual_rating,
                    "fact_check_source": publisher,
                    "fact_check_url": review_url
                })

        return {
            "source": domain,
            "credibility_score": "Verified",
            "fact_check_results": fact_check_results
        }

    except requests.Timeout:
        logging.error("Request to Google Fact Check API timed out")
        return {"error": "Fact check request timed out"}
    except requests.RequestException as e:
        logging.error(f"Error with Google Fact Check API: {e}")
        return {"error": "Failed to fetch fact-check data"}

# Example usage
if __name__ == "__main__":
    source = "https://example-news-site.com"
    credibility_info = check_source_credibility(source)
    print(credibility_info)