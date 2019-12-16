import numpy as np

from configs import doc_count, load_index_file, load_vectors_file

postings_list = load_index_file()
document_vectors = load_vectors_file()


def query_tf_idf(query_histogram):
    query_vector = {}
    query_vector_mag = 0
    for term in query_histogram:
        query_vector[term] = (np.log(query_histogram[term]) + 1) * np.log(doc_count / len(postings_list[term]))
        query_vector_mag += np.power(query_vector[term], 2)
    query_vector_mag = np.sqrt(query_vector_mag)
    return query_vector, query_vector_mag


def cos_similarity(query_vector, query_vector_mag, doc_vector_normalized):
    dot_product = 0
    for i in query_vector:
        if i in doc_vector_normalized:
            dot_product += query_vector[i] * doc_vector_normalized[i]
    return dot_product / query_vector_mag


def compute_score(query_histogram, doc_id):
    query_vector, query_vector_mag = query_tf_idf(query_histogram)
    return cos_similarity(query_vector, query_vector_mag, document_vectors[doc_id])
