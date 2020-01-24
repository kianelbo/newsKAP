from os import path


data_dir = path.join(path.dirname(path.dirname(path.realpath(__file__))), 'data')
# paths
stop_words_path = path.join(data_dir, 'sw.txt')
equivalents_path = path.join(data_dir, 'equivalents.txt')
compounds_path = path.join(data_dir, 'compounds.txt')
# dataset_path = path.join(data_dir, 'IR-F19-Project02-14k.csv')
dataset_path = path.join(data_dir, '150k/')
# index_file_path = path.join(data_dir, 'dictionary-14k.pickle')
index_file_path = path.join(data_dir, 'dictionary-150k.pickle')
# doc_vectors_path = path.join(data_dir, 'doc-vectors-14k.pickle')
doc_vectors_path = path.join(data_dir, 'doc-vectors-150k.pickle')
