import pickle
import shlex
import xlrd
from configs import dataset_path, index_file_path


postings_list = pickle.load(open(index_file_path, 'rb'))
sheet = xlrd.open_workbook(dataset_path).sheet_by_index(0)

data_keys = ['date', 'title', 'source', 'summary', 'tags', 'content', 'thumbnail']


def query_tokenize(q_str):
    phrase_tokens = []
    not_tokens = []
    regular_tokens = []
    for q in shlex.split(q_str):
        if ' ' in q:
            phrase_tokens.append(q)
        elif '!' in q:
            not_tokens.append(q[1:])
        else:
            regular_tokens.append(q)
    regular_tokens.sort(key=lambda x: len(postings_list[x]))
    return phrase_tokens, regular_tokens, not_tokens


def search(q_str):
    phrase_tokens, regular_tokens, not_tokens = query_tokenize(q_str)
    docs = set(postings_list[regular_tokens[0]].keys())
    for t in regular_tokens[1:]:
        if not docs:
            break
        docs.intersection_update(postings_list[t].keys())

    if docs:
        for nt in not_tokens:
            for d in postings_list[nt].keys():
                if d in docs:
                    docs.remove(d)

    results = []
    for d in docs:
        data_values = sheet.row_values(d)
        n = dict(zip(data_keys, data_values))
        n['relevance'] = 1
        results.append(n)
    return results
