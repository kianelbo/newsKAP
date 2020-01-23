from os import path

import xlrd

data_dir = path.join(path.dirname(path.dirname(path.realpath(__file__))), 'data')
# paths
stop_words_path = path.join(data_dir, 'sw.txt')
equivalents_path = path.join(data_dir, 'equivalents.txt')
compounds_path = path.join(data_dir, 'compounds.txt')
dataset_path = path.join(data_dir, '14k.xlsx')
index_file_path = path.join(data_dir, 'postings-14k.pickle')
doc_vectors_path = path.join(data_dir, 'doc-vectors-14k.pickle')

# data corpus
sheet = xlrd.open_workbook(dataset_path).sheet_by_index(0)
doc_count = sheet.nrows
