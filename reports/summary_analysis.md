# TMDB Movie Data Analysis - Summary Report

**Project:** TMDB Movie Data Analysis using Pandas and APIs  
**Date:** December 2024  
**Analyst:** [Jeremiah Anku Coblah]  
**Movies Analyzed:** 18 films from TMDB database

---

## Executive Summary

This report presents a comprehensive analysis of  movies sourced from The Movie Database (TMDB) API. The analysis pipeline includes data extraction, cleaning, KPI calculation, and visualization to identify patterns in movie performance, franchise success, and directorial impact.

**Key Highlights:**
- Successfully extracted and cleaned data for movies
- Calculated 10+ performance metrics including ROI, profit, and ratings
- Compared franchise vs standalone movie performance
- Identified top-performing directors and franchises
- Generated 5 data visualizations for insights presentation

---

## 1. Methodology

### 1.1 Data Collection
- **Source:** TMDB API (The Movie Database)
- **Method:** REST API calls using Python requests library
- **Movie IDs:** 299534, 19995, 140607, 299536, 597, 135397, 420818, 24428, 168259, 99861, 284054, 12445, 181808, 330457, 351286, 109445, 321612, 260513
- **Data Points:** ~30 attributes per movie including budget, revenue, ratings, cast, crew, genres, etc.

### 1.2 Data Cleaning Process
1. Dropped 5 irrelevant columns (adult, imdb_id, original_title, video, homepage)
2. Extracted and normalized JSON-like columns (genres, production companies, countries, languages)
3. Converted datatypes (numeric conversions, datetime parsing)
4. Handled missing values and unrealistic entries (0 values replaced with NaN)
5. Converted budget and revenue to millions USD for readability
6. Filtered for released movies with sufficient data (≥10 non-null columns)
7. Final dataset: 18 movies × 22 columns

### 1.3 Analysis Approach
- **KPI Calculation:** Computed profit, ROI, and various ranking metrics
- **Comparative Analysis:** Grouped data by franchise status
- **Aggregation:** Analyzed performance by director and franchise
- **Visualization:** Created 5 matplotlib charts to present findings

---

## 2. Dataset Overview

### 2.1 Data Quality Metrics
- **Total Movies Fetched:** 18
- **Movies After Cleaning:** 18
- **Completeness Rate:** ~XX% (average non-null values per movie)
- **Date Range:** [Earliest year] - [Latest year]

### 2.2 Genre Distribution
Top genres in dataset:
1. [Genre 1] - X movies
2. [Genre 2] - X movies
3. [Genre 3] - X movies

### 2.3 Financial Overview
- **Total Combined Budget:** $X,XXX million USD
- **Total Combined Revenue:** $X,XXX million USD
- **Average Budget per Movie:** $XXX.X million
- **Average Revenue per Movie:** $XXX.X million
- **Overall Profit Margin:** XX%

---

## 3. Key Performance Indicators (KPIs)

### 3.1 Best Performing Movies

#### Highest Revenue
| Rank | Movie Title | Revenue (M USD) |
|------|-------------|-----------------|
| 1 | [Movie] | $X,XXX.X |
| 2 | [Movie] | $X,XXX.X |
| 3 | [Movie] | $X,XXX.X |

#### Highest Budget
| Rank | Movie Title | Budget (M USD) |
|------|-------------|----------------|
| 1 | [Movie] | $XXX.X |
| 2 | [Movie] | $XXX.X |
| 3 | [Movie] | $XXX.X |

#### Highest Profit (Revenue - Budget)
| Rank | Movie Title | Profit (M USD) |
|------|-------------|----------------|
| 1 | [Movie] | $X,XXX.X |
| 2 | [Movie] | $X,XXX.X |
| 3 | [Movie] | $X,XXX.X |

#### Highest ROI (Budget ≥ $10M)
| Rank | Movie Title | ROI | Budget (M USD) | Revenue (M USD) |
|------|-------------|-----|----------------|-----------------|
| 1 | [Movie] | XX.XX | $XXX.X | $X,XXX.X |
| 2 | [Movie] | XX.XX | $XXX.X | $X,XXX.X |
| 3 | [Movie] | XX.XX | $XXX.X | $X,XXX.X |

### 3.2 Worst Performing Movies

#### Lowest Profit
| Rank | Movie Title | Profit (M USD) |
|------|-------------|----------------|
| 1 | [Movie] | $-XXX.X |
| 2 | [Movie] | $-XXX.X |
| 3 | [Movie] | $-XXX.X |

#### Lowest ROI (Budget ≥ $10M)
| Rank | Movie Title | ROI |
|------|-------------|-----|
| 1 | [Movie] | X.XX |
| 2 | [Movie] | X.XX |
| 3 | [Movie] | X.XX |

### 3.3 Audience Reception

#### Most Voted Movies
| Rank | Movie Title | Vote Count |
|------|-------------|------------|
| 1 | [Movie] | XX,XXX |
| 2 | [Movie] | XX,XXX |
| 3 | [Movie] | XX,XXX |

