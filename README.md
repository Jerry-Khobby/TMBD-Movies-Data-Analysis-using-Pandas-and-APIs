# 📽️ TMDB Movie Data Analysis

A comprehensive data analysis pipeline that fetches, cleans, analyzes, and visualizes movie data from The Movie Database (TMDB) API using Python, Pandas, and Matplotlib.

---

## 📋 Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Data Pipeline](#data-pipeline)
- [Key Findings](#key-findings)
- [Project Deliverables](#project-deliverables)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Project Overview

This project implements a complete movie data analysis pipeline that:
- Fetches movie data from TMDB API for 18 specific movies
- Cleans and preprocesses raw data according to data quality standards
- Implements Key Performance Indicators (KPIs) for movie performance analysis
- Generates visualizations to present insights on movie success factors
- Compares franchise vs standalone movie performance
- Identifies top-performing directors and franchises

**Assignment Type:** Individual Project  
**Data Source:** The Movie Database (TMDB) API  
**Analysis Focus:** Financial performance, audience reception, and franchise dynamics

---

## ✨ Features

- **API Data Extraction:** Automated fetching of movie details using TMDB API
- **Data Cleaning Pipeline:** Comprehensive preprocessing including:
  - JSON column extraction and normalization
  - Missing data handling
  - Datatype conversions
  - Unrealistic value replacement
- **KPI Analysis:** 10+ performance metrics including ROI, profit, ratings, and popularity
- **Advanced Filtering:** Custom search queries for specific movie combinations
- **Comparative Analysis:** Franchise vs standalone movie performance metrics
- **Data Visualization:** 5 key visualizations using Matplotlib
- **Modular Code Structure:** Reusable functions organized in separate modules

---

## 📁 Project Structure

```
tmdb-movie-analysis/
│
├── README.md                          # Project documentation (this file)
├── requirements.txt                   # Python dependencies
├── .gitignore                        # Git ignore rules
├── .env.example                      # API key template
│
├── data/
│   ├── raw/
│   │   └── movies_raw.csv            # Raw data from API (18 movies)
│   ├── cleaned/
│   │   └── tmdb_movies_clean.csv     # Cleaned and preprocessed data
│   └── final/
│       └── tmdb_after_kpi.csv        # Data with calculated KPIs
│
├── notebooks/
│   ├── tmdb-movies-data-cleaning.ipynb          # Data cleaning workflow
│   ├── kpi-implementation-analysis.ipynb        # KPI calculations
│   └── data-visualisation.ipynb                 # Visualization generation
│
├── src/
│   └── api_client.py                 # TMDB API data fetching script
│
└── reports/
    ├── figures/                      # Generated visualizations (PNG files)         
```

---

## 🛠️ Technologies Used

- **Python 3.x** - Core programming language
- **Pandas** - Data manipulation and analysis
- **Requests** - HTTP library for API calls
- **Matplotlib** - Data visualization
- **Python-dotenv** - Environment variable management
- **Jupyter Notebook** - Interactive analysis environment
- **TMDB API** - Movie data source

---

## 🚀 Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- TMDB API account and API key

### Installation Steps

1. **Clone the repository**
```bash
git clone https://github.com/Jerry-Khobby/TMBD-Movies-Data-Analysis-using-Pandas-and-APIs.git
cd tmdb-movie-data-analysis
```

2. **Create a virtual environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up TMDB API key**
   - Sign up for a free account at [The Movie Database](https://www.themoviedb.org/)
   - Navigate to Settings → API → Request an API Key
   - Copy your API key

5. **Configure environment variables**
```bash
# Create .env file from template
cp .env.example .env

# Edit .env and add your credentials:
API_KEY=your_tmdb_api_key_here
BASE_URL=https://api.themoviedb.org/3/movie/
```

---

## 💻 Usage

### Step 1: Fetch Movie Data

Run the API client script to fetch movie data:

```bash
python src/api_client.py
```

This will:
- Fetch data for 18 movies from TMDB API
- Save raw data to `data/raw/movies_raw.csv`
- Log the fetching process

**Movies Analyzed (IDs):**  
299534, 19995, 140607, 299536, 597, 135397, 420818, 24428, 168259, 99861, 284054, 12445, 181808, 330457, 351286, 109445, 321612, 260513

### Step 2: Data Cleaning

Open and run the cleaning notebook:
```bash
jupyter notebook notebooks/tmdb-movies-data-cleaning.ipynb
```

This notebook:
- Loads raw data from `data/raw/movies_raw.csv`
- Applies all cleaning transformations per project specifications
- Saves cleaned data to `data/cleaned/tmdb_movies_clean.csv`

### Step 3: KPI Analysis

Open and run the KPI notebook:
```bash
jupyter notebook notebooks/kpi-implementation-analysis.ipynb
```

This notebook:
- Loads cleaned data
- Calculates all KPI metrics (profit, ROI, rankings)
- Performs franchise vs standalone analysis
- Saves results to `data/final/tmdb_after_kpi.csv`

### Step 4: Visualization

Open and run the visualization notebook:
```bash
jupyter notebook notebooks/data-visualisation.ipynb
```

This notebook:
- Generates 5 required visualizations
- Saves figures to `reports/figures/`
- Presents key insights

---

## 🔄 Data Pipeline

```
┌─────────────────┐
│   TMDB API      │
│  (18 Movies)    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  src/           │
│  api_client.py  │ ──► Fetch movie details
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  data/raw/      │
│  movies_raw.csv │ ──► 18 movies × ~30 columns
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│  notebooks/             │
│  data_cleaning.ipynb    │ ──► Clean & preprocess
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────┐
│  data/cleaned/           │
│  tmdb_movies_clean.csv   │ ──► 18 movies × 22 columns
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────────┐
│  notebooks/             │
│  kpi_analysis.ipynb     │ ──► Calculate KPIs
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────┐
│  data/final/             │
│  tmdb_after_kpi.csv      │ ──► With profit, ROI columns
└────────┬─────────────────┘
         │
         ▼
┌─────────────────────────┐
│  notebooks/             │
│  visualisation.ipynb    │ ──► Generate charts
└────────┬────────────────┘
         │
         ▼
┌──────────────────────────┐
│  reports/figures/        │
│  *.png                   │ ──► 5 visualizations
└──────────────────────────┘
```

---

## 📊 Key Findings

### Data Overview
- **Total Movies Analyzed:** 18 movies
- **Date Range:** Various release years
- **Genres Covered:** Action, Adventure, Sci-Fi, Fantasy, Drama, and more

### Top Performers

**Highest Revenue Movies:**
1. [Top movie] - $2924 million
2. [Second movie] - $2799 million
3. [Third movie] - $2264 million

**Best ROI (Return on Investment):**
- Movies with budget ≥ $10M showed ROI ranging from 12.33 to 4.44
- Highest ROI achieved by: [Avatar]

**Highest Rated:**
- Best-rated movie (≥10 votes): [Avengers:Endgame] with rating 8.238/10

### Franchise vs Standalone Analysis

| Metric | Franchise | Standalone |
|--------|-----------|------------|
| Mean Revenue | $1691.8.X M | $0 M |
| Median ROI | 7.88M | 0 |
| Mean Budget | $213.78M | $0 M |
| Mean Popularity | 14.721 | 0 |
| Mean Rating | 7.3968 | 0|

**Key Insight:** [Franchises/Standalone movies] performed better overall in terms of [metric].


---

## 📦 Project Deliverables

### ✅ Completed Components

1. **API Data Extraction**
   - ✓ Functional `api_client.py` script
   - ✓ Raw data saved to CSV
   - ✓ Error handling and logging implemented

2. **Data Cleaning & Preprocessing**
   - ✓ All 11 cleaning steps from specification completed
   - ✓ JSON columns properly extracted
   - ✓ Datatypes converted correctly
   - ✓ Unrealistic values handled
   - ✓ Final column order matches requirements

3. **KPI Implementation**
   - ✓ 10 ranking metrics calculated
   - ✓ User-defined ranking function created
   - ✓ Advanced search queries implemented
   - ✓ Franchise vs standalone comparison
   - ✓ Top franchises and directors identified

4. **Data Visualization**
   - ✓ Revenue vs Budget scatter plot
   - ✓ ROI distribution by genre
   - ✓ Popularity vs Rating analysis
   - ✓ Yearly box office trends
   - ✓ Franchise vs standalone comparison chart

5. **Documentation**
   - ✓ Comprehensive README
   - ✓ Analysis summary report
   - ✓ Clean, modular code
   - ✓ Requirements.txt with dependencies

---

## 🔍 Data Cleaning Specifications Met

- [x] Dropped irrelevant columns: adult, imdb_id, original_title, video, homepage
- [x] Extracted collection name from belongs_to_collection
- [x] Extracted genre names separated by "|"
- [x] Extracted spoken languages separated by "|"
- [x] Extracted production countries separated by "|"
- [x] Extracted production companies separated by "|"
- [x] Converted budget, id, popularity to numeric
- [x] Converted release_date to datetime
- [x] Replaced budget/revenue/runtime = 0 with NaN
- [x] Converted budget and revenue to million USD
- [x] Handled vote_count = 0 cases
- [x] Cleaned overview and tagline placeholders
- [x] Removed duplicates
- [x] Dropped rows with unknown id or title
- [x] Kept only rows with ≥10 non-null columns
- [x] Filtered to Released movies only
- [x] Reordered columns per specification
- [x] Reset index

---

## 📈 Visualizations Generated

All visualizations are saved in `reports/figures/` directory:

1. **revenue_vs_budget.png** - Scatter plot showing relationship between budget and revenue
2. **roi_by_genre.png** - Box plot displaying ROI distribution across genres
3. **popularity_vs_rating.png** - Scatter plot of popularity versus audience rating
4. **yearly_trends.png** - Line plot showing box office performance over time
5. **franchise_comparison.png** - Bar chart comparing franchise vs standalone metrics

---

## 🤝 Contributing

This is an individual academic project. If you'd like to suggest improvements:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -m 'Add improvement'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## 📝 License

This project is created for educational purposes as part of a data engineering course assignment.

---

## 👤 Author

**Your Name**  
- GitHub: [@Jerry-Khobby](https://github.com/Jerry-Khobby)


## 🙏 Acknowledgments

- [The Movie Database (TMDB)](https://www.themoviedb.org/) for providing the API
- Course instructors for project guidelines and specifications
- Pandas, Matplotlib, and Python communities for excellent documentation

---

## 📞 Support

If you have questions about this project:
- Open an issue on GitHub
- Contact via email: [jeremiah.anku.coblah@gmail.com]

---

**Last Updated:** December 2024
