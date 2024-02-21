import pandas as pd
import numpy as np
from gensim.models.keyedvectors import KeyedVectors
from sklearn.neighbors import NearestNeighbors
from scipy.spatial.distance import cosine

def load_data():
    # Grab a dataframe from Data cleaner folder and only import columns necessary for analyzing a user's repositories
    df = pd.read_csv('/Users/mirandadrummond/VSCode/Github-Recommendation-System/monkelib/Data/clean/allReposCleaned.csv', usecols=['owner_user', 'name', 'description', 'language'])
    return df

def preprocess_data(df):
    # count unique languges
    num_languages = df['language'].nunique()

    # Create list of unique languages with _ prefix
    languages = ['_' + language for language in df['language'].unique()]

    # one hot encode the languages and don't include the language prefix
    df = pd.get_dummies(df, columns=['language'], prefix='')

    # Group by 'owner_user' and aggregate
    aggregation_dict = {
        'name': lambda x: list(x),
        'description': lambda x: list(x)
    }

    # Add columns for languages
    for lang in languages:
        aggregation_dict[lang] = 'max'

    user_df = df.groupby('owner_user').agg(aggregation_dict).reset_index()

    # first we turn list of names and descriptions into a single string
    user_df['name'] = user_df['name'].apply(lambda x: ' '.join(str(i) for i in x) if isinstance(x, list) else '')
    user_df['description'] = user_df['description'].apply(lambda x: ' '.join(str(i) for i in x) if isinstance(x, list) else '')

    return user_df

def load_word2vec_model():
    # Load pre-trained Word2Vec model. Word Embeddings for the Software Engineering Domain, pre-trained on 15GB of Stack Overflow posts
    # Citation: Efstathiou Vasiliki, Chatzilenas Christos, & Spinellis Diomidis. (2018). Word Embeddings for the Software Engineering Domain [Data set]. Zenodo. https://doi.org/10.5281/zenodo.1199620
    word_vect = KeyedVectors.load_word2vec_format("/Users/mirandadrummond/VSCode/Github-Recommendation-System/monkelib/PretrainedModels/SO_vectors_200.bin", binary=True)
    return word_vect

def vectorize_text(text, word_vect):
    vector_sum = np.zeros(word_vect.vector_size)  # Initialize an array to store the sum of word vectors
    count = 0  # Initialize a count to keep track of the number of words found in the vocabulary
    for word in text.split():
        if word in word_vect.key_to_index:  # Check if the word is in the vocabulary
            vector_sum += word_vect[word]  # Add the word vector to the sum
            count += 1  # Increment the count
    if count > 0:
        return vector_sum / count  # Return the average of word vectors
    else:
        return vector_sum  # Return the zero vector if no words are found in the vocabulary

def preprocess_user_df(user_df, word_vect):
    embedded_user_df = user_df.copy()
    embedded_user_df['name'] = user_df['name'].fillna('')  
    embedded_user_df['description'] = user_df['description'].fillna('')
    embedded_user_df['name_vector'] = embedded_user_df['name'].apply(lambda x: vectorize_text(x, word_vect))
    embedded_user_df['description_vector'] = embedded_user_df['description'].apply(lambda x: vectorize_text(x, word_vect))
    return embedded_user_df

def preprocess_neighbors_repos(neighborsRepos, word_vect):
    neighborsRepos['name_vector'] = neighborsRepos['name'].apply(lambda x: vectorize_text(x, word_vect))
    neighborsRepos['description_vector'] = neighborsRepos['description'].apply(lambda x: vectorize_text(x, word_vect))
    neighborsRepos.drop(['name','description'], axis=1, inplace=True)
    return neighborsRepos

def calculate_cosine_dissimilarity(vec1, vec2):
    if np.all(vec1 == 0) or np.all(vec2 == 0):
        return 1.0  # Assuming maximum dissimilarity when one vector is all zeros
    return cosine(vec1, vec2)

def find_most_dissimilar_repo(target_user, target_repos, other_repos):
    max_dissimilarity_score = 0
    most_dissimilar_repo_info = None

    for index, other_repo in other_repos.iterrows():
        other_name_vec = np.array(other_repo['name_vector'])
        other_desc_vec = np.array(other_repo['description_vector'])

        for _, target_repo in target_repos.iterrows():
            target_name_vec = np.array(target_repo['name_vector'])
            target_desc_vec = np.array(target_repo['description_vector'])

            name_dissimilarity = calculate_cosine_dissimilarity(other_name_vec, target_name_vec)
            desc_dissimilarity = calculate_cosine_dissimilarity(other_desc_vec, target_desc_vec)

            average_dissimilarity = (name_dissimilarity + desc_dissimilarity) / 2

            if average_dissimilarity > max_dissimilarity_score:
                max_dissimilarity_score = average_dissimilarity
                most_dissimilar_repo_info = (index, other_repo['owner_user'], max_dissimilarity_score)

    return most_dissimilar_repo_info 

def clean_code(user_input='21,AntiTyping'):
    target_user_index, target_user = user_input.split(',')
    target_user_index = int(target_user_index)
    # Load data, preprocess it, and load the word2vec model, then preprocess the user dataframe and the neighbors dataframe.
    df = load_data()
    user_df = preprocess_data(df)
    word_vect = load_word2vec_model()
    embedded_user_df = preprocess_user_df(user_df, word_vect)
    vectors = []
    repo_df = embedded_user_df * 1

    # Embed and vectorize the user dataframe
    for row in repo_df.index: 
        vector = []
        for columns in ['name_vector', 'description_vector']:
            if type(repo_df.at[row, columns]) == np.ndarray:
                for element in repo_df.at[row, columns]:
                    vector.append(element)
            else: vector.append(repo_df.at[row, columns])
        vectors.append(vector)

    # Fit the nearest neighbors model to find the most similar users to the target user
    k = 5
    nn_model = NearestNeighbors(n_neighbors=k, metric='euclidean')
    nn_model.fit(vectors)

    # print the target user and the most similar users
    neighbors = nn_model.kneighbors([vectors[target_user_index]], return_distance=False)[0][1:]
    neighborsAndTarget = [target_user_index] + list(neighbors)
    neighborsAndTargetRepos = user_df.iloc[neighborsAndTarget]

    ###   
    dfs = []
    for index in neighborsAndTargetRepos.index:
        dfs.append(df[df['owner_user'] == user_df.at[index, 'owner_user']])

    neighborsRepos = pd.concat(dfs, ignore_index=False)
    neighborsRepos = preprocess_neighbors_repos(neighborsRepos, word_vect)

    target_repos = neighborsRepos[neighborsRepos['owner_user'] == target_user]
    other_repos = neighborsRepos[neighborsRepos['owner_user'] != target_user]

    most_dissimilar_repo_info = find_most_dissimilar_repo(target_user, target_repos, other_repos)

    if most_dissimilar_repo_info:
        most_dissimilar_repo = df.iloc[most_dissimilar_repo_info[0]]
        
    owner_user, description, language = most_dissimilar_repo['owner_user'], most_dissimilar_repo['description'], most_dissimilar_repo['language']
    recommendations = []  # Placeholder for recommendations
    
    # Example: Generate a list of recommendation dictionaries
    for i in range(1):  # Assuming you want to return 3 recommendations
        recommendations.append({
            'owner_user': owner_user,
            'description': description,
            'language': language
        })
    
    print(recommendations)
    return recommendations
