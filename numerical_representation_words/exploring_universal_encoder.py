import pandas as pd
import tensorflow_hub as hub
import tensorflow_text
import random

class make_embedding(object):
    def __init__(self, data_to_process):
        self.data_to_process = data_to_process
        self.model = None
        self.encoding = []

    def load_model(self):
        print("Load module")
        module_url = 'https://tfhub.dev/google/universal-sentence-encoder-multilingual/3'
        self.model = hub.load(module_url)

    def __encoding_line(self, line):
        return self.model(line)

    def apply_encoding(self):
        for element in self.data_to_process:
            embedding = self.__encoding_line(element)[0].numpy()
            self.encoding.append(embedding)

    def export_embedding_to_df(self):

        header = ["p_{}".format(i) for i in range(len(self.encoding[0]))]
        df_data = pd.DataFrame(self.encoding, columns=header)
        return df_data

