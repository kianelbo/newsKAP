from os import path


data_dir = path.join(path.dirname(path.dirname(path.realpath(__file__))), 'data')
# paths
stop_words_path = path.join(data_dir, 'sw.txt')
equivalents_path = path.join(data_dir, 'equivalents.txt')
compounds_path = path.join(data_dir, 'compounds.txt')

dataset_path = path.join(data_dir, 'refined_dataset.csv')

vectorizer_file_path = path.join(data_dir, 'vectorizer.pickle')
kmeans_file_path = path.join(data_dir, 'kmeans.pickle')
clusters_file_path = path.join(data_dir, 'clusters.pickle')
duplicates_path = path.join(data_dir, 'duplicates.pickle')
indices_file_path = path.join(data_dir, 'indices.pickle')
doc_vectors_path = path.join(data_dir, 'doc-vectors.pickle')


# number of clusters
clustering_k = 20
# dimension of doc vectors
max_features = 10000
