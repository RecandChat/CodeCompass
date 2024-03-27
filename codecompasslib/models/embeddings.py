import numpy as np
from gensim.models.keyedvectors import KeyedVectors

def load_word2vec_model():
    # Load pre-trained Word2Vec model. Word Embeddings for the Software Engineering Domain, pre-trained on 15GB of Stack Overflow posts
    # Citation: Efstathiou Vasiliki, Chatzilenas Christos, & Spinellis Diomidis. (2018). Word Embeddings for the Software Engineering Domain [Data set]. Zenodo. https://doi.org/10.5281/zenodo.1199620
    word_vect = KeyedVectors.load_word2vec_format("./codecompasslib/PretrainedModels/SO_vectors_200.bin", binary=True)
    return word_vect

# Vectorizing text using domain specific word2vec model
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
    

