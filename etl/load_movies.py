# load_movies.py
import pandas as pd
import logging
from datetime import datetime
from etl.transform import clean_tmdb
import os

# Setup logging
LOG_DIR = "../logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"tmdb_load_{datetime.now():%Y%m%d_%H%M%S}.log")

logger = logging.getLogger("tmdb_load")
logger.setLevel(logging.INFO)
fh = logging.FileHandler(log_file)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

logger.info("Starting TMDB load and cleaning pipeline")

try:
    # Path to raw CSV
    raw_csv_path = "../data/raw/tmdb_movies_raw.json"
    logger.info(f"Loading raw CSV from {raw_csv_path}")
    df_raw = pd.read_json(raw_csv_path,orient="records",indent=2)

    # Clean data
    logger.info("Cleaning and transforming raw data")
    df_clean = clean_tmdb(df_raw)

    # Save cleaned CSV
    output_csv = "../data/clean/tmdb_movies_clean.csv"
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df_clean.to_csv(output_csv, index=False)
    logger.info(f"Cleaned CSV saved at: {output_csv}")

except Exception as e:
    logger.exception(f"An error occurred during loading and cleaning: {e}")

logger.info("TMDB load and cleaning pipeline finished")
