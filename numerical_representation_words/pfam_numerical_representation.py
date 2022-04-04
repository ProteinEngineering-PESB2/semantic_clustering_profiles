import pandas as pd
import sys
import random
from exploring_universal_encoder import make_embedding

dataset = pd.read_csv(sys.argv[1])
path_export = sys.argv[2]

description_values = dataset['description']
accession_values = dataset['accession']

embedding_dev = make_embedding(description_values)
embedding_dev.load_model()
embedding_dev.apply_encoding()

df_export = embedding_dev.export_embedding_to_df()
random_name = random.randint(1, 100)*1000
name_export = "{}{}_encoding_embedding.csv".format(path_export, random_name)
df_export['description'] = description_values
df_export['accession'] = accession_values
df_export.to_csv(name_export, index=False)
