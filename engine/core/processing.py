from datetime import datetime
import string
from bs4 import BeautifulSoup
from hazm import *

from configs import stop_words_path

stemmer = Stemmer()

stop_words = set()
with open(stop_words_path, encoding='utf-8') as f:
    for w in f.readlines():
        stop_words.add(w.strip())


def normalize_text(text):
    text = text.replace('آ', 'ا')
    text = text.replace('\u0643', 'ک')
    text = text.replace('\u064A', 'ی')
    text = text.replace('\u200C', '')
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
    # stemming
    cleaned = stem(cleaned)
    return cleaned


def remove_html(text):
    return BeautifulSoup(text, features="html.parser").get_text()


def str_to_date(d):
    d = d.split()
    d[1] = d[1][:-2]  # day
    d[3] = d[3][:-7]  # time
    return datetime.strptime(' '.join(d), '%B %d %Y, %H:%M')
