from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from nltk.tokenize import word_tokenize
import pandas as pd

class training_autoencoders(object):

    def __init__(self, list_word, epoch, min_alpha, vector_size, alpha):

        self.list_word = list_word
        self.epoch = epoch
        self.min_alpha = min_alpha
        self.vector_size = vector_size
        self.alpha = alpha

    def dev_autoencoder(self):
        tagged_data = [TaggedDocument(words=word_tokenize(_d.lower()), tags=[str(i)]) for i, _d in
                       enumerate(self.list_word)]

        self.model = Doc2Vec(vector_size=self.vector_size, alpha=self.alpha, min_alpha=self.min_alpha, min_count=1, dm=1)
        self.model.build_vocab(tagged_data)
        self.model.train(tagged_data, total_examples=self.model.corpus_count, epochs=500)

    def get_embedding(self, data_to_evaluate):
        embedding_matrix = []

        for element in data_to_evaluate:
            embedding = self.model.infer_vector(element)
            row_data = [value for value in embedding]
            row_data.insert(0, element)
            embedding_matrix.append(row_data)

        header = ["p_{}".format(i) for i in range(self.vector_size)]
        header.insert(0, "word")

        df_export = pd.DataFrame(embedding_matrix, columns=header)
        return df_export



