import shlex
from core.corpus import sheet
from core.dictionary import load_index_file
from core.processing import clean_token, fix_compounds, remove_html, stop_words
from core.ranking import compute_score

dictionary = load_index_file()

data_keys = ['date', 'title', 'source', 'summary', 'tags', 'content', 'thumbnail']


def make_snippet(regular_tokens, phrase_tokens, doc_id):
    news_words = fix_compounds(remove_html(sheet['content'][doc_id])).split()

    phrase_snippet_limit = 2
    regular_snippet_limit = 6

    phrase_snippet = []
    for phrase in phrase_tokens:
        if phrase_snippet_limit == 0:
            break
        for i in dictionary[phrase[0]][doc_id]:
            valid_i = True
            # check if this i represents a phrase
            for j, phrase_word in enumerate(phrase[1:]):
                if phrase_word in dictionary:
                    if doc_id not in dictionary[phrase_word] or i + j + 1 not in dictionary[phrase_word][doc_id]:
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
        if doc_id not in dictionary[q]:
            continue
        for i in dictionary[q][doc_id]:
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
                if cleaned_word in dictionary:
                    term_id = dictionary.term_id(cleaned_word)
                    query_histogram[term_id] = query_histogram.setdefault(term_id, 0) + 1
            phrase_tokens.append(this_phrase)
            continue

        cleaned_q = clean_token(q)
        if q[0] == '!':
            if cleaned_q in dictionary:
                not_tokens.append(dictionary.term_id(cleaned_q))
        elif q.startswith('source:'):
            source_phrase = q[7:]
        elif q.startswith('cat:'):
            category_phrase = q[4:]
        elif cleaned_q in dictionary:
            term_id = dictionary.term_id(cleaned_q)
            regular_tokens.append(term_id)
            query_histogram[term_id] = query_histogram.setdefault(term_id, 0) + 1
    return query_histogram, phrase_tokens, regular_tokens, not_tokens, source_phrase, category_phrase


def search_phrase(words):
    results = set()

    s = 0
    while s < len(words) and words[s] in stop_words:
        s += 1
    if s == len(words):
        return results

    common_docs = dictionary.get_docs(words[s])
    for i in range(s + 1, len(words)):
        if words[i] not in stop_words:
            common_docs &= dictionary.get_docs(words[i])

    for cd in common_docs:
        for pos in dictionary[words[s]][cd]:
            flag = True
            for i in range(s + 1, len(words)):
                if words[i] in stop_words:
                    continue
                if pos + i - s not in dictionary[words[i]][cd]:
                    flag = False
                    break
            if flag:
                results.add(cd)
                break
    return results


def retrieve_docs(query_histogram, phrases, regular_tokens, not_tokens):
    docs = set()

    if not phrases:  # in case query does not have phrases
        for rt in regular_tokens:
            docs |= dictionary.get_docs(rt)
    else:  # in case query has phrases
        docs = search_phrase(phrases[0])
        for ph in phrases[1:]:
            docs &= search_phrase(ph)

    for nt in not_tokens:
        docs -= dictionary.get_docs(nt)

    docs = list(docs)
    scores = [0] * len(docs)
    for i in range(len(docs)):
        scores[i] = compute_score(query_histogram, docs[i])

    return docs, scores


def search(q_str):
    query_histogram, phrase_tokens, regular_tokens, not_tokens, source, category = query_tokenize(q_str)

    docs, scores = retrieve_docs(query_histogram, phrase_tokens, regular_tokens, not_tokens)
    docs_and_scores = []

    if source and not category:
        for d, s in zip(docs, scores):
            if sheet['url'][d] == source:
                docs_and_scores.append((d, s))
    elif category and not source:
        for d, s in zip(docs, scores):
            if sheet['category'][d] == category:
                docs_and_scores.append((d, s))
    elif source and category:
        for d, s in zip(docs, scores):
            if sheet['url'][d] == source and sheet['category'][d] == category:
                docs_and_scores.append((d, s))
    else:
        docs_and_scores = zip(docs, scores)

    results = []
    for d, s in docs_and_scores:
        n = {'date': sheet['publish_date'][d], 'title': sheet['title'][d], 'source': sheet['url'][d],
             'snippet': make_snippet(regular_tokens, phrase_tokens, d), 'thumbnail': sheet['thumbnail'][d],
             'relevance': s, 'id': d}
        results.append(n)
    return results


def view_news(news_id):
    n = dict(zip(data_keys, list(sheet.iloc[int(news_id)])))
    n['content'] = remove_html(n['content'])
    n['tags'] = n['tags'][1:-1].replace('\"', '').split(',') if n['tags'] != '[]' else []
    return n
