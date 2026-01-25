import os
import logging
from datetime import datetime
import pandas as pd

from etl.extract_movies import extract_tmdb_movies_as_dataframe
from etl.transform import clean_tmdb
from kpis.kpis_ranking import compute_tmdb_kpis_and_save
from kpis.advanced import advanced_tmdb_pandas
from visualisation import visualize_tmdb

LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)

log_file = os.path.join(
    LOG_DIR, f"tmdb_pipeline_{datetime.now():%Y%m%d_%H%M%S}.log"
)

logger = logging.getLogger("tmdb_pipeline")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    fh = logging.FileHandler(log_file)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)


def main():
    try:
        logger.info("===== TMDB Pipeline Started =====")

        logger.info("Step 1: Extracting raw movie data")
        df_raw = extract_tmdb_movies_as_dataframe()
        raw_path = "./data/raw/tmdb_movies_raw.json"
        os.makedirs(os.path.dirname(raw_path), exist_ok=True)
        df_raw.to_json(raw_path, orient="records", indent=2)

        logger.info("Step 2: Cleaning and transforming data")
        df_clean = clean_tmdb(df_raw)
        clean_path = "./data/clean/tmdb_movies_clean.csv"
        os.makedirs(os.path.dirname(clean_path), exist_ok=True)
        df_clean.to_csv(clean_path, index=False)

        logger.info("Step 3: Computing KPI rankings")
        kpi_dir = "./data/kpi_results"
        compute_tmdb_kpis_and_save(df_clean, top_n=10, output_dir=kpi_dir)

        logger.info("Step 4: Computing advanced KPIs")
        advanced_tmdb_pandas(df_clean, top_n=10, output_dir=f"{kpi_dir}/advanced")

        logger.info("Step 5: Generating visualizations")
        df_kpi = pd.read_csv(f"{kpi_dir}/tmdb_with_roi_profit.csv")
        visualize_tmdb(df_kpi, output_dir="./data/diagrams")

        logger.info("===== TMDB Pipeline Completed Successfully =====")

    except Exception:
        logger.exception("Pipeline failed")
        raise


if __name__ == "__main__":
    main()
