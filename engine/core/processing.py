import string
from bs4 import BeautifulSoup

from configs import stop_words_path

stop_words = set()
with open(stop_words_path, encoding='utf-8') as f:
    for w in f.readlines():
        stop_words.add(w.strip())


def clean_token(token):
    # remove numbers
    cleaned = ''.join([letter for letter in token if not letter.isdigit()])
    # remove punctuations
    cleaned = cleaned.translate(str.maketrans('', '', string.punctuation))
    return cleaned


def remove_html(text):
    return BeautifulSoup(text, features="html.parser").get_text()
