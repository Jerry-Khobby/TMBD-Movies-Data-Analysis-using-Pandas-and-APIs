import pandas as pd
import numpy as np
import logging
import json
from typing import Dict
from datetime import datetime
import os 


def log_event(logger: logging.Logger, level: str, event_type: str, message: str, **kwargs):
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level.upper(),
        "event_type": event_type,
        "message": message,
        **kwargs
    }

    if level.lower() == "info":
        logger.info(json.dumps(payload))
    elif level.lower() == "warning":
        logger.warning(json.dumps(payload))
    elif level.lower() == "error":
        logger.error(json.dumps(payload))
    else:
        logger.debug(json.dumps(payload))


def advanced_tmdb(df: pd.DataFrame, top_n: int = 10,logger:logging.Logger=None) -> Dict[str, pd.DataFrame]:
    """
    Advanced TMDB analysis with structured JSON logging.
    """

    log_event(logger,"info", "pipeline_start", "Starting advanced TMDB analysis")

    df = df.copy()


    # Feature Engineering
    df['profit'] = df['revenue_musd'] - df['budget_musd']
    df['roi'] = df['revenue_musd'] / df['budget_musd']
    df.loc[df['budget_musd'] < 10, 'roi'] = np.nan

    log_event(
        logger,
        "info",
        "feature_engineering",
        "Computed profit and ROI",
        total_rows=len(df)
    )

    results = {}

    def rank(df_, col, ascending=False, filter_func=None):
        if filter_func:
            df_ = df_[filter_func(df_)]
        df_ranked = df_.sort_values(by=col, ascending=ascending).head(top_n).copy()
        df_ranked['rank'] = np.arange(1, len(df_ranked) + 1)
        return df_ranked

    # KPI Rankings
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

        log_event(
            logger,
            "info",
            "kpi_computation_start",
            f"Computing KPI {kpi['name']}",
            metric=kpi["col"]
        )

        df_kpi = rank(
            df,
            col=kpi['col'],
            ascending=kpi.get('ascending', False),
            filter_func=kpi.get('filter', None)
        )

        results[kpi['name']] = df_kpi

        if not df_kpi.empty:
            top_row = df_kpi.iloc[0]

            log_event(
                logger,
                "info",
                "kpi_result",
                "KPI computed successfully",
                kpi_name=kpi["name"],
                metric=kpi["col"],
                top_movie=top_row.get("title", None),
                top_value=float(top_row[kpi["col"]]) if pd.notna(top_row[kpi["col"]]) else None,
                rows_returned=len(df_kpi)
            )
        else:
            log_event(
                logger,
                "warning",
                "kpi_empty_result",
                f"No results for KPI {kpi['name']}",
                kpi_name=kpi["name"]
            )


    # Advanced Searches
    log_event(logger,"info", "advanced_search_start", "Bruce Willis Sci-Fi/Action search")

    search1 = df[
        df['genres'].str.contains('Science Fiction', na=False) &
        df['genres'].str.contains('Action', na=False) &
        df['cast'].str.contains('Bruce Willis', na=False)
    ].sort_values(by='vote_average', ascending=False).head(top_n)

    results["search_bruce_willis_sci_fi_action"] = search1

    log_event(
        logger,
        "info",
        "advanced_search_result",
        "Completed Bruce Willis search",
        rows_returned=len(search1)
    )

    log_event(logger, "info", "advanced_search_start", "Uma Thurman + Quentin Tarantino search")

    search2 = df[
        df['cast'].str.contains('Uma Thurman', na=False) &
        (df['director'] == 'Quentin Tarantino')
    ].sort_values(by='runtime', ascending=True).head(top_n)

    results["search_uma_thurman_tarantino"] = search2

    log_event(
        logger,
        "info",
        "advanced_search_result",
        "Completed Uma Thurman search",
        rows_returned=len(search2)
    )

    # Franchise vs Standalone
    log_event(logger, "info", "franchise_analysis_start", "Analyzing franchise vs standalone")

    df['is_franchise'] = df['belongs_to_collection'].notna()

    franchise_stats = df.groupby('is_franchise').agg(
        mean_revenue=('revenue_musd', 'mean'),
        median_roi=('roi', 'median'),
        mean_budget=('budget_musd', 'mean'),
        mean_popularity=('popularity', 'mean'),
        mean_rating=('vote_average', 'mean')
    ).reset_index()

    results["franchise_vs_standalone"] = franchise_stats

    log_event(
        logger,
        "info",
        "franchise_analysis_result",
        "Computed franchise vs standalone stats",
        groups=len(franchise_stats)
    )

    # Most Successful Franchises
    log_event(logger, "info", "franchise_ranking_start", "Ranking franchises by total revenue")

    franchises = df[df['belongs_to_collection'].notna()].groupby('belongs_to_collection').agg(
        total_movies=('title', 'count'),
        total_budget=('budget_musd', 'sum'),
        total_revenue=('revenue_musd', 'sum'),
        mean_rating=('vote_average', 'mean')
    ).sort_values(by='total_revenue', ascending=False).reset_index()

    results["most_successful_franchises"] = franchises.head(top_n)

    log_event(  
        logger,
        "info",
        "franchise_ranking_result",
        "Top franchises computed",
        rows_returned=len(results["most_successful_franchises"])
    )

    # Most Successful Directors
    log_event(logger, "info", "director_ranking_start", "Ranking directors by total revenue")

    directors = df.groupby('director').agg(
        total_movies=('title', 'count'),
        total_revenue=('revenue_musd', 'sum'),
        mean_rating=('vote_average', 'mean')
    ).sort_values(by='total_revenue', ascending=False).reset_index()

    results["most_successful_directors"] = directors.head(top_n)

    log_event(
        logger,
        "info",
        "director_ranking_result",
        "Top directors computed",
        rows_returned=len(results["most_successful_directors"])
    )

    log_event(logger, "info", "pipeline_complete", "Advanced TMDB analysis completed")

    return results,df
