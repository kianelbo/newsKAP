import pickle
import shlex

from configs import kmeans_file_path, vectorizer_file_path, indices_file_path, duplicates_path, doc_vectors_path
from core.corpus import sheet
from core.processing import fix_compounds, stop_words, clean_token

data_keys = ['date', 'title', 'source', 'summary', 'tags', 'content', 'thumbnail']

category_mapping = ['science', 'culture', 'politics', 'economic', 'social', 'international', 'sport', 'multimedia', '']

kmeans = pickle.load(open(kmeans_file_path, 'rb'))
vectorizer = pickle.load(open(vectorizer_file_path, 'rb'))
inverted_indices = pickle.load(open(indices_file_path, 'rb'))
document_vectors = pickle.load(open(doc_vectors_path, 'rb'))
duplicates = pickle.load(open(duplicates_path, 'rb'))


def make_snippet(regular_tokens, phrase_tokens, doc_id, cluster):
    news_words = fix_compounds(sheet['content'][doc_id]).split()

    phrase_snippet_limit = 2
    regular_snippet_limit = 6

    phrase_snippet = []
    for phrase in phrase_tokens:
        if phrase_snippet_limit == 0:
            break
        for i in inverted_indices[cluster][phrase[0]][doc_id]:
            valid_i = True
            # check if this i represents a phrase
            for j, phrase_word in enumerate(phrase[1:]):
                if phrase_word in inverted_indices[cluster]:
                    if doc_id not in inverted_indices[cluster][phrase_word] or \
                            i + j + 1 not in inverted_indices[cluster][phrase_word][doc_id]:
                        valid_i = False
                        break
            if valid_i:
                phrase_snippet_limit -= 1
                phrase_snippet += news_words[i - 5:i - 1]
                # append phrase
                phrase_snippet.append('<span class="bold">')
                for h in range(len(phrase)):
                    phrase_snippet.append(news_words[i + h])
                phrase_snippet.append('</span>')
                phrase_snippet += news_words[i + len(phrase):i + len(phrase) + 5]
                phrase_snippet.append("... ")

    snippet_words = []
    for q in regular_tokens:
        if doc_id not in inverted_indices[cluster][q]:
            continue
        for i in inverted_indices[cluster][q][doc_id]:
            if regular_snippet_limit == 0:
                break
            regular_snippet_limit -= 1
            snippet_words += news_words[i - 5:i - 1]
            snippet_words.append('<span class="bold">' + news_words[i] + '</span>')
            snippet_words += news_words[i + 1:i + 5]
            snippet_words.append("... ")

    return ' '.join(phrase_snippet) + ' '.join(snippet_words)


def vectorize(raw_query):
    q_str = ''
    raw_query = fix_compounds(raw_query)
    words = raw_query.split()
    for word in words:
        if word[0] != '!':
            q_str += clean_token(word) + ' '

    query_vector = vectorizer.transform([q_str])
    cluster = int(kmeans.predict(query_vector)[0])
    return cluster, query_vector


def compute_score(query_vector, doc_id):
    return float(query_vector.dot(document_vectors[doc_id].transpose())[0])


def query_tokenize(q_str, cluster):
    phrase_tokens = []
    not_tokens = []
    regular_tokens = []
    source_phrase = ""
    category_phrase = ""

    q_str = fix_compounds(q_str)
    for q in shlex.split(q_str):
        if ' ' in q:
            this_phrase = []
            for phrase_word in q.split():
                cleaned_word = clean_token(phrase_word)
                this_phrase.append(cleaned_word)
            phrase_tokens.append(this_phrase)
            continue

        cleaned_q = clean_token(q)
        if q[0] == '!':
            if cleaned_q in inverted_indices[cluster]:
                not_tokens.append(inverted_indices[cluster].term_id(cleaned_q))
        elif q.startswith('source:'):
            source_phrase = q[7:]
        elif q.startswith('cat:'):
            category_phrase = q[4:]
        elif cleaned_q in inverted_indices[cluster]:
            term_id = inverted_indices[cluster].term_id(cleaned_q)
            regular_tokens.append(term_id)

    return phrase_tokens, regular_tokens, not_tokens, source_phrase, category_phrase


def search_phrase(words, cluster):
    results = set()

    s = 0
    while s < len(words) and words[s] in stop_words:
        s += 1
    if s == len(words):
        return results

    common_docs = inverted_indices[cluster].get_docs(words[s])
    for i in range(s + 1, len(words)):
        if words[i] not in stop_words:
            common_docs &= inverted_indices[cluster].get_docs(words[i])

    for cd in common_docs:
        for pos in inverted_indices[cluster][words[s]][cd]:
            flag = True
            for i in range(s + 1, len(words)):
                if words[i] in stop_words:
                    continue
                if pos + i - s not in inverted_indices[cluster][words[i]][cd]:
                    flag = False
                    break
            if flag:
                results.add(cd)
                break
    return results


def retrieve_docs(query_vector, phrases, regular_tokens, not_tokens, source, category, cluster):
    docs = set()
    if not phrases:  # in case query does not have phrases
        for rt in regular_tokens:
            docs |= inverted_indices[cluster].get_docs(rt)
    else:  # in case query has phrases
        docs = search_phrase(phrases[0], cluster)
        for ph in phrases[1:]:
            docs &= search_phrase(ph, cluster)

    for nt in not_tokens:
        docs -= inverted_indices[cluster].get_docs(nt)

    if source:
        docs &= set(sheet.index[sheet['url'] == source].tolist())
    if category:
        cat_number = category_mapping.index(category) + 1
        docs &= set(sheet.index[sheet['category'] == cat_number].tolist())

    docs_and_scores = {}
    for d in docs:
        docs_and_scores[d] = compute_score(query_vector, d)

    return docs_and_scores


def search(q_str):
    cluster, query_vector = vectorize(q_str)
    phrase_tokens, regular_tokens, not_tokens, source, category = query_tokenize(q_str, cluster)

    docs_and_scores = retrieve_docs(query_vector, phrase_tokens, regular_tokens, not_tokens, source, category, cluster)

    results = []
    for d in docs_and_scores:
        n = {'date': sheet['publish_date'][d], 'title': sheet['title'][d], 'source': sheet['url'][d],
             'snippet': make_snippet(regular_tokens, phrase_tokens, d, cluster), 'thumbnail': sheet['thumbnail'][d],
             'relevance': docs_and_scores[d], 'category': category_mapping[sheet['category'][d] - 1], 'id': d}
        results.append(n)

    return results


def view_news(news_id):
    news_id = int(news_id)
    n = dict(zip(data_keys, list(sheet.iloc[news_id])))
    n['tags'] = n['tags'].split(',') if n['tags'] else []
    n['duplicates'] = [
        {'id': dup, 'title': sheet['title'][dup], 'source': sheet['url'][dup]} for dup in duplicates[news_id]
    ]

    return n
