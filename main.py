import os
import logging
from datetime import datetime
import pandas as pd

from etl.extract_movies import extract_tmdb_movies,save_dataframe
from etl.transform import clean_tmdb
from kpis.kpis_ranking import compute_tmdb_kpis
from kpis.advanced import advanced_tmdb
from visualisation import visualize_tmdb


LOG_DIR = "./logs"
os.makedirs(LOG_DIR, exist_ok=True)

def get_step_logger(step_name: str) -> logging.Logger:
    """
    Create a dedicated logger for a pipeline step.
    Each step writes to its own log file.
    """
    logger = logging.getLogger(step_name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers if called multiple times
    if not logger.handlers:
        file_handler = logging.FileHandler(
            os.path.join(LOG_DIR, f"{step_name}.log")
        )
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # Prevent propagation to root logger
        logger.propagate = False

    return logger



def main():

    extract_logger = get_step_logger("extract")
    transform_logger = get_step_logger("transform")
    kpi_logger = get_step_logger("kpi")
    advanced_logger = get_step_logger("advanced")
    visualize_logger = get_step_logger("visualize")

    try:
        #extract
        extract_logger.info("Extraction started")
        df_raw = extract_tmdb_movies(logger=extract_logger)
        extract_logger.info("Extraction completed | rows=%s", len(df_raw))
        
        # Save raw CSV
        raw_csv_file = "./data/raw/tmdb_movies_raw.json"
        save_dataframe(df_raw, raw_csv_file)

        #transform
        transform_logger.info("Transformation started")
        df_clean = clean_tmdb(df_raw, logger=transform_logger)
        transform_logger.info("Transformation completed | rows=%s", len(df_clean))

        #kpi
        kpi_logger.info("KPI computation started")
        compute_tmdb_kpis(df_clean, logger=kpi_logger)
        kpi_logger.info("KPI computation completed")

        #advanced
        advanced_logger.info("Advanced analysis started")
        results,df_clean = advanced_tmdb(df_clean, logger=advanced_logger)
        advanced_logger.info("Advanced analysis completed | rows=%s", len(df_clean))
        
        
        output_file = "./data/clean/tmdb_clean_after_kpi.csv"
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        df_clean.to_csv(output_file, index=False)
        advanced_logger.info("Saved clean dataset | path=%s", output_file)
        
        
        #visualisation
        visualize_logger.info("Visualization started")
        visualize_tmdb(df_clean, logger=visualize_logger)
        visualize_logger.info("Visualization completed")

    except Exception as e:
        extract_logger.exception("Pipeline failed")
        raise



if __name__ == "__main__":
    main()
