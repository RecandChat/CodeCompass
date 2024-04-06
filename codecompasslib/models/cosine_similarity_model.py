"""
Repository Recommendation System

This script analyzes GitHub repositories to recommend repositories based on cosine similarity scores
calculated from their textual descriptions, names, and primary programming languages. It utilizes
TF-IDF vectorization and cosine similarity to determine the relevance of each repository to a given user preference.
"""

# Standard library imports
import os
import sys

# Third-party imports
import pandas as pd
from pandas import DataFrame
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_DIR)

from codecompasslib.API.drive_operations import download_csv_as_pd_dataframe, get_creds_drive

def load_and_clean_data(full_data_folder_id):
    """
    Load and clean the dataset from a specified filepath.
    
    Args:
        full_data_folder_id (str): data folder id of the dataframe on drive.

    Returns:
        pandas.DataFrame: The cleaned DataFrame.
    """
    DRIVE_ID = "0AL1DtB4TdEWdUk9PVA"
    DATA_FOLDER = "13JitBJQLNgMvFwx4QJcvrmDwKOYAShVx"

    creds = get_creds_drive()
    df: DataFrame = download_csv_as_pd_dataframe(creds=creds, file_id=full_data_folder_id)

    # Delete missing values
    df.dropna(inplace=True)

    # Delete columns that are not needed
    columns_to_drop = [
        'is_archived', 'is_disabled', 'is_template', 'has_projects',  
        'owner_type', 'has_pages', 'has_wiki', 
        'has_issues', 'has_downloads', 'is_fork'
    ]
    df.drop(columns=columns_to_drop, inplace=True)

    # Handling missing values in text columns
    df['description'].fillna('', inplace=True)
    df['name'].fillna('', inplace=True)
    df['language'].fillna('', inplace=True)

    # Drop duplicates with name
    df.drop_duplicates(subset='name', keep='first', inplace=True)

    return df


def recommend_repos(user_preference, df, top_n=10):
    """
    Recommend repositories based on user preferences.

    Args:
        user_preference (str): The user's preferred keywords or phrases.
        df (pandas.DataFrame): The DataFrame containing repository data.
        top_n (int, optional): Number of top recommendations to return. Defaults to 10.

    Returns:
        pandas.DataFrame: DataFrame containing top_n recommended repositories.
    """
    
    tfidf_vectorizer = TfidfVectorizer()
    # Vectorize the user preference
    user_pref_vector = tfidf_vectorizer.transform([user_preference])

    # Calculate cosine similarity with all repositories
    cosine_scores = cosine_similarity(user_pref_vector, tfidf_vectorizer.transform(df['name'] + " " + df['description'] + " " + df['language'])).flatten()

    # Get the indices of the repositories with the highest similarity scores
    top_indices = np.argsort(cosine_scores)[-top_n:][::-1]

    # Select the top n recommended repositories
    recommended_repos = df.iloc[top_indices].reset_index(drop=True)

    return recommended_repos[['name', 'description', 'language', 'cosine_similarity_score']]

def main():
    """
    Main function to run the script.
    """
    df = load_and_clean_data('1Qiy9u03hUthqaoBDr4VQqhKwtLJ2O3Yd')
    user_preference = "python"
    recommended_repos = recommend_repos(user_preference, df, top_n=10)
    print(recommended_repos)

if __name__ == "__main__":
    main()