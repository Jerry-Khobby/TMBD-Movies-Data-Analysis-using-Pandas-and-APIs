import pandas as pd
import numpy as np
import logging
from datetime import datetime

# Setup module-level logger
logger = logging.getLogger(__name__)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)


def clean_tmdb(df: pd.DataFrame, validate: bool = True) -> pd.DataFrame:
    """
    Clean and transform raw TMDB DataFrame.
    Handles JSON-like columns, numeric conversions, cast/crew extraction, and filtering.
    """
    try:
        logger.info("Starting TMDB data cleaning pipeline")
        df = df.copy()

        # Step 1: Drop irrelevant columns
        try:
            drop_cols = ['adult', 'imdb_id', 'original_title', 'video', 'homepage']
            df = df.drop(columns=[c for c in drop_cols if c in df.columns])
            logger.info("Dropped irrelevant columns: %s", drop_cols)
        except Exception as e:
            logger.warning("Failed to drop some columns: %s", e)

        # Step 2: Flatten JSON-like columns
        try:
            logger.info("Flattening JSON-like columns (collection, genres, spoken_languages, production)")
            if 'belongs_to_collection' in df.columns:
                df['belongs_to_collection'] = df['belongs_to_collection'].apply(
                    lambda x: x.get('name') if isinstance(x, dict) else np.nan
                )

            if 'genres' in df.columns:
                df['genres'] = df['genres'].apply(
                    lambda x: '|'.join([g['name'] for g in x]) if isinstance(x, list) else np.nan
                )

            if 'spoken_languages' in df.columns:
                df['spoken_languages'] = df['spoken_languages'].apply(
                    lambda x: '|'.join([l.get('english_name', '') for l in x]) if isinstance(x, list) else np.nan
                )

            if 'production_countries' in df.columns:
                df['production_countries'] = df['production_countries'].apply(
                    lambda x: '|'.join([c.get('name', '') for c in x]) if isinstance(x, list) else np.nan
                )

            if 'production_companies' in df.columns:
                df['production_companies'] = df['production_companies'].apply(
                    lambda x: '|'.join([c.get('name', '') for c in x]) if isinstance(x, list) else np.nan
                )

        except Exception as e:
            logger.warning("Failed to flatten JSON-like columns: %s", e)

        # Step 3: Convert numeric columns
        try:
            numeric_cols = ['budget', 'id', 'popularity', 'revenue', 'runtime', 'vote_count', 'vote_average']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')

            if 'release_date' in df.columns:
                df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

            # Handle zeros
            for col in ['budget', 'revenue', 'runtime']:
                if col in df.columns:
                    df.loc[df[col] == 0, col] = np.nan

            # Convert to million USD
            if 'budget' in df.columns:
                df['budget_musd'] = df['budget'] / 1_000_000
            if 'revenue' in df.columns:
                df['revenue_musd'] = df['revenue'] / 1_000_000
            if 'vote_count' in df.columns and 'vote_average' in df.columns:
                df.loc[df['vote_count'] == 0, 'vote_average'] = np.nan

        except Exception as e:
            logger.warning("Failed numeric conversion or adjustments: %s", e)

        # Step 4: Replace placeholder text
        try:
            placeholders = ['No Data', 'N/A', '', 'null']
            for col in ['overview', 'tagline']:
                if col in df.columns:
                    df[col] = df[col].replace(placeholders, np.nan)
        except Exception as e:
            logger.warning("Failed to replace placeholder text: %s", e)

        # Step 5: Extract cast/crew from credits
        try:
            if 'credits' in df.columns:

                def extract_cast(credits):
                    if isinstance(credits, dict):
                        cast_list = credits.get('cast', [])
                        return '|'.join([c.get('name', '') for c in cast_list[:5]]) if cast_list else np.nan
                    return np.nan

                def extract_cast_size(credits):
                    if isinstance(credits, dict):
                        return len(credits.get('cast', []))
                    return 0

                def extract_director(credits):
                    if isinstance(credits, dict):
                        directors = [c.get('name', '') for c in credits.get('crew', []) if c.get('job') == 'Director']
                        return directors[0] if directors else np.nan
                    return np.nan

                def extract_crew_size(credits):
                    if isinstance(credits, dict):
                        return len(credits.get('crew', []))
                    return 0

                df['cast'] = df['credits'].apply(extract_cast)
                df['cast_size'] = df['credits'].apply(extract_cast_size)
                df['director'] = df['credits'].apply(extract_director)
                df['crew_size'] = df['credits'].apply(extract_crew_size)
                df = df.drop(columns=['credits'])
        except Exception as e:
            logger.warning("Failed to extract cast/crew info: %s", e)

        # Step 6: Remove duplicates and incomplete rows
        try:
            if 'id' in df.columns and 'title' in df.columns:
                df = df.drop_duplicates(subset=['id'])
                df = df.dropna(subset=['id', 'title'])
                df = df.dropna(thresh=10)
        except Exception as e:
            logger.warning("Failed to remove duplicates/incomplete rows: %s", e)

        # Step 7: Keep only released movies
        try:
            if 'status' in df.columns:
                df = df[df['status'] == 'Released'].drop(columns=['status'])
        except Exception as e:
            logger.warning("Failed to filter released movies: %s", e)

        # Step 8: Reorder final columns
        final_columns = [
            'id', 'title', 'tagline', 'release_date', 'genres',
            'belongs_to_collection', 'original_language',
            'budget_musd', 'revenue_musd',
            'production_companies', 'production_countries',
            'vote_count', 'vote_average', 'popularity', 'runtime',
            'overview', 'spoken_languages', 'poster_path',
            'cast', 'cast_size', 'director', 'crew_size'
        ]
        df = df[[c for c in final_columns if c in df.columns]]

        # Step 9: Reset index
        df = df.reset_index(drop=True)

        # Step 10: Validation logging
        if validate:
            logger.info("Final row count: %s | Final column count: %s", len(df), len(df.columns))
            for col in ['cast', 'cast_size', 'director', 'crew_size']:
                if col in df.columns:
                    logger.info("%s sample: %s", col, df[col].head(3).tolist())

        logger.info("TMDB data cleaning pipeline completed successfully")
        return df

    except Exception as e:
        logger.exception("Unexpected error in TMDB cleaning pipeline: %s", e)
        return pd.DataFrame()
