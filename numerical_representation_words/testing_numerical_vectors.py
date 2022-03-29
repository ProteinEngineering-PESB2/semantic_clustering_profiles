import pandas as pd
import sys
from exploring_universal_encoder import make_embedding

dataset = pd.read_csv(sys.argv[1])
data_encoding = dataset['word'][:10]
print(data_encoding)
embedding_dev = make_embedding(data_encoding)
embedding_dev.load_model()
embedding_dev.apply_encoding()

df_export = embedding_dev.export_embedding_to_df()
print(df_export)