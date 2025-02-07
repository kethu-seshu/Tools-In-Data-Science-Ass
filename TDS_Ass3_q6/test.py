import numpy as np
from itertools import combinations

def cosine_similarity(v1, v2):
    dot_product = np.dot(v1, v2)
    norm1 = np.linalg.norm(v1)
    norm2 = np.linalg.norm(v2)
    return dot_product / (norm1 * norm2)

def most_similar(embeddings):
    phrases_and_vectors = list(embeddings.items())

    max_similarity = -1
    most_similar_pair = None
    
    for (phrase1, vec1), (phrase2, vec2) in combinations(phrases_and_vectors, 2):
        similarity = cosine_similarity(vec1, vec2)
        if similarity > max_similarity:
            max_similarity = similarity
            most_similar_pair = (phrase1, phrase2)
    
    return most_similar_pair