import pickle
import xlrd
from configs import dataset_path, index_file_path


postings_list = pickle.load(open(index_file_path, 'rb'))
sheet = xlrd.open_workbook(dataset_path).sheet_by_index(0)

data_keys = ['date', 'title', 'source', 'summary', 'tags', 'content', 'thumbnail']


def search(q_str):
    q_tokens = q_str.split()
    docs = set(postings_list[q_tokens[0]])
    for t in q_tokens[1:]:
        docs.intersection_update(postings_list[t])

    results = []
    for d in docs:
        data_values = sheet.row_values(d)
        n = dict(zip(data_keys, data_values))
        n['relevance'] = 1
        results.append(n)
    return results
