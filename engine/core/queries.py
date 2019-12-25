import shlex
from configs import sheet, load_index_file, load_champions_list
from core.processing import clean_token, fix_compounds, remove_html, stop_words
from core.ranking import compute_score

postings_list = load_index_file()
vocabulary = postings_list.keys()
champions_list = load_champions_list()

data_keys = ['date', 'title', 'source', 'summary', 'tags', 'content', 'thumbnail']


def make_snippet(regular_tokens, phrase_tokens, doc_id):
    news_words = fix_compounds(remove_html(sheet.cell_value(doc_id, 5))).split()

    phrase_snippet_limit = 2
    regular_snippet_limit = 6

    phrase_snippet = []
    for phrase in phrase_tokens:
        if phrase_snippet_limit == 0:
            break
        for i in postings_list[phrase[0]][doc_id]:
            valid_i = True
            # check if this i represents a phrase
            for j, phrase_word in enumerate(phrase[1:]):
                if doc_id not in postings_list[phrase_word] or i + j + 1 not in postings_list[phrase_word][doc_id]:
                    valid_i = False
                    break
            if valid_i:
                phrase_snippet_limit -= 1
                phrase_snippet += news_words[i - 5:i - 1]
                # append phrase
                phrase_snippet.append('<span class="bold">')
                for h in range(len(phrase)):
                    phrase_snippet.append(news_words[i+h])
                phrase_snippet.append('</span>')
                phrase_snippet += news_words[i + len(phrase):i + len(phrase) + 5]
                phrase_snippet.append("... ")

    snippet_words = []
    for q in regular_tokens:
        if doc_id not in postings_list[q]:
            continue
        for i in postings_list[q][doc_id]:
            if regular_snippet_limit == 0:
                break
            regular_snippet_limit -= 1
            snippet_words += news_words[i-5:i-1]
            snippet_words.append('<span class="bold">' + news_words[i] + '</span>')
            snippet_words += news_words[i + 1:i + 5]
            snippet_words.append("... ")

    return ' '.join(phrase_snippet) + ' '.join(snippet_words)


def query_tokenize(q_str):
    query_histogram = {}
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
                if cleaned_word in postings_list:
                    query_histogram[cleaned_word] = query_histogram.setdefault(cleaned_word, 0) + 1
            phrase_tokens.append(this_phrase)
            continue

        cleaned_q = clean_token(q)
        if q[0] == '!':
            if cleaned_q in postings_list:
                not_tokens.append(cleaned_q)
        elif q.startswith('source:'):
            source_phrase = q[7:]
        elif q.startswith('cat:'):
            category_phrase = q[4:]
        elif cleaned_q in postings_list:
            regular_tokens.append(cleaned_q)
            query_histogram[cleaned_q] = query_histogram.setdefault(cleaned_q, 0) + 1
    return query_histogram, phrase_tokens, regular_tokens, not_tokens, source_phrase, category_phrase


def search_phrase(words):
    results = set()

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


def retrieve_docs(query_histogram, phrases, regular_tokens, not_tokens):
    docs = set()
    local_champions = set()

    for t in query_histogram:
        local_champions.update(champions_list[t])

    if not phrases:  # in case query does not have phrases
        for rt in regular_tokens:
            docs |= set(postings_list[rt].keys())
    else:  # in case query has phrases
        docs = search_phrase(phrases[0])
        for ph in phrases[1:]:
            docs &= search_phrase(ph)

    for nt in not_tokens:
        omitted_docs = set(postings_list[nt].keys())
        docs -= omitted_docs
        local_champions -= omitted_docs

    docs = sorted(docs, key=lambda k: k in local_champions)
    scores = [0] * len(docs)
    for i in range(len(docs)):
        scores[i] = compute_score(query_histogram, docs[i])

    return docs, scores


def search(q_str):
    query_histogram, phrase_tokens, regular_tokens, not_tokens, source, category = query_tokenize(q_str)

    if source or category:
        pass

    docs, score = retrieve_docs(query_histogram, phrase_tokens, regular_tokens, not_tokens)
    results = []
    for d, s in zip(docs, score):
        n = {'date': sheet.cell_value(d, 0)[:-7], 'title': sheet.cell_value(d, 1), 'source': sheet.cell_value(d, 2),
             'snippet': make_snippet(regular_tokens, phrase_tokens, d), 'thumbnail': sheet.cell_value(d, 6),
             'relevance': s, 'id': d}
        results.append(n)
    return results


def view_news(news_id):
    n = dict(zip(data_keys, sheet.row_values(int(news_id))))
    n['date'] = n['date'][:-7]
    n['content'] = remove_html(n['content'])
    n['tags'] = n['tags'][1:-1].replace('\"', '').split(',') if n['tags'] != '[]' else []
    return n
