import pandas as pd
import sys
from exploring_gensim_word2vec import training_autoencoders
import os
import random

print("Start reading dataset")
dataset = pd.read_csv(sys.argv[1])
path_export = sys.argv[2]

dataset = dataset.dropna()

list_word = dataset['description']

print("Instance object")
for i in range(11, 513):
    print("Exploring training with vector size: ", i)
    training_embedding = training_autoencoders(list_word, 10, 0.005, i, 0.05)

    print("Training model")
    training_embedding.dev_autoencoder()

    print("Get embedding")
    dataset_embedding = training_embedding.get_embedding(list_word)

    print("Create directory")
    command = "mkdir {}{}_size".format(path_export, i)
    os.system(command)

    print("Export dataset")
    name_export = "{}{}_size\\{}_embedding_data.csv".format(path_export, i, random.randint(1, 1000)*100)
    dataset_embedding.to_csv(name_export, index=False)