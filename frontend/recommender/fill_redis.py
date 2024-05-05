import os
import sys
import streamlit as st
import redis
import json
import pandas as pd

# Navigate to root directory
root_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(root_dir)
real_project_dir = os.path.dirname(project_dir)

# Add project directory to Python path
sys.path.insert(0, real_project_dir)

# Import necessary functions from codecompasslib
from codecompasslib.models.lightgbm_model import load_data


def fill_redis_with_data():
    try:
        # Load the data
        full_data_folder_id = '1Qiy9u03hUthqaoBDr4VQqhKwtLJ2O3Yd'
        full_data_embedded_folder_id = '139wi78iRzhwGZwxmI5WALoYocR-Rk9By'
        df_non_embedded, df_embedded = load_data(full_data_folder_id, full_data_embedded_folder_id)

        # Convert DataFrames to JSON format
        df_non_embedded_json = df_non_embedded.to_json(orient='records')
        df_embedded_json = df_embedded.to_json(orient='records')

        # Connect to Redis
        redis_client = redis.Redis(host='localhost', port=6379, db=0)

        # Store the JSON strings in Redis
        print("Storing data in Redis...")
        
        print("Not embedded df saving ...")
        redis_client.set('df_non_embedded', df_non_embedded_json)
        
        print("Embedded df saving ...")
        redis_client.set('df_embedded', df_embedded_json)

        print("Data stored in Redis successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    fill_redis_with_data()
