import pickle
import xlrd

from configs import dataset_path, doc_vectors_path, index_file_path
from core.processing import clean_token, remove_html, stop_words
from core.ranking import calc_tf_idf_docs

if __name__ == "__main__":
    sheet = xlrd.open_workbook(dataset_path).sheet_by_index(0)

    # index file: dictionary - postings lists - positional indices
    postings_list = {}
    for row in range(1, sheet.nrows):
        token_pos = -1
        content = remove_html(sheet.cell_value(row, 5))
        for word in content.split():
            token_pos += 1
            cleaned_token = clean_token(word)
            if cleaned_token and cleaned_token not in stop_words:
                postings_list.setdefault(cleaned_token, {}).setdefault(row, []).append(token_pos)

    with open(index_file_path, 'wb') as index_file:
        pickle.dump(postings_list, index_file)

    # document vectors
    document_vectors = calc_tf_idf_docs(postings_list)

    with open(doc_vectors_path, 'wb') as vectors_file:
        pickle.dump(document_vectors, vectors_file)
