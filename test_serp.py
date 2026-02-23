import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv("SERPAPI_API_KEY")

def test_search(role, location="India"):
    params = {
        "engine": "google_jobs",
        "q": f"{role} jobs in {location}",
        "hl": "en",
        "gl": "in",
        "api_key": api_key
    }
    
    logger.info(f"Testing with key: {api_key[:5] if api_key else 'NONE'}...")
    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "error" in results:
        logger.error(f"Error: {results['error']}")
    elif "jobs_results" in results:
        logger.info(f"Success! Found {len(results['jobs_results'])} jobs")
        for job in results["jobs_results"][:3]:
            print(f"- {job.get('title')} at {job.get('company_name')}")
    else:
        logger.warning("No jobs_results key found")
        print(results.keys())

if __name__ == "__main__":
    test_search("Data Scientist")
