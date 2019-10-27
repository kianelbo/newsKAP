import pickle
import random
import shlex
import xlrd
from configs import dataset_path, index_file_path
from core.preprocessing import clean_token, stop_words

postings_list = pickle.load(open(index_file_path, 'rb'))
vocabulary = postings_list.keys()
sheet = xlrd.open_workbook(dataset_path).sheet_by_index(0)

data_keys = ['date', 'title', 'source', 'summary', 'tags', 'content', 'thumbnail']


def query_tokenize(q_str):
    phrase_tokens = []
    not_tokens = []
    regular_tokens = []
    source_phrase = ""
    category_phrase = ""
    for q in shlex.split(q_str):
        cleaned_q = clean_token(q)
        if cleaned_q in stop_words:
            continue
        if ' ' in q:
            phrase_tokens.append((cleaned_q, 2))
        elif q[0] == '!':
            not_tokens.append((cleaned_q, 3))
        elif q.startswith('source:'):
            source_phrase = q[7:]
        elif q.startswith('cat:'):
            category_phrase = q[4:]
        else:
            regular_tokens.append((cleaned_q, 1))
    regular_tokens.sort(key=lambda x: len(postings_list[x[0]]))
    return phrase_tokens + regular_tokens + not_tokens, source_phrase, category_phrase


def search_phrase(phrase):
    results = set()

    words = phrase.split()
    s = 0
    while s < len(words) and words[s] in stop_words:
        s += 1
    if s == len(words):
        return results

    common_docs = set(postings_list[words[s]].keys())
    for i in range(s + 1, len(words)):
        if words[i] not in stop_words:
            common_docs &= set(postings_list[words[i]].keys())

    for cd in common_docs:
        for pos in postings_list[words[s]][cd]:
            flag = True
            for i in range(s + 1, len(words)):
                if words[i] in stop_words:
                    continue
                if pos + i - s not in postings_list[words[i]][cd]:
                    flag = False
                    break
            if flag:
                results.add(cd)
                break
    return results


def retrieve_docs(q_str):
    parts, source, category = query_tokenize(q_str)
    docs = set()

    if source or category:
        pass

    if not parts or parts[0][1] == 3:                   # empty query or without regular tokens or phrases
        return docs

    if parts[0][1] == 2:                                # first searching the phrase if exists
        docs = search_phrase(parts[0][0])
    else:                                               # regular word
        docs.update(postings_list[parts[0][0]].keys())

    for t in parts[1:]:
        if not docs:
            break
        if t[1] == 2:
            docs &= search_phrase(t[0])
        elif t[1] == 3:
            docs -= set(postings_list[t[0]].keys())
        else:
            docs &= set(postings_list[t[0]].keys())

    return docs


def search(q_str):
    docs = retrieve_docs(q_str)
    results = []
    for d in docs:
        n = {'date': sheet.cell_value(d, 0), 'title': sheet.cell_value(d, 1), 'source': sheet.cell_value(d, 2),
             'preview': sheet.cell_value(d, 3), 'thumbnail': sheet.cell_value(d, 6), 'relevance': random.random(),
             'id': d}
        results.append(n)
    return results


def view_news(news_id):
    return dict(zip(data_keys, sheet.row_values(int(news_id))))
