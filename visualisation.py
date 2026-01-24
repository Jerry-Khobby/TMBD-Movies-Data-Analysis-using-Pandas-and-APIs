import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

# Setup logger
logger = logging.getLogger("tmdb_visualization")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

def visualize_tmdb(df: pd.DataFrame, output_dir: str = "../data/visualizations") -> dict:
    """
    Generate visualizations for TMDB dataset and save plots to a directory.
    
    Visualizations:
    - Revenue vs Budget Trends
    - ROI Distribution by Genre
    - Popularity vs Rating
    - Yearly Trends in Box Office Performance
    - Franchise vs Standalone Success
    
    Returns a dictionary mapping plot names to saved file paths.
    """
    logger.info("Starting TMDB data visualization")
    os.makedirs(output_dir, exist_ok=True)
    plot_paths = {}
    
    # Ensure year column exists
    df = df.copy()
    df['year'] = pd.DatetimeIndex(df['release_date']).year

    sns.set_style("whitegrid")
    
    #  Revenue vs Budget Trends
    logger.info("Plotting Revenue vs Budget")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='budget_musd', y='revenue_musd', hue='vote_average', palette='viridis', alpha=0.7)
    plt.title("Revenue vs Budget (Million USD)")
    plt.xlabel("Budget (M USD)")
    plt.ylabel("Revenue (M USD)")
    plt.xscale("log")
    plt.yscale("log")
    path = os.path.join(output_dir, "revenue_vs_budget.png")
    plt.savefig(path)
    plt.close()
    plot_paths['revenue_vs_budget'] = path

    #  ROI Distribution by Genre
    logger.info("Plotting ROI Distribution by Genre")
    # Explode genres for one row per genre
    df_genres = df[['genres', 'roi']].dropna()
    df_genres = df_genres.assign(genres=df_genres['genres'].str.split('|')).explode('genres')
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df_genres, x='genres', y='roi')
    plt.xticks(rotation=45, ha='right')
    plt.title("ROI Distribution by Genre")
    plt.ylabel("ROI")
    plt.xlabel("Genre")
    path = os.path.join(output_dir, "roi_by_genre.png")
    plt.savefig(path)
    plt.close()
    plot_paths['roi_by_genre'] = path

    #  Popularity vs Rating
    logger.info("Plotting Popularity vs Rating")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='popularity', y='vote_average', hue='profit', palette='coolwarm', alpha=0.7)
    plt.title("Popularity vs Rating")
    plt.xlabel("Popularity")
    plt.ylabel("Average Rating")
    path = os.path.join(output_dir, "popularity_vs_rating.png")
    plt.savefig(path)
    plt.close()
    plot_paths['popularity_vs_rating'] = path

    # Yearly Trends in Box Office Performance
    logger.info("Plotting Yearly Trends in Box Office Performance")
    df_yearly = df.groupby('year').agg(
        total_revenue=('revenue_musd', 'sum'),
        total_budget=('budget_musd', 'sum'),
        avg_roi=('roi', 'mean')
    ).reset_index()
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=df_yearly, x='year', y='total_revenue', label='Total Revenue')
    sns.lineplot(data=df_yearly, x='year', y='total_budget', label='Total Budget')
    plt.title("Yearly Trends in Box Office Performance (Million USD)")
    plt.xlabel("Year")
    plt.ylabel("Million USD")
    plt.legend()
    path = os.path.join(output_dir, "yearly_box_office_trends.png")
    plt.savefig(path)
    plt.close()
    plot_paths['yearly_box_office_trends'] = path

    # Comparison of Franchise vs Standalone Success
    logger.info("Plotting Franchise vs Standalone Success")
    df['is_franchise'] = df['belongs_to_collection'].notna()
    df_group = df.groupby('is_franchise').agg(
        mean_revenue=('revenue_musd', 'mean'),
        mean_budget=('budget_musd', 'mean'),
        mean_roi=('roi', 'mean'),
        mean_rating=('vote_average', 'mean')
    ).reset_index()
    df_group['type'] = df_group['is_franchise'].map({True: 'Franchise', False: 'Standalone'})
    
    metrics = ['mean_revenue', 'mean_budget', 'mean_roi', 'mean_rating']
    for metric in metrics:
        plt.figure(figsize=(6, 4))
        sns.barplot(data=df_group, x='type', y=metric, palette='pastel')
        plt.title(f"{metric.replace('_',' ').title()} by Movie Type")
        plt.ylabel(metric.replace('_',' ').title())
        path = os.path.join(output_dir, f"{metric}_franchise_vs_standalone.png")
        plt.savefig(path)
        plt.close()
        plot_paths[metric+'_franchise_vs_standalone'] = path

    logger.info("TMDB data visualization completed successfully")
    return plot_paths