#### Highest Rated (≥10 votes)
| Rank | Movie Title | Rating | Vote Count |
|------|-------------|--------|------------|
| 1 | [Movie] | X.X/10 | XX,XXX |
| 2 | [Movie] | X.X/10 | XX,XXX |
| 3 | [Movie] | X.X/10 | XX,XXX |

#### Lowest Rated (≥10 votes)
| Rank | Movie Title | Rating | Vote Count |
|------|-------------|--------|------------|
| 1 | [Movie] | X.X/10 | XX,XXX |
| 2 | [Movie] | X.X/10 | XX,XXX |
| 3 | [Movie] | X.X/10 | XX,XXX |

#### Most Popular
| Rank | Movie Title | Popularity Score |
|------|-------------|------------------|
| 1 | [Movie] | XXX.XX |
| 2 | [Movie] | XXX.XX |
| 3 | [Movie] | XXX.XX |

---

## 4. Advanced Search Queries

### 4.1 Search 1: Science Fiction Action Movies Starring Bruce Willis
**Criteria:** Genre contains "Science Fiction" AND "Action", Cast includes "Bruce Willis"

**Results:**
| Movie Title | Rating | Vote Count | Release Year |
|-------------|--------|------------|--------------|
| [If found] | X.X/10 | XX,XXX | XXXX |

*Note: If no results found, document that here*

### 4.2 Search 2: Uma Thurman & Quentin Tarantino Collaborations
**Criteria:** Cast includes "Uma Thurman", Director is "Quentin Tarantino"

**Results (sorted by runtime - shortest to longest):**
| Movie Title | Runtime (min) | Rating | Release Year |
|-------------|---------------|--------|--------------|
| [If found] | XXX | X.X/10 | XXXX |

*Note: If no results found, document that here*

---

## 5. Franchise vs Standalone Analysis

### 5.1 Performance Comparison

| Metric | Franchise Movies | Standalone Movies | Difference |
|--------|------------------|-------------------|------------|
| **Count** | X movies | X movies | - |
| **Mean Revenue** | $XXX.X M | $XXX.X M | +/- $XXX.X M |
| **Median ROI** | X.XX | X.XX | +/- X.XX |
| **Mean Budget** | $XXX.X M | $XXX.X M | +/- $XXX.X M |
| **Mean Popularity** | XX.X | XX.X | +/- XX.X |
| **Mean Rating** | X.X/10 | X.X/10 | +/- X.X |

### 5.2 Key Insights

**Franchise Movies:**
- Typically have [higher/lower] budgets
- Generate [more/less] revenue on average
- Show [better/worse] ROI compared to standalone films
- Have [higher/lower] popularity scores

**Standalone Movies:**
- Demonstrate [characteristics]
- Perform [better/worse] in terms of ratings
- [Other notable patterns]

**Statistical Significance:**
[Note any statistically significant differences observed]

---

## 6. Most Successful Franchises

### 6.1 Top Franchises by Total Revenue

| Rank | Franchise Name | # Movies | Total Budget (M USD) | Total Revenue (M USD) | Mean Revenue (M USD) | Mean Rating |
|------|----------------|----------|----------------------|----------------------|---------------------|-------------|
| 1 | [Franchise] | X | $XXX.X | $X,XXX.X | $XXX.X | X.X/10 |

### 6.2 Franchise Analysis Insights

**Most Profitable Franchise:**
- Name: [Franchise name]
- Total profit: $X,XXX.X million
- Number of movies in dataset: X
- Average profit per movie: $XXX.X million

**Best-Rated Franchise:**
- Name: [Franchise name]
- Average rating: X.X/10
- Consistency: [High/Medium/Low variation in ratings]

**Key Observations:**
- [Insight about franchise performance]
- [Patterns in successful franchises]
- [Comparison between franchises]

---

## 7. Most Successful Directors

### 7.1 Top Directors by Total Revenue

| Rank | Director Name | # Movies Directed | Total Revenue (M USD) | Mean Rating |
|------|---------------|-------------------|----------------------|-------------|
| 1 | [Director] | X | $X,XXX.X | X.X/10 |
| 2 | [Director] | X | $X,XXX.X | X.X/10 |
| 3 | [Director] | X | $X,XXX.X | X.X/10 |

### 7.2 Director Performance Analysis

**Highest Grossing Director:**
- Name: [Director name]
- Movies in dataset: X
- Total box office: $X,XXX.X million
- Average revenue per film: $XXX.X million

**Best-Rated Director:**
- Name: [Director name]
- Average rating: X.X/10
- Critical consistency: [Analysis]

**Key Insights:**
- [Observation about director success factors]
- [Correlation between director and genre]
- [Impact of director on franchise success]

---

## 8. Visualization Insights

### 8.1 Revenue vs Budget Trends
**Chart:** `reports/figures/revenue_vs_budget.png`

**Key Findings:**
- [Describe the correlation observed]
- [Note any outliers]
- [Trend line interpretation]
- Budget-revenue ratio: Approximately X:X

### 8.2 ROI Distribution by Genre
**Chart:** `reports/figures/roi_by_genre.png`

**Key Findings:**
- Highest ROI genre: [Genre] with median ROI of X.XX
- Lowest ROI genre: [Genre] with median ROI of X.XX
- Most consistent genre: [Genre] (low variance)
- Genre with highest variability: [Genre]

