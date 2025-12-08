import requests 
import os 
from dotenv import load_dotenv
import pandas as pd 
import logging

 
load_dotenv()

# configure logging to console
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

#access environment variables 
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")


#Movie IDs
movies_id=[0, 299534, 19995, 140607, 299536, 597, 135397, 420818, 24428, 168259, 99861, 284054, 12445, 181808, 330457, 351286, 109445, 321612, 260513]


# Function to get movies details by ID 
def fetch_movie(movie_id):
    url = f"{base_url}{movie_id}?api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        logging.error(
            "Unable to fetch data for movie ID %s. Status code: %s. Error message: %s",
            movie_id,
            response.status_code,
            response.text
        )
        return None
      
      
#fetch movies 
movies=[fetch_movie(movie_id) for movie_id in movies_id]

#convert to DataFrame 
df_raw= pd.DataFrame(movies)
df_raw.to_csv("../data/raw/movies_raw.csv", index=False)


