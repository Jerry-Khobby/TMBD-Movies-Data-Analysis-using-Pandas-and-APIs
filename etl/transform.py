import pandas as pd
import numpy as np
import logging
from datetime import datetime

# Setup module-level logger
logger = logging.getLogger("tmdb_cleaning")
logger.setLevel(logging.INFO)

# Add a console handler if not already added
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)


def clean_tmdb(df: pd.DataFrame, validate: bool = True) -> pd.DataFrame:
    logger.info("Starting TMDB data cleaning pipeline")

    # Step 1: Drop irrelevant columns
    logger.info("Dropping irrelevant columns")
    df = df.drop(columns=['adult', 'imdb_id', 'original_title', 'video', 'homepage'], errors='ignore')

    # Step 2: Flatten JSON-like columns
    logger.info("Flattening JSON-like columns (collection, genres, spoken_languages, production)")
    df['belongs_to_collection'] = df['belongs_to_collection'].apply(
        lambda x: x.get('name') if isinstance(x, dict) else np.nan
    )
    df['genres'] = df['genres'].apply(lambda x: '|'.join([g['name'] for g in x]) if isinstance(x, list) else np.nan)
    df['spoken_languages'] = df['spoken_languages'].apply(lambda x: '|'.join([l.get('english_name','') for l in x]) if isinstance(x, list) else np.nan)
    df['production_countries'] = df['production_countries'].apply(lambda x: '|'.join([c.get('name','') for c in x]) if isinstance(x, list) else np.nan)
    df['production_companies'] = df['production_companies'].apply(lambda x: '|'.join([c.get('name','') for c in x]) if isinstance(x, list) else np.nan)

    # Step 3: Convert numeric columns
    logger.info("Converting numeric columns and release_date")
    numeric_cols = ['budget', 'id', 'popularity', 'revenue', 'runtime', 'vote_count', 'vote_average']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df['release_date'] = pd.to_datetime(df['release_date'], errors='coerce')

    # Handle zeros and convert budget/revenue to million USD
    logger.info("Handling zero values and converting budget/revenue to million USD")
    for col in ['budget', 'revenue', 'runtime']:
        df.loc[df[col] == 0, col] = np.nan
    df['budget_musd'] = df['budget'] / 1_000_000
    df['revenue_musd'] = df['revenue'] / 1_000_000
    df.loc[df['vote_count'] == 0, 'vote_average'] = np.nan

    # Replace placeholder text
    logger.info("Replacing placeholder text in overview/tagline")
    placeholders = ['No Data', 'N/A', '', 'null']
    for col in ['overview', 'tagline']:
        df[col] = df[col].replace(placeholders, np.nan)

    # Step 4: Extract cast/crew from credits
    logger.info("Extracting cast and crew information")

    def extract_cast(credits):
        if isinstance(credits, dict):
            cast_list = credits.get('cast', [])
            return '|'.join([c.get('name','') for c in cast_list[:5]]) if cast_list else np.nan
        return np.nan

    def extract_cast_size(credits):
        if isinstance(credits, dict):
            return len(credits.get('cast', []))
        return 0

    def extract_director(credits):
        if isinstance(credits, dict):
            directors = [c.get('name','') for c in credits.get('crew', []) if c.get('job') == 'Director']
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

    # Drop original credits column
    df = df.drop(columns=['credits'])

    # Step 5: Remove duplicates and incomplete rows
    logger.info("Removing duplicates and incomplete rows")
    df = df.drop_duplicates(subset=['id'])
    df = df.dropna(subset=['id', 'title'])
    df = df.dropna(thresh=10)

    # Step 6: Keep only released movies
    if 'status' in df.columns:
        logger.info("Filtering released movies")
        df = df[df['status'] == 'Released'].drop(columns=['status'])

    # Step 7: Reorder final columns
    final_columns = [
        'id', 'title', 'tagline', 'release_date', 'genres',
        'belongs_to_collection', 'original_language',
        'budget_musd', 'revenue_musd',
        'production_companies', 'production_countries',
        'vote_count', 'vote_average', 'popularity', 'runtime',
        'overview', 'spoken_languages', 'poster_path',
        'cast', 'cast_size', 'director', 'crew_size'
    ]
    df = df[final_columns]

    # Step 8: Reset index
    df = df.reset_index(drop=True)

    if validate:
        logger.info(f"Final row count: {len(df)} | Final column count: {len(df.columns)}")
        logger.info("Sample of cast/director/crew_size columns:")
        logger.info(df[['cast', 'cast_size', 'director', 'crew_size']].head(3).to_dict())

    logger.info("TMDB data cleaning pipeline completed successfully")
    return df
