import os
import sys
import streamlit as st
import redis
import json

# Navigate to root directory
root_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(root_dir)
real_project_dir = os.path.dirname(project_dir)

# Add project directory to Python path
sys.path.insert(0, real_project_dir)

# Import necessary functions from codecompasslib
from codecompasslib.models.lightgbm_model import load_data

# Function to load cached data
def load_cached_data():
    if 'cached_data' not in st.session_state:
        with st.spinner('Fetching data from the server...'):
            full_data_folder_id = '1Qiy9u03hUthqaoBDr4VQqhKwtLJ2O3Yd'
            full_data_embedded_folder_id = '139wi78iRzhwGZwxmI5WALoYocR-Rk9By'
            st.session_state.cached_data = load_data(full_data_folder_id, full_data_embedded_folder_id)
    return st.session_state.cached_data

# Connect to Redis
try:
    redis_client = redis.Redis(host='localhost', port=6379, db=0)
except Exception as e:
    st.error(f"Could not connect to Redis: {e}")
    sys.exit(1)

def main():
    # Load the data
    df_non_embedded, df_embedded = load_cached_data()

    st.title('GitHub Repo Recommendation System')
    target_user = st.text_input("Enter the target user's username:")

    if st.button('Get Recommendations'):
        try:
            recommendations = redis_client.get(target_user)
            if recommendations is None:
                st.error("User not found in the dataset. Please enter a valid username.")
            else:
                recommendations = json.loads(recommendations.decode("utf-8"))
                st.subheader("Recommendations")
                for index, repo in enumerate(recommendations):
                    repo_id, owner = repo
                    name = df_non_embedded[df_non_embedded['id'] == repo_id]['name'].values[0]
                    description = df_non_embedded[df_non_embedded['id'] == repo_id]['description'].values[0]
                    link = f"https://github.com/{owner}/{name}"
                    
                    st.markdown(f"""
                    <div style="background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px; color: #333; box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);">
                        <h3 style="margin-bottom: 5px; color: #000;">{name}</h3>
                        <p style="color: #000;">{description}</p>
                        <a href="{link}" target="_blank" style="color: #0366d6; text-decoration: none;">View on GitHub</a>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Could not retrieve recommendations: {e}")

if __name__ == "__main__":
    main()
