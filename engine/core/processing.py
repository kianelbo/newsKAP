from datetime import datetime
import string
from bs4 import BeautifulSoup
from hazm import *
# from finglish import f2p

from configs import equivalents_path, stop_words_path

stemmer = Stemmer()

stop_words = set()
with open(stop_words_path, encoding='utf-8') as f:
    for w in f.readlines():
        stop_words.add(w.strip())

equivalents = {}
with open(equivalents_path, encoding='utf-8') as f:
    for pair in f.readlines():
        pair_wrong, pair_correct = pair.split()
        equivalents[pair_wrong] = pair_correct


def standardize(token):
    # token = f2p(token)
    if token in equivalents:
        return equivalents[token]
    return token


def normalize_text(text):
    text = text.replace('\u0643', 'ک')
    text = text.replace('\u064A', 'ی')
    text = text.replace('ئ', 'ی')
    text = text.replace('آ', 'ا')
    text = text.replace('أ', 'ا')
    for bad_char in '\u200C\u0618\u0619\u061A\u0651':
        text = text.replace(bad_char, '')
    return text


def stem(token):
    return stemmer.stem(token)


def clean_token(token):
    # remove numbers
    cleaned = ''.join([letter for letter in token if not letter.isdigit()])
    # remove punctuations
    cleaned = cleaned.translate(str.maketrans('', '', string.punctuation))
    # normalizing
    cleaned = normalize_text(cleaned)
    # equivalent check
    cleaned = standardize(cleaned)
    # stemming
    cleaned = stem(cleaned)
    return cleaned


def remove_html(text):
    return BeautifulSoup(text, features="html.parser").get_text()


def str_to_date(d):
    d = d.split()
    d[1] = d[1][:-2]  # day
    return datetime.strptime(' '.join(d), '%B %d %Y, %H:%M')
