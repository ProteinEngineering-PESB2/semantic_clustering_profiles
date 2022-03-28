import tensorflow as tf
import sys
import pandas as pd
from keras.layers import TextVectorization

dataset = pd.read_csv(sys.argv[1])
dataset = dataset.dropna()

vectorizer = TextVectorization(max_tokens=20000, output_sequence_length=200)
text_ds = tf.data.Dataset.from_tensor_slices(dataset['word']).batch(128)
vectorizer.adapt(text_ds)

print(vectorizer.get_vocabulary()[:19])