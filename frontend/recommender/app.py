import os
import sys
import streamlit as st
import pandas as pd

# go up to root
# Construct the path to the root directory (one level up from embeddings)
root_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(root_dir)
real_project_dir = os.path.dirname(project_dir)

# Add the project directory to the Python path
sys.path.insert(0, real_project_dir)

from codecompasslib.models.lightgbm_model import generate_lightGBM_recommendations, load_data

def load_cached_data():
    # Check if data is already stored in session state
    if 'cached_data' not in st.session_state:
        with st.spinner('Fetching data from the server...'):
            # Load data
            full_data_folder_id: str = '1Qiy9u03hUthqaoBDr4VQqhKwtLJ2O3Yd'
            full_data_embedded_folder_id: str = '139wi78iRzhwGZwxmI5WALoYocR-Rk9By'
            st.session_state.cached_data = load_data(full_data_folder_id, full_data_embedded_folder_id)
    return st.session_state.cached_data

def main():
    # Load the data
    df_non_embedded, df_embedded = load_cached_data()

    st.title('GitHub Repo Recommendation System')

    # Input for target user
    target_user = st.text_input("Enter the target user's username:")

    if st.button('Get Recommendations'):
        # Check if user exists in the dataset
        if target_user not in df_embedded['owner_user'].values:
            st.error("User not found in the dataset. Please enter a valid username.")
        else:
            with st.spinner('Training model...'):
                # Generate recommendations
                recommendations = generate_lightGBM_recommendations(target_user, df_non_embedded, df_embedded, number_of_recommendations=10)
            st.subheader("Recommendations")
            for index, repo in enumerate(recommendations):
                name = df_non_embedded[df_non_embedded['id'] == repo[0]]['name'].values[0]
                description = df_non_embedded[df_non_embedded['id'] == repo[0]]['description'].values[0]
                link = f"https://github.com/{repo[1]}/{name}"
                st.write(f"{index+1} - Repo ID: {repo[0]}, Owner: {repo[1]}, [Link]({link})")
                st.write("Description:", description)

if __name__ == "__main__":
    main()
