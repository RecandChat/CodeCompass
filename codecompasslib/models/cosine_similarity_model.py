import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# load the data
df = pd.read_csv('allReposCleaned.csv')

# delete missing values
df = df.dropna()

# delete columns that are not needed
df = df.drop(columns=[ 'is_archived', 'is_disabled', 'is_template', 'has_projects', 
        'has _discussions', 'owner_type', 'has_pages', 'has_wiki', 
        'has_issues', 'has_downloads', 'is_fork'])

# Handling missing values in text columns
df['description'].fillna('', inplace=True)
df['name'].fillna('', inplace=True)
df['language'].fillna('', inplace=True)

# Concatenating the text columns for vectorization
text_data = df['name'] + " " + df['description'] + " " + df['language']

# Vectorizing the text data
tfidf_vectorizer = TfidfVectorizer()
tfidf_matrix = tfidf_vectorizer.fit_transform(text_data)

# Calculating cosine similarity
cosine_sim = cosine_similarity(tfidf_matrix)

# Since the goal is to give a score to each repo, we can average the cosine similarities for each repo
# This gives a single score representing how similar each repo's text data is to all other repos
similarity_scores = np.mean(cosine_sim, axis=1)

# Adding the new column to the dataset
df['cosine_similarity_score'] = similarity_scores

# Displaying the updated dataset with the new column
# df[['name', 'description', 'language', 'cosine_similarity_score']].head(100)

def recommend_repos(user_preference, df, tfidf_vectorizer, top_n=10):
    """
    Recommend repositories based on user preferences.
    """
    # Vectorize the user preference
    user_pref_vector = tfidf_vectorizer.transform([user_preference])

    # Calculate cosine similarity with all repositories
    cosine_scores = cosine_similarity(user_pref_vector, tfidf_vectorizer.transform(df['name'] + " " + df['description'] + " " + df['language'])).flatten()

    # Get the indices of the repositories with the highest similarity scores
    top_indices = np.argsort(cosine_scores)[-top_n:][::-1]

    # Select the top n recommended repositories and reset the index
    recommended_repos = df.iloc[top_indices].reset_index(drop=True)

    # Optionally, format the output to make it more readable
    # For example, only displaying certain columns
    return recommended_repos[['name', 'description', 'language', 'cosine_similarity_score']]


# drop duplìcates with name
df = df.drop_duplicates(subset='name', keep='first')

# Example usage:
user_preference = "python"
recommended_repos = recommend_repos(user_preference, df, tfidf_vectorizer, top_n=10)
print(recommended_repos)



