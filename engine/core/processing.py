from datetime import datetime
import re

from configs import compounds_path, equivalents_path, stop_words_path

non_farsi_chars = '[^' + 'ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی ' + ']'
normalization_table = str.maketrans('\u0643\u064Aئآأۀ\u0623\u0624ة', 'کییااهاوه', '')  # substituting bad chars
endings = ['ات', 'ان', 'ترین', 'تر', 'م', 'ت', 'ش', 'یی', 'ی', 'ها', '‌ا']

stop_words = list()
with open(stop_words_path, encoding='utf-8') as f:
    for w in f.readlines():
        stop_words.append(w.strip())

equivalents = {}
with open(equivalents_path, encoding='utf-8') as f:
    for pair in f.readlines():
        pair_wrong, pair_correct = pair.split()
        equivalents[pair_wrong] = pair_correct

compounds_dict = {}
with open(compounds_path, encoding='utf-8') as f:
    for pair in f.readlines():
        pair_wrong, pair_correct = pair.split(',')
        compounds_dict[pair_wrong] = pair_correct
compounds_dict = dict((re.escape(k), v) for k, v in compounds_dict.items())
compounds_pattern = re.compile("|".join(compounds_dict.keys()))


def fix_compounds(text):
    return compounds_pattern.sub(lambda m: compounds_dict[re.escape(m.group(0))], text)


def standardize(token):
    if token in equivalents:
        token = equivalents[token]
    return stem(token)


def normalize_text(text):
    return re.sub(non_farsi_chars, '', text.translate(normalization_table))


def stem(token):
    if token in stop_words:
        return token
    original_token = token
    for end in endings:
        if token.endswith(end):
            token = token[:-len(end)]
    if not token or (original_token != token and token in stop_words):
        return original_token
    return token


def tokenize(text):
    tokens = [word for word in text.split()]
    stemmed_tokens = [stem(item) for item in tokens]
    return stemmed_tokens


def clean_text(text):
    # normalizing and removing invalid characters
    cleaned = normalize_text(text)
    # fixing compounds
    cleaned = fix_compounds(cleaned)
    return cleaned


def clean_token(token):
    # normalizing and removing invalid characters
    cleaned = normalize_text(token)
    # equivalent check
    cleaned = standardize(cleaned)
    # stemming
    cleaned = stem(cleaned)
    return cleaned


def str_to_date(d):
    d = d.split()
    d[1] = d[1][:-2]  # day
    return datetime.strptime(' '.join(d), '%B %d %Y, %H:%M')
