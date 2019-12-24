from itertools import groupby
from operator import itemgetter
import shlex
from configs import load_index_file, sheet
from core.processing import clean_token, remove_html, stop_words
from core.ranking import compute_score

postings_list = load_index_file()
vocabulary = postings_list.keys()

data_keys = ['date', 'title', 'source', 'summary', 'tags', 'content', 'thumbnail']


def make_snippet2(regular_tokens ,phrase_tokens ,doc_id):
    news_words = remove_html(sheet.cell_value(doc_id, 5)).split()
    print("regular tokens:",regular_tokens)
    print("phrase tokens:", phrase_tokens)

    phrase_snippet_limit = 2
    regular_snippet_limit = 6

    snippet = ""

    phrase_snippet = []
    for phrase in phrase_tokens:
        if phrase_snippet_limit == 0:
            break
        for i in postings_list[phrase[0]][doc_id]:
            print(f"checking if position {i} makes a phrase ...")
            valid_i = True
            # check if this i represents a phrase
            for j, phrase_word in enumerate(phrase[1:]):
                print(f"checking position {i+j+1}")
                if doc_id not in postings_list[phrase_word] or i + j + 1 not in postings_list[phrase_word][doc_id]:
                    valid_i = False
                    print("i invalid")
                    break
            if valid_i:
                phrase_snippet_limit -= 1;
                phrase_snippet += news_words[i - 5:i - 1]
                # append phrase
                phrase_snippet.append('<span class="bold">')
                for h in range(0,len(phrase)):
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

    snippet = ' '.join(phrase_snippet) + ' '.join(snippet_words)

    return snippet


def make_snippet(parts, doc_id):
    news_words = remove_html(sheet.cell_value(doc_id, 5)).split()

    q_tokens = []
    for p in parts:
        if p[1] == 1:
            q_tokens.append(p[0])
        elif p[1] == 2:
            for pw in p[0].split():
                if pw not in stop_words:
                    q_tokens.append(pw)

    snippet_words = set()
    bolds = set()
    for q in q_tokens:
        for i in postings_list[q][doc_id]:
            bolds.add(i)
            snippet_words.add(i)

            j = i
            while True:
                j -= 1
                if j >= 0:
                    snippet_words.add(j)
                else:
                    break
                if news_words[j].endswith('.') or i - j > 5:
                    break
            j = i
            while True:
                j += 1
                if j < len(news_words):
                    snippet_words.add(j)
                else:
                    break
                if news_words[j].endswith('.') or j - i > 5:
                    break

    sentence_ranges = []
    for k, g in groupby(enumerate(snippet_words), lambda x: x[0] - x[1]):
        group = (map(itemgetter(1), g))
        group = list(map(int, group))
        r = range(group[0], group[-1])
        if len(r) > 4:
            sentence_ranges.append(r)
        if len(sentence_ranges) > 2:
            break

    snippet = []
    for rng in sentence_ranges:
        for i in rng:
            snippet.append(news_words[i] if i not in bolds else '<span class="bold">' + news_words[i] + '</span>')
        snippet.append('...')
    if snippet[-2].endswith('.'):
        snippet.pop()

    return ' '.join(snippet)


def query_tokenize(q_str):
    query_histogram = {}
    phrase_tokens = []
    not_tokens = []
    regular_tokens = []
    source_phrase = ""
    category_phrase = ""

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


def retrieve_docs(phrases, regular_tokens, not_tokens):
    docs = set()
    if not regular_tokens:
        if not phrases:
            return docs
        docs = search_phrase(phrases[0])
        for ph in phrases[1:]:
            docs &= search_phrase(ph)
            return docs

    for rt in regular_tokens:
        docs |= set(postings_list[rt].keys())
    for ph in phrases:
        docs &= search_phrase(ph)
    for nt in not_tokens:
        docs -= set(postings_list[nt].keys())

    return docs


def search(q_str):
    query_histogram, phrase_tokens, regular_tokens, not_tokens, source, category = query_tokenize(q_str)

    if source or category:
        pass

    docs = retrieve_docs(phrase_tokens, regular_tokens, not_tokens)
    results = []
    for d in docs:
        n = {'date': sheet.cell_value(d, 0)[:-7], 'title': sheet.cell_value(d, 1), 'source': sheet.cell_value(d, 2),
             'snippet': make_snippet2(regular_tokens,phrase_tokens,d), 'thumbnail': sheet.cell_value(d, 6),
             'relevance': compute_score(query_histogram, d), 'id': d}
        results.append(n)
    return results


def view_news(news_id):
    n = dict(zip(data_keys, sheet.row_values(int(news_id))))
    n['date'] = n['date'][:-7]
    n['content'] = remove_html(n['content'])
    n['tags'] = n['tags'][1:-1].replace('\"', '').split(',') if n['tags'] != '[]' else []
    return n
