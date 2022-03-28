from tfid_vectorization import tfid_vectors
import sys
import pandas as pd

dataset = pd.read_csv(sys.argv[1])
dataset = dataset.dropna()

path_export = sys.argv[2]

#add index to dataset
index_list = [i for i in range(len(dataset))]
dataset['index'] = index_list

tfid_vectors_instance = tfid_vectors(dataset['word'], 'spanish', dataset['index'])
tfid_vectors_instance.apply_tfid_vectorization()