### 8.3 Popularity vs Rating
**Chart:** `reports/figures/popularity_vs_rating.png`

**Key Findings:**
- [Correlation between popularity and rating]
- [Identify quadrants: high-pop/high-rating, etc.]
- [Notable outliers and why]

### 8.4 Yearly Box Office Trends
**Chart:** `reports/figures/yearly_trends.png`

**Key Findings:**
- Peak revenue year: [Year] with $X,XXX.X million
- Trend direction: [Increasing/Decreasing/Stable]
- Notable patterns: [Any seasonal or cyclical trends]

### 8.5 Franchise vs Standalone Comparison
**Chart:** `reports/figures/franchise_comparison.png`

**Key Findings:**
- Visual comparison confirms [franchise/standalone] superiority in [metrics]
- Largest difference observed in: [Metric]
- Most similar performance in: [Metric]

---

## 9. Conclusions and Recommendations

### 9.1 What Makes a Successful Movie?

Based on the analysis of 18 movies, success factors include:

1. **Budget Investment:**
   - [Relationship between budget and success]
   - Optimal budget range: $XXX-XXX million

2. **Franchise Advantage:**
   - [Whether franchises outperform standalone films]
   - [Specific metrics where franchises excel]

3. **Genre Selection:**
   - Top-performing genres: [List]
   - Genres with best ROI: [List]

4. **Critical vs Commercial Success:**
   - [Relationship between ratings and revenue]
   - [Whether high ratings guarantee high revenue]

5. **Director Impact:**
   - [Evidence of director influence on success]
   - [Top directors' common characteristics]

### 9.2 Industry Insights

- **For Studios:** [Recommendations based on data]
- **For Investors:** [ROI and risk insights]
- **For Filmmakers:** [Success pattern observations]

### 9.3 Limitations

This analysis is subject to the following limitations:

1. **Sample Size:** Only 18 movies analyzed - may not represent broader industry
2. **Selection Bias:** Movies selected via specific IDs, not random sampling
3. **Temporal Coverage:** Dataset spans [X years], may not reflect current trends
4. **Missing Data:** Some movies had incomplete information (cast, crew, etc.)
5. **External Factors:** Does not account for marketing spend, release timing, competition
6. **Currency/Inflation:** Revenue not adjusted for inflation across different release years

### 9.4 Future Work

Recommendations for extending this analysis:

1. Expand dataset to 100+ movies for statistical significance
2. Include temporal analysis with inflation-adjusted figures
3. Incorporate marketing budget data if available
4. Analyze impact of streaming vs theatrical release
5. Include sentiment analysis of reviews
6. Examine seasonal release patterns and their impact
7. Correlate with award nominations/wins

---

## 10. Technical Specifications

### 10.1 Data Quality Report

**Completeness by Column:**
- Budget: XX% complete
- Revenue: XX% complete
- Ratings: XX% complete
- Cast/Crew: XX% complete

**Data Transformations Applied:**
- Budget/Revenue: Converted to million USD
- Zero values: Replaced with NaN
- JSON columns: Extracted and pipe-separated
- Dates: Converted to datetime format

### 10.2 Reproducibility

All analysis can be reproduced by:
1. Running `src/api_client.py` to fetch raw data
2. Executing `notebooks/tmdb-movies-data-cleaning.ipynb`
3. Running `notebooks/kpi-implementation-analysis.ipynb`
4. Generating visualizations with `notebooks/data-visualisation.ipynb`

---

## 11. References

- **Data Source:** The Movie Database (TMDB) API - https://www.themoviedb.org/
- **API Documentation:** https://developers.themoviedb.org/3
- **Python Pandas Documentation:** https://pandas.pydata.org/docs/
- **Matplotlib Documentation:** https://matplotlib.org/stable/contents.html

---

## Appendix A: Column Definitions

| Column Name | Data Type | Description |
|-------------|-----------|-------------|
| id | int | Unique TMDB movie ID |
| title | string | Movie title |
| tagline | string | Movie tagline/slogan |
| release_date | datetime | Release date |
| genres | string | Pipe-separated genre names |
| belongs_to_collection | string | Franchise/collection name |
| original_language | string | Original language code |
| budget_musd | float | Budget in million USD |
| revenue_musd | float | Revenue in million USD |
| production_companies | string | Pipe-separated company names |
| production_countries | string | Pipe-separated country names |
| vote_count | int | Number of votes |
| vote_average | float | Average rating (0-10) |
| popularity | float | TMDB popularity score |
| runtime | int | Runtime in minutes |
| overview | string | Movie description |
| spoken_languages | string | Pipe-separated language names |
| poster_path | string | URL path to poster image |
| cast | list | Cast members (if available) |
| cast_size | int | Number of cast members |
| director | list | Director name(s) |
| crew_size | int | Total crew size |

## Appendix B: Calculated Metrics

- **Profit:** `revenue_musd - budget_musd`
- **ROI (Return on Investment):** `revenue_musd / budget_musd`
- **Profit Margin:** `(profit / revenue_musd) × 100`
