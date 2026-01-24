import os
import logging
from datetime import datetime

# Import your modules
from etl.extract_movies import extract_tmdb_movies_as_dataframe
from etl.load_movies import clean_tmdb
from kpis.kpis_ranking import compute_tmdb_kpis_pandas, save_kpi_results
from kpis.advanced import advanced_tmdb_pandas
from visualisation import visualize_tmdb
import pandas as pd

# Setup main logger
LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_file = os.path.join(LOG_DIR, f"tmdb_pipeline_{datetime.now():%Y%m%d_%H%M%S}.log")
logger = logging.getLogger("tmdb_pipeline")
logger.setLevel(logging.INFO)
if not logger.handlers:
    fh = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def main():
    try:
        #Extract
        logger.info("Step 1: Extracting raw movie data")
        df_raw = extract_tmdb_movies_as_dataframe()
        raw_path = "./data/raw/tmdb_movies_raw.json"
        os.makedirs(os.path.dirname(raw_path), exist_ok=True)
        df_raw.to_json(raw_path, orient="records", indent=2)
        logger.info(f"Raw movie data saved at: {raw_path}")

        #Load & Clean
        logger.info("Step 2: Cleaning and transforming data")
        df_clean = clean_tmdb(df_raw)
        clean_path = "./data/clean/tmdb_movies_clean.csv"
        os.makedirs(os.path.dirname(clean_path), exist_ok=True)
        df_clean.to_csv(clean_path, index=False)
        logger.info(f"Cleaned data saved at: {clean_path}")

        #KPIs (Basic)
        logger.info("Step 3: Computing KPI rankings")
        kpi_dir = "./data/kpi_results"
        os.makedirs(kpi_dir, exist_ok=True)
        kpi_results = compute_tmdb_kpis_pandas(df_clean, top_n=10)
        save_kpi_results(kpi_results, kpi_dir)
        logger.info(f"KPI rankings saved to directory: {kpi_dir}")

        #Advanced KPIs
        logger.info("Step 4: Computing advanced KPIs")
        adv_kpi_dir = "./data/kpi_results/advanced"
        advanced_results = advanced_tmdb_pandas(df_clean, top_n=10, output_dir=adv_kpi_dir)
        logger.info(f"Advanced KPI results saved to directory: {adv_kpi_dir}")

        #Visualizations
        logger.info("Step 5: Generating visualizations")
        viz_dir = "./data/diagrams"
        plot_paths = visualize_tmdb(df_clean, output_dir=viz_dir)
        logger.info(f"Visualizations saved to directory: {viz_dir}")

        logger.info("===== TMDB Pipeline Completed Successfully =====")
        return {
            "raw_data": raw_path,
            "clean_data": clean_path,
            "kpi_results": kpi_dir,
            "advanced_kpi_results": adv_kpi_dir,
            "visualizations": plot_paths
        }

    except Exception as e:
        logger.exception(f"Pipeline failed: {e}")
        raise e


if __name__ == "__main__":
    results = main()
    print("Pipeline completed. Results directories and files:")
    for k, v in results.items():
        print(f"{k}: {v}")
