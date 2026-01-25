# etl/load_movies.py

import pandas as pd
import logging
import os
from etl.transform import clean_tmdb

# Setup logger
logger = logging.getLogger(__name__)
if not logger.hasHandlers():  # avoid duplicate handlers if imported multiple times
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def load_and_clean_tmdb(raw_json_path: str, output_csv_path: str) -> pd.DataFrame:
    """
    Load raw TMDB JSON, clean it, and save cleaned CSV.
    Returns the cleaned DataFrame or empty DataFrame if errors occur.
    """
    try:
        logger.info("Loading raw TMDB data from %s", raw_json_path)
        if not os.path.exists(raw_json_path):
            logger.error("Raw JSON file not found: %s", raw_json_path)
            return pd.DataFrame()

        try:
            df_raw = pd.read_json(raw_json_path, orient="records")
            logger.info("Loaded raw data | records=%s", len(df_raw))
        except ValueError as ve:
            logger.exception("Failed to parse JSON | error=%s", ve)
            return pd.DataFrame()

        try:
            logger.info("Cleaning TMDB data")
            df_clean = clean_tmdb(df_raw)
            logger.info("Data cleaned successfully | records=%s", len(df_clean))
        except Exception as e:
            logger.exception("Error during cleaning TMDB data | error=%s", e)
            return pd.DataFrame()

        try:
            os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
            df_clean.to_csv(output_csv_path, index=False)
            logger.info("Cleaned data saved to CSV | path=%s", output_csv_path)
        except Exception as e:
            logger.exception("Failed to save cleaned CSV | path=%s | error=%s", output_csv_path, e)

        return df_clean

    except Exception as e:
        logger.exception("Unexpected error in load_and_clean_tmdb | error=%s", e)
        return pd.DataFrame()
