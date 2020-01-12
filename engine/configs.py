import pickle
from os import path

import xlrd

data_dir = path.join(path.dirname(path.dirname(path.realpath(__file__))), 'data')
# paths
stop_words_path = path.join(data_dir, 'sw.txt')
equivalents_path = path.join(data_dir, 'equivalents.txt')
compounds_path = path.join(data_dir, 'compounds.txt')
# dataset_path = path.join(data_dir, 'IR-F19-Project01-Input-2k.xlsx')
dataset_path = path.join(data_dir, '14k.xlsx')
index_file_path = path.join(data_dir, 'postings-14k.pickle')
doc_vectors_path = path.join(data_dir, 'doc-vectors-14k.pickle')
champions_list_path = path.join(data_dir, 'champions-list-14k.pickle')

# data corpus
sheet = xlrd.open_workbook(dataset_path).sheet_by_index(0)
doc_count = sheet.nrows

# champions list setting
champions_r_param = 20


def load_index_file():
    return pickle.load(open(index_file_path, 'rb'))


def load_vectors_file():
    return pickle.load(open(doc_vectors_path, 'rb'))


def load_champions_list():
    return pickle.load(open(champions_list_path, 'rb'))


def save_index_file(postings_list):
    with open(index_file_path, 'wb') as index_file:
        pickle.dump(postings_list, index_file)


def save_vectors_file(document_vectors):
    with open(doc_vectors_path, 'wb') as vectors_file:
        pickle.dump(document_vectors, vectors_file)


def save_champions_list(champions_list):
    with open(champions_list_path, 'wb') as champions_file:
        pickle.dump(champions_list, champions_file)
