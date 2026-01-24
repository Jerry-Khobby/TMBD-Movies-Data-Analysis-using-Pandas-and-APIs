import pandas as pd
import numpy as np
import logging
import os
from typing import Dict

# Setup logger
logger = logging.getLogger("tmdb_advanced")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def advanced_tmdb_pandas(df: pd.DataFrame, top_n: int = 10, output_dir: str = None) -> Dict[str, pd.DataFrame]:
    """
    Advanced TMDB analysis in Pandas:
    - KPI rankings
    - Advanced searches
    - Franchise vs standalone
    - Most successful franchises & directors
    """
    logger.info("Starting advanced TMDB analysis")
    df = df.copy()

    # Feature engineering
    df['profit'] = df['revenue_musd'] - df['budget_musd']
    df['roi'] = df['revenue_musd'] / df['budget_musd']
    df.loc[df['budget_musd'] < 10, 'roi'] = np.nan

    results = {}

    # Helper: rank top_n by column
    def rank(df_, col, ascending=False, filter_func=None):
        if filter_func:
            df_ = df_[filter_func(df_)]
        df_ranked = df_.sort_values(by=col, ascending=ascending).head(top_n).copy()
        df_ranked['rank'] = np.arange(1, len(df_ranked) + 1)
        return df_ranked

    # KPI rankings
    kpis = [
        {"name": "highest_revenue", "col": "revenue_musd"},
        {"name": "highest_budget", "col": "budget_musd"},
        {"name": "highest_profit", "col": "profit"},
        {"name": "lowest_profit", "col": "profit", "ascending": True},
        {"name": "highest_roi", "col": "roi"},
        {"name": "lowest_roi", "col": "roi", "ascending": True},
        {"name": "most_voted", "col": "vote_count"},
        {"name": "highest_rated", "col": "vote_average", "filter": lambda d: d['vote_count'] >= 10},
        {"name": "lowest_rated", "col": "vote_average", "ascending": True, "filter": lambda d: d['vote_count'] >= 10},
        {"name": "most_popular", "col": "popularity"}
    ]

    for kpi in kpis:
        logger.info(f"Computing KPI: {kpi['name']}")
        df_kpi = rank(
            df,
            col=kpi['col'],
            ascending=kpi.get('ascending', False),
            filter_func=kpi.get('filter', None)
        )
        results[kpi['name']] = df_kpi

    # Advanced Searches
    logger.info("Advanced search: Bruce Willis in Sci-Fi/Action")
    search1 = df[
        df['genres'].str.contains('Science Fiction', na=False) &
        df['genres'].str.contains('Action', na=False) &
        df['cast'].str.contains('Bruce Willis', na=False)
    ].sort_values(by='vote_average', ascending=False).head(top_n)
    results["search_bruce_willis_sci_fi_action"] = search1

    logger.info("Advanced search: Uma Thurman + Quentin Tarantino")
    search2 = df[
        df['cast'].str.contains('Uma Thurman', na=False) &
        (df['director'] == 'Quentin Tarantino')
    ].sort_values(by='runtime', ascending=True).head(top_n)
    results["search_uma_thurman_tarantino"] = search2

    # Franchise vs Standalone
    logger.info("Analyzing franchise vs standalone movies")
    df['is_franchise'] = df['belongs_to_collection'].notna()
    franchise_stats = df.groupby('is_franchise').agg(
        mean_revenue=('revenue_musd', 'mean'),
        median_roi=('roi', 'median'),
        mean_budget=('budget_musd', 'mean'),
        mean_popularity=('popularity', 'mean'),
        mean_rating=('vote_average', 'mean')
    ).reset_index()
    results["franchise_vs_standalone"] = franchise_stats

    # Most successful franchises
    logger.info("Computing most successful franchises")
    franchises = df[df['belongs_to_collection'].notna()].groupby('belongs_to_collection').agg(
        total_movies=('title', 'count'),
        total_budget=('budget_musd', 'sum'),
        mean_budget=('budget_musd', 'mean'),
        total_revenue=('revenue_musd', 'sum'),
        mean_revenue=('revenue_musd', 'mean'),
        mean_rating=('vote_average', 'mean')
    ).sort_values(by='total_revenue', ascending=False).reset_index()
    results["most_successful_franchises"] = franchises.head(top_n)

    # Most successful directors
    logger.info("Computing most successful directors")
    directors = df.groupby('director').agg(
        total_movies=('title', 'count'),
        total_revenue=('revenue_musd', 'sum'),
        mean_rating=('vote_average', 'mean')
    ).sort_values(by='total_revenue', ascending=False).reset_index()
    results["most_successful_directors"] = directors.head(top_n)

    # Save results if output_dir provided
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"Saving results to directory: {output_dir}")
        for name, df_res in results.items():
            path = os.path.join(output_dir, f"{name}.csv")
            df_res.to_csv(path, index=False)
            logger.info(f"Saved '{name}' to {path}")

    logger.info("Advanced TMDB analysis completed successfully")
    return results
