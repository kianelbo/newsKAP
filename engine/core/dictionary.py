import pickle

from configs import index_file_path


def load_index_file():
    return pickle.load(open(index_file_path, 'rb'))


class Dictionary:
    def __init__(self):
        self.mapping = {}
        self.postings_lists = {}

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.postings_lists[item]
        return self.postings_lists[self.mapping[item]]

    def __contains__(self, item):
        return item in self.mapping

    def add(self, word, doc_id, positional):
        if word not in self.mapping:
            self.mapping[word] = len(self.mapping)
        self.postings_lists.setdefault(self.mapping[word], {}).setdefault(doc_id, []).append(positional)

    def term_id(self, term_string):
        return self.mapping[term_string]

    def get_docs(self, term):
        if isinstance(term, int):
            return set(self.postings_lists[term].keys())
        return set(self.postings_lists[self.mapping[term]].keys())

    def doc_frequency(self, term_id):
        return len(self.postings_lists[term_id])

    def term_frequency(self, term_id, doc_id):
        return len(self.postings_lists[term_id][doc_id])

    def save(self):
        with open(index_file_path, 'wb') as index_file:
            pickle.dump(self, index_file)
