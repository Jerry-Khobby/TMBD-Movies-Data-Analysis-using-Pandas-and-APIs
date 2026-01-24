import pandas as pd
import numpy as np
import os
from typing import Dict
import logging

# Setup logger
logger = logging.getLogger("tmdb_kpi_save")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def compute_tmdb_kpis_and_save(df: pd.DataFrame, top_n: int = 10, output_dir: str = None) -> Dict[str, pd.DataFrame]:
    """
    Compute KPI rankings for TMDB movies dataset using Pandas,
    save KPI CSVs AND a new dataset with ROI and profit added.
    """
    logger.info("Starting KPI computation for TMDB movies")
    df = df.copy()

    # --- Compute profit and ROI ---
    logger.info("Computing profit and ROI")
    df['profit'] = df['revenue_musd'] - df['budget_musd']
    df['roi'] = df['revenue_musd'] / df['budget_musd']
    df.loc[df['budget_musd'] < 10, 'roi'] = np.nan  # Only consider movies with budget >= 10M for ROI

    # --- Define KPIs ---
    kpis = [
        {"name": "highest_revenue", "col": "revenue_musd", "asc": False},
        {"name": "highest_budget", "col": "budget_musd", "asc": False},
        {"name": "highest_profit", "col": "profit", "asc": False},
        {"name": "lowest_profit", "col": "profit", "asc": True},
        {"name": "highest_roi", "col": "roi", "asc": False},
        {"name": "lowest_roi", "col": "roi", "asc": True},
        {"name": "most_voted", "col": "vote_count", "asc": False},
        {"name": "highest_rated", "col": "vote_average", "asc": False, "filter": lambda d: d['vote_count'] >= 10},
        {"name": "lowest_rated", "col": "vote_average", "asc": True, "filter": lambda d: d['vote_count'] >= 10},
        {"name": "most_popular", "col": "popularity", "asc": False},
    ]

    results = {}

    # --- Generic ranking function ---
    def rank_movies(df_, col, asc=True, filter_func=None):
        if filter_func:
            df_ = df_[filter_func(df_)]
        ranked = df_.sort_values(by=col, ascending=asc).head(top_n).copy()
        ranked['rank'] = np.arange(1, len(ranked) + 1)
        return ranked

    # --- Compute each KPI ---
    for kpi in kpis:
        logger.info(f"Computing KPI: {kpi['name']}")
        df_kpi = rank_movies(
            df,
            col=kpi['col'],
            asc=kpi.get('asc', False),
            filter_func=kpi.get('filter', None)
        )
        results[kpi['name']] = df_kpi

    # --- Save KPIs and dataset if output_dir is provided ---
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Saving KPI results and updated dataset to directory: {output_dir}")

        # Save each KPI
        for kpi_name, df_kpi in results.items():
            path = os.path.join(output_dir, f"{kpi_name}.csv")
            df_kpi.to_csv(path, index=False)
            logger.info(f"Saved KPI '{kpi_name}' to {path}")

        # Save full dataset with profit and ROI
        dataset_path = os.path.join(output_dir, "tmdb_with_roi_profit.csv")
        df.to_csv(dataset_path, index=False)
        logger.info(f"Saved full dataset with 'profit' and 'roi' to {dataset_path}")

    logger.info("KPI computation and dataset saving completed successfully")
    return results





def save_kpi_results(results: Dict[str, pd.DataFrame], output_dir: str):
    """
    Save each KPI DataFrame to a CSV file.

    Parameters
    ----------
    results : dict
        Dictionary of KPI DataFrames keyed by KPI name.
    output_dir : str
        Directory where CSV files will be saved.
    """
    os.makedirs(output_dir, exist_ok=True)
    logger.info(f"Saving KPI results to directory: {output_dir}")

    for kpi_name, df_kpi in results.items():
        file_path = os.path.join(output_dir, f"{kpi_name}.csv")
        df_kpi.to_csv(file_path, index=False)
        logger.info(f"Saved KPI '{kpi_name}' to {file_path}")

# Example usage:
# df_clean = pd.read_csv("../data/clean/tmdb_movies_clean.csv")
# kpi_results = compute_tmdb_kpis_pandas(df_clean, top_n=5)
# kpi_results['highest_profit']
