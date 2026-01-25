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

load_dotenv()
API_KEY = os.getenv("API_KEY")
BASE_URL = os.getenv("BASE_URL")  

MOVIE_IDS = [
    0, 299534, 19995, 140607, 299536, 597, 135397,
    420818, 24428, 168259, 99861, 284054, 12445,
    181808, 330457, 351286, 109445, 321612, 260513
]


TIMEOUT = 10
RETRY_TOTAL = 3
RETRY_BACKOFF = 1.5
RATE_LIMIT_SLEEP = 0.25
LOG_DIR = "../logs"
os.makedirs(LOG_DIR, exist_ok=True)


# Logging setup

logging.basicConfig(
    filename=os.path.join(LOG_DIR, f"tmdb_extraction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


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
        response.raise_for_status()  # Raises HTTPError for 4xx/5xx
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        logger.error("HTTP error | url=%s | error=%s", url, http_err)
    except requests.exceptions.RequestException as req_err:
        logger.error("Request exception | url=%s | error=%s", url, req_err)
    except json.JSONDecodeError as json_err:
        logger.error("JSON decode error | url=%s | error=%s", url, json_err)
    return None

def fetch_movie_with_credits(movie_id: int) -> dict | None:
    if movie_id == 0:
        logger.warning("Skipping movie_id=0 (placeholder)")
        return None
    url = f"{BASE_URL}{movie_id}?api_key={API_KEY}&append_to_response=credits"
    movie_data = get_json(url)
    if not movie_data or "id" not in movie_data:
        logger.warning("Invalid or empty movie payload | movie_id=%s", movie_id)
        return None
    return movie_data


#Extraction of data 
def extract_tmdb_movies_as_dataframe() -> pd.DataFrame:
    """Extract TMDB movies and return as a Pandas DataFrame with error handling."""
    records = []

    for movie_id in MOVIE_IDS:
        try:
            logger.info("Fetching movie_id=%s", movie_id)
            movie_payload = fetch_movie_with_credits(movie_id)
            if movie_payload:
                records.append(movie_payload)
            else:
                logger.warning("Movie skipped | movie_id=%s", movie_id)
        except Exception as e:
            logger.exception("Unexpected error while fetching movie_id=%s | error=%s", movie_id, e)
        time.sleep(RATE_LIMIT_SLEEP)

    if not records:
        logger.error("No movies were fetched successfully. Exiting extraction.")
        return pd.DataFrame()  # Return empty DataFrame

    try:
        df_movies = pd.DataFrame(records)
        logger.info("Extraction completed successfully | records=%s", len(df_movies))
        return df_movies
    except Exception as e:
        logger.exception("Failed to create DataFrame | error=%s", e)
        return pd.DataFrame()


def save_dataframe(df: pd.DataFrame, json_path: str):
    try:
        os.makedirs(os.path.dirname(json_path), exist_ok=True)
        df.to_json(json_path, orient="records", indent=2)
        logger.info("Saved DataFrame to JSON | path=%s", json_path)
    except Exception as e:
        logger.exception("Failed to save DataFrame | path=%s | error=%s", json_path, e)

if __name__ == "__main__":
    logger.info("===== TMDB Extraction Pipeline Started =====")
    df_movies = extract_tmdb_movies_as_dataframe()
    if not df_movies.empty:
        save_dataframe(df_movies, "../data/raw/tmdb_movies_raw.json")
    else:
        logger.error("No data to save. Pipeline completed with errors.")
    logger.info("===== TMDB Extraction Pipeline Completed =====")
