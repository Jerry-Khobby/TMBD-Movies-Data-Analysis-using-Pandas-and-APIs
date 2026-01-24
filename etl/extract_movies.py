import os
import time
import logging
import requests
import pandas as pd
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from datetime import datetime
import json

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")  

MOVIE_IDS = [
    0, 299534, 19995, 140607, 299536, 597, 135397,
    420818, 24428, 168259, 99861, 284054, 12445,
    181808, 330457, 351286, 109445, 321612, 260513
]

# Constants
TIMEOUT = 10
RETRY_TOTAL = 3
RETRY_BACKOFF = 1.5
RATE_LIMIT_SLEEP = 0.25
LOG_DIR = "../logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Logging setup
log_file = os.path.join(
    LOG_DIR, f"tmdb_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

# Requests session with retries
def create_session() -> requests.Session:
    retry_strategy = Retry(
        total=RETRY_TOTAL,
        backoff_factor=RETRY_BACKOFF,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

session = create_session()

def get_json(url: str) -> dict | None:
    try:
        response = session.get(url, timeout=TIMEOUT)
        if response.status_code != 200:
            logging.error("Non-200 response | status=%s | url=%s", response.status_code, url)
            return None
        return response.json()
    except requests.exceptions.RequestException as exc:
        logging.error("HTTP request failed | url=%s | error=%s", url, exc)
        return None

def fetch_movie_with_credits(movie_id: int) -> dict | None:
    if movie_id == 0:
        return None
    url = f"{BASE_URL}{movie_id}?api_key={API_KEY}&append_to_response=credits"
    movie_data = get_json(url)
    if not movie_data or "id" not in movie_data:
        logging.warning("Invalid movie payload | movie_id=%s", movie_id)
        return None
    return movie_data

def extract_tmdb_movies_as_dataframe() -> pd.DataFrame:
    """Extract TMDB movies and return as a Pandas DataFrame"""
    records = []

    for movie_id in MOVIE_IDS:
        logging.info("Extracting movie_id=%s", movie_id)
        movie_payload = fetch_movie_with_credits(movie_id)
        if movie_payload:
            records.append(movie_payload)
        time.sleep(RATE_LIMIT_SLEEP)

    # Create a DataFrame directly
    df_movies = pd.DataFrame(records)
    logging.info("Extraction completed | records=%s", len(df_movies))

    return df_movies

if __name__ == "__main__":
    df_movies = extract_tmdb_movies_as_dataframe()

    # Optional: save to JSON
    output_path = "../data/raw/tmdb_movies_raw.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_movies.to_json(output_path, orient="records", indent=2)
    logging.info("Saved DataFrame to JSON | path=%s", output_path)

    # Optional: save to CSV as well
"""     output_csv = "../data/raw/tmdb_movies_raw.csv"
    df_movies.to_csv(output_csv, index=False)
    logging.info("Saved DataFrame to CSV | path=%s", output_csv) """
