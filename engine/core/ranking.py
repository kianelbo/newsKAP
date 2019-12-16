import numpy as np
import pickle

from configs import doc_vectors_path
from core.queries import sheet, postings_list

doc_count = sheet.nrows
document_vectors = pickle.load(open(doc_vectors_path, 'rb'))


def calc_tf_idf_docs(indices):
    doc_vectors = {}
    # raw tf idf
    for term in indices:
        idf = np.log(doc_count / len(term))
        for doc in term:
            tf = np.log(len(doc)) + 1
            doc_vectors[doc][term] = idf * tf
    # normalization
    for doc in doc_vectors:
        vector_mag = 0
        for e in doc_vectors[doc]:
            vector_mag += np.power(doc_vectors[doc][e], 2)
        vector_mag = np.sqrt(vector_mag)
        for e in doc_vectors[doc]:
            doc_vectors[doc][e] /= vector_mag
    return doc_vectors


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
    for e in query_vector:
        if e in doc_vector_normalized:
            dot_product += query_vector[e] * doc_vector_normalized[e]
    return dot_product / query_vector_mag


def compute_score(query_histogram, doc):
    query_vector, query_vector_mag = query_tf_idf(query_histogram)
    return cos_similarity(query_vector, query_vector_mag, document_vectors[doc])
