from os import path

data_dir = path.join(path.dirname(path.dirname(path.realpath(__file__))), 'data')


stop_words_path = path.join(data_dir, 'sw.txt')
dataset_path = path.join(data_dir, 'IR-F19-Project01-Input.xlsx')
index_file_path = path.join(data_dir, 'postings.pickle')
