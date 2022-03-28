import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords

class tfid_vectors(object):

    def __init__(self, elements_to_process, stop_words_language, index_label):
        self.elements_to_process = elements_to_process
        self.stop_words_language = stop_words_language
        self.index_label = index_label
        self.features = None

    def apply_tfid_vectorization(self):
        vec = TfidfVectorizer(stop_words=stopwords.words(self.stop_words_language))
        vec.fit(self.elements_to_process)
        self.features = vec.transform(self.elements_to_process)

