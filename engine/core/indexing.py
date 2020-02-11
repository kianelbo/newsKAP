import pickle

from configs import clustering_k, clusters_file_path, indices_file_path
from core.corpus import sheet
from core.inverted_index import InvertedIndex
from core.processing import stop_words, clean_text, standardize

if __name__ == "__main__":
    clusters = pickle.load(open(clusters_file_path, 'rb'))
    inverted_indices = [InvertedIndex() for _ in range(clustering_k)]
    # building indices file
    for c in range(clustering_k):
        for doc_id in clusters[c]:
            content = sheet['content'][doc_id]
            content = clean_text(content)
            token_pos = -1
            for word in content.split():
                token_pos += 1
                cleaned_token = standardize(word)
                if cleaned_token and cleaned_token not in stop_words:
                    inverted_indices[c].add(cleaned_token, doc_id, token_pos)

    with open(indices_file_path, 'wb') as indices_file:
        pickle.dump(inverted_indices, indices_file)
    print("successfully created the indices file")
