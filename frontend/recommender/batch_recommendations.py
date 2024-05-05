import redis
import pandas as pd
from codecompasslib.models.lightgbm_model import generate_lightGBM_recommendations, load_data

def fetch_and_store_recommendations():
    # Load data
    full_data_folder_id = '1Qiy9u03hUthqaoBDr4VQqhKwtLJ2O3Yd'
    full_data_embedded_folder_id = '139wi78iRzhwGZwxmI5WALoYocR-Rk9By'
    df_non_embedded, df_embedded = load_data(full_data_folder_id, full_data_embedded_folder_id)
    
    # Connect to Redis
    redis_client = redis.Redis(host='localhost', port=6379, db=0)

    # Get unique users
    unique_users = df_embedded['owner_user'].unique()

    # Compute recommendations for each user
    for user in unique_users:
        recommendations = generate_lightGBM_recommendations(user, df_non_embedded, df_embedded, number_of_recommendations=10)
        redis_client.set(user, str(recommendations))

if __name__ == "__main__":
    fetch_and_store_recommendations()
