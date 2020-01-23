import pickle
import sys
import numpy as np

from configs import doc_vectors_path
from core.corpus import doc_count
from core.dictionary import load_index_file

if sys.argv[1] != '-index':
    dictionary = load_index_file()
    document_vectors = pickle.load(open(doc_vectors_path, 'rb'))


def build_doc_vectors(dic):
    doc_vectors = [dict() for d in range(doc_count + 1)]
    # raw tf-idf (not normalized yet)
    for term_id in dic.postings_lists:
        idf = np.log2(doc_count / dic.doc_frequency(term_id))
        for doc_id in dic[term_id]:
            tf = np.log2(dic.term_frequency(term_id, doc_id)) + 1
            doc_vectors[doc_id][term_id] = tf * idf
    # normalization
    for vector in doc_vectors:
        vector_mag = 0
        for i in vector:
            vector_mag += np.power(vector[i], 2)
        vector_mag = np.sqrt(vector_mag)
        for i in vector:
            vector[i] /= vector_mag

    # saving the file
    with open(doc_vectors_path, 'wb') as vectors_file:
        pickle.dump(doc_vectors, vectors_file)


def query_tf_idf(query_histogram):
    query_vector = {}
    query_vector_mag = 0
    for term in query_histogram:
        query_vector[term] = (np.log2(query_histogram[term]) + 1) * np.log2(doc_count / dictionary.doc_frequency(term))
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
