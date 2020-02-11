import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import configs
from core.corpus import sheet
from core.processing import tokenize, stop_words

k = configs.clustering_k
dimension = configs.max_features

if __name__ == "__main__":
    tf_idf_vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words=stop_words, max_features=dimension)
    doc_vectors = tf_idf_vectorizer.fit_transform(sheet['content'])
    print("successfully created doc vectors")

    with open(configs.vectorizer_file_path, 'wb') as vectorizer_file:
        pickle.dump(tf_idf_vectorizer, vectorizer_file)
    print("successfully saved vectorizer")
    with open(configs.doc_vectors_path, 'wb') as vectors_file:
        pickle.dump(doc_vectors, vectors_file)
    print("successfully saved doc vectors")

    k_means = KMeans(n_clusters=k, random_state=20).fit(doc_vectors)
    print("completed clustering")

    with open(configs.kmeans_file_path, 'wb') as kmeans_file:
        pickle.dump(k_means, kmeans_file)
    print("successfully saved kmeans file")

    results = k_means.predict(doc_vectors)
    print("completed labeling")

    clusters = [set() for _ in range(k)]
    for i, cluster in enumerate(results):
        clusters[cluster].add(i)
    with open(configs.clusters_file_path, 'wb') as clusters_file:
        pickle.dump(clusters, clusters_file)
    print("successfully saved clusters file")
