import string
import pickle
import xlrd
from bs4 import BeautifulSoup

from configs import stop_words_path, dataset_path, index_file_path


def gather_stop_words():
    stop_words_set = set()
    with open(stop_words_path, encoding='utf-8') as f:
        for w in f.readlines():
            stop_words_set.add(w.strip())
    return stop_words_set


def clean_token(token):
    cleaned = ''.join([letter for letter in token if not letter.isdigit()])
    cleaned = cleaned.translate(str.maketrans('', '', string.punctuation))
    return cleaned


if __name__ == "__main__":
    stop_words = gather_stop_words()

    sheet = xlrd.open_workbook(dataset_path).sheet_by_index(0)

    vocab = {}
    for row in range(1, sheet.nrows):
        content = BeautifulSoup(sheet.row_values(row, 5)[0], features="html.parser").get_text()
        for word in content.split():
            cleaned_token = clean_token(word)
            if cleaned_token and cleaned_token not in stop_words:
                # print(cleaned_word)
                vocab.setdefault(cleaned_token, []).append(row)

    with open(index_file_path, 'wb') as index_file:
        pickle.dump(vocab, index_file)
