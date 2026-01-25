import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import logging

logger = logging.getLogger(__name__)

def visualize_tmdb(df: pd.DataFrame, output_dir: str = "../data/visualizations") -> dict:
    """
    Generate only the visualizations required by the project for TMDB dataset.

    Visualizations:
    1. Revenue vs Budget Trends
    2. ROI Distribution by Genre
    3. Popularity vs Rating
    4. Yearly Trends in Box Office Performance
    5. Comparison of Franchise vs Standalone Success

    Returns a dictionary mapping plot names to saved file paths.
    """
    logger.info("Starting TMDB data visualization")
    os.makedirs(output_dir, exist_ok=True)
    plot_paths = {}

    df = df.copy()
    df['year'] = pd.DatetimeIndex(df['release_date']).year

    sns.set_style("whitegrid")

    # 1. Revenue vs Budget Trends
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

    # 2. ROI Distribution by Genre
    logger.info("Plotting ROI Distribution by Genre")
    df_genres = df[['genres', 'roi']].dropna()
    df_genres = df_genres.assign(genres=df_genres['genres'].str.split('|')).explode('genres')
    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df_genres, x='genres', y='roi')
    plt.xticks(rotation=45, ha='right')
    plt.title("ROI Distribution by Genre")
    plt.xlabel("Genre")
    plt.ylabel("ROI")
    path = os.path.join(output_dir, "roi_by_genre.png")
    plt.savefig(path)
    plt.close()
    plot_paths['roi_by_genre'] = path

    # 3. Popularity vs Rating
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

    # 4. Yearly Trends in Box Office Performance
    logger.info("Plotting Yearly Trends in Box Office Performance")
    df_yearly = df.groupby('year').agg(
        total_revenue=('revenue_musd', 'sum'),
        total_budget=('budget_musd', 'sum'),
        avg_roi=('roi', 'mean')
    ).reset_index()
    plt.figure(figsize=(12, 6))
    plt.plot(df_yearly['year'], df_yearly['total_revenue'], marker='o', label='Total Revenue')
    plt.plot(df_yearly['year'], df_yearly['total_budget'], marker='o', label='Total Budget')
    plt.title("Yearly Trends in Box Office Performance (Million USD)")
    plt.xlabel("Year")
    plt.ylabel("Million USD")
    plt.legend()
    path = os.path.join(output_dir, "yearly_box_office_trends.png")
    plt.savefig(path)
    plt.close()
    plot_paths['yearly_box_office_trends'] = path

    # 5. Comparison of Franchise vs Standalone Success (single plot)
    logger.info("Plotting Franchise vs Standalone Success")
    df['is_franchise'] = df['belongs_to_collection'].notna()
    df_group = df.groupby('is_franchise').agg(
        mean_revenue=('revenue_musd', 'mean'),
        mean_roi=('roi', 'mean')
    ).reset_index()
    df_group['type'] = df_group['is_franchise'].map({True: 'Franchise', False: 'Standalone'})

    # Melt to long format for grouped bar chart
    df_melt = df_group.melt(id_vars='type', value_vars=['mean_revenue', 'mean_roi'])
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df_melt, x='type', y='value', hue='variable')
    plt.title("Franchise vs Standalone Success")
    plt.xlabel("Movie Type")
    plt.ylabel("Value")
    path = os.path.join(output_dir, "franchise_vs_standalone.png")
    plt.savefig(path)
    plt.close()
    plot_paths['franchise_vs_standalone'] = path

    logger.info("TMDB data visualization completed successfully")
    return plot_paths
