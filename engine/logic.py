import string
import xlrd
from bs4 import BeautifulSoup

data_keys = ['date', 'title', 'source', 'summary', 'tags', 'content', 'thumbnail']

stop_words = set()
with open('../data/sw.txt', encoding='utf-8') as f:
    for w in f.readlines():
        stop_words.add(w.strip())

sheet = xlrd.open_workbook('../data/IR-F19-Project01-Input.xlsx').sheet_by_index(0)

vocab = {}


def build_dict():
    for row in range(1, 2):
        content = BeautifulSoup(sheet.row_values(row, 5)[0], features="html.parser").get_text()
        for word in content.split():
            cleaned_word = ''.join([letter for letter in word if not letter.isdigit()])
            cleaned_word = cleaned_word.translate(str.maketrans('', '', string.punctuation))
            if cleaned_word and cleaned_word not in stop_words:  # if string is not empty and is not stop word
                # print(cleaned_word)
                vocab.setdefault(cleaned_word, []).append(row)


def dummy_test(count):
    results = []
    for i in range(1, int(count) + 1):
        data_values = sheet.row_values(i)
        n = dict(zip(data_keys, data_values))
        n['relevance'] = 1
        results.append(n)
    return results
