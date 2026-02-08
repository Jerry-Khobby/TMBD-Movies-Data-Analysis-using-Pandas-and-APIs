import pandas as pd
import numpy as np
from typing import Dict
import logging
import json
from datetime import datetime




def log_event(logger: logging.Logger, level: str, event_type: str, message: str, **kwargs):
    """
    Structured JSON logger.
    """
    if logger is None:
        raise ValueError("Logger must be provided to log_event")
    
    log_payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "level": level.upper(),
        "event_type": event_type,
        "message": message,
        **kwargs
    }

    if level.lower() == "info":
        logger.info(json.dumps(log_payload))
    elif level.lower() == "warning":
        logger.warning(json.dumps(log_payload))
    elif level.lower() == "error":
        logger.error(json.dumps(log_payload))
    else:
        logger.debug(json.dumps(log_payload))


def compute_tmdb_kpis(df: pd.DataFrame, top_n: int = 10,logger:logging.Logger=None) -> Dict[str, pd.DataFrame]:
    """
    Compute KPI rankings for TMDB movies dataset.
    Uses structured JSON logging.
    """
    log_event(logger, "info", "pipeline_start", "Starting KPI computation")

    df = df.copy()

    # --- Compute profit and ROI ---
    df['profit'] = df['revenue_musd'] - df['budget_musd']
    df['roi'] = df['revenue_musd'] / df['budget_musd']
    df.loc[df['budget_musd'] < 10, 'roi'] = np.nan

    log_event(
        logger,
        "info",
        "feature_engineering",
        "Computed profit and ROI columns",
        total_rows=len(df)
    )

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

    def rank_movies(df_, col, asc=True, filter_func=None):
        if filter_func:
            df_ = df_[filter_func(df_)]
        ranked = df_.sort_values(by=col, ascending=asc).head(top_n).copy()
        ranked['rank'] = np.arange(1, len(ranked) + 1)
        return ranked

    for kpi in kpis:

        log_event(
            logger,
            "info",
            "kpi_computation_start",
            f"Computing KPI: {kpi['name']}",
            metric_column=kpi["col"]
        )

        df_kpi = rank_movies(
            df,
            col=kpi['col'],
            asc=kpi.get('asc', False),
            filter_func=kpi.get('filter', None)
        )

        results[kpi['name']] = df_kpi

        if not df_kpi.empty:
            top_row = df_kpi.iloc[0]

            log_event(
                logger,
                "info",
                "kpi_result",
                f"KPI computed successfully",
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
                f"No results for KPI: {kpi['name']}",
                kpi_name=kpi["name"]
            )

    log_event(logger,"info", "pipeline_complete", "KPI computation completed")

    return results
