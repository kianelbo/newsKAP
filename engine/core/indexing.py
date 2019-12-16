import numpy as np

from configs import doc_count, save_index_file, save_vectors_file, sheet
from core.processing import clean_token, remove_html, stop_words

if __name__ == "__main__":
    # building index file
    postings_list = {}
    for row in range(1, doc_count):
        token_pos = -1
        content = remove_html(sheet.cell_value(row, 5))
        for word in content.split():
            token_pos += 1
            cleaned_token = clean_token(word)
            if cleaned_token and cleaned_token not in stop_words:
                postings_list.setdefault(cleaned_token, {}).setdefault(row, []).append(token_pos)

    save_index_file(postings_list)
    print("successfully created the index file")

    # building document vectors file
    document_vectors = [dict() for d in range(doc_count + 1)]
    # raw tf idf
    for term in postings_list:
        idf = np.log(doc_count / len(postings_list[term]))
        for doc in postings_list[term]:
            tf = np.log(len(postings_list[term][doc])) + 1
            document_vectors[doc][term] = idf * tf
    # normalization
    for vector in document_vectors:
        vector_mag = 0
        for i in vector:
            vector_mag += np.power(vector[i], 2)
        vector_mag = np.sqrt(vector_mag)
        for i in vector:
            vector[i] /= vector_mag

    save_vectors_file(document_vectors)
    print("successfully created the vectors file")
