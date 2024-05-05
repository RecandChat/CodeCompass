import os
import sys

# Set path to the root directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
print("Path:", sys.path)

import redis
import pandas as pd
import json
from codecompasslib.models.lightgbm_model import generate_lightGBM_recommendations, load_data
import logging

logging.basicConfig(level=logging.INFO)

def fetch_and_store_recommendations():
    # Load data
    full_data_folder_id = '1Qiy9u03hUthqaoBDr4VQqhKwtLJ2O3Yd'
    full_data_embedded_folder_id = '139wi78iRzhwGZwxmI5WALoYocR-Rk9By'
    df_non_embedded, df_embedded = load_data(full_data_folder_id, full_data_embedded_folder_id)
    
    # Connect to Redis
    try:
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
    except Exception as e:
        logging.error(f"Could not connect to Redis: {e}")
        return

    # Get unique users
    unique_users = df_embedded['owner_user'].unique()

    # Compute recommendations for each user
    for user in unique_users:
        recommendations = generate_lightGBM_recommendations(user, df_non_embedded, df_embedded, number_of_recommendations=10)
        recommendations_json = json.dumps(recommendations)

        try:
            redis_client.set(user, recommendations_json)
            logging.info(f"Stored recommendations for user {user}")
        except Exception as e:
            logging.error(f"Could not store recommendations for user {user}: {e}")

if __name__ == "__main__":
    fetch_and_store_recommendations()
