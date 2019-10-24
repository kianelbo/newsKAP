import string

from configs import stop_words_path

stop_words = set()
with open(stop_words_path, encoding='utf-8') as f:
    for w in f.readlines():
        stop_words.add(w.strip())


def clean_token(token):
    cleaned = ''.join([letter for letter in token if not letter.isdigit()])
    cleaned = cleaned.translate(str.maketrans('', '', string.punctuation))
    return cleaned
