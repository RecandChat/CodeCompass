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
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Path setup
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.insert(0, PROJECT_DIR)

# Constants
FILE_PATH = 'allReposCleaned.csv'

def load_and_clean_data(filepath):
    """
    Load and clean the dataset from a specified filepath.
    
    Args:
        filepath (str): The file path to the dataset.

    Returns:
        pandas.DataFrame: The cleaned DataFrame.
    """
    # Load the data
    df = pd.read_csv(filepath)

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

def calculate_cosine_similarity_scores(df):
    """
    Calculate cosine similarity scores for the dataset.

    Args:
        df (pandas.DataFrame): The DataFrame containing repository data.

    Returns:
        tuple: A tuple containing the DataFrame with added similarity scores and the TF-IDF vectorizer.
    """
    # Concatenating the text columns for vectorization
    text_data = df['name'] + " " + df['description'] + " " + df['language']

    # Vectorizing the text data using TF-IDF
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(text_data)

    # Calculating cosine similarity
    cosine_sim = cosine_similarity(tfidf_matrix)

    # Average the cosine similarities for each repo
    similarity_scores = np.mean(cosine_sim, axis=1)

    # Adding the new column to the dataset
    df['cosine_similarity_score'] = similarity_scores

    return df, tfidf_vectorizer

def recommend_repos(user_preference, df, tfidf_vectorizer, top_n=10):
    """
    Recommend repositories based on user preferences.

    Args:
        user_preference (str): The user's preferred keywords or phrases.
        df (pandas.DataFrame): The DataFrame containing repository data.
        tfidf_vectorizer (TfidfVectorizer): The TF-IDF vectorizer used for transforming text data.
        top_n (int, optional): Number of top recommendations to return. Defaults to 10.

    Returns:
        pandas.DataFrame: DataFrame containing top_n recommended repositories.
    """
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
    df = load_and_clean_data(FILE_PATH)
    df, tfidf_vectorizer = calculate_cosine_similarity_scores(df)
    user_preference = "python"
    recommended_repos = recommend_repos(user_preference, df, tfidf_vectorizer, top_n=10)
    print(recommended_repos)

if __name__ == "__main__":
    main()