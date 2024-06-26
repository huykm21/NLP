# -*- coding: utf-8 -*-
"""Dấu câu kết nối GG Drive

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UyZQt460F7XhS-BOj0NJDeah_FW_bS0K
"""

# kết nối với gg drive
from google.colab import drive
drive.mount('/content/drive')

import sys
sys.path.append('/content/drive/MyDrive/Project NLP dấu câu ')


from data_loader import load_data, load_data, save_vectorization, make_dataset
from trainer import create_vectorizations

file_path = '/content/drive/MyDrive/Project NLP dấu câu /data10000.csv'
train_pairs, val_pairs, test_pairs = load_data(file_path, limit=10000)

source_vectorization, target_vectorization = create_vectorizations(train_pairs)
save_vectorization(source_vectorization, '/content/drive/MyDrive/Project NLP dấu câu /source_vectorization_layer.pkl')
save_vectorization(target_vectorization, '/content/drive/MyDrive/Project NLP dấu câu /target_vectorization_layer.pkl')

batch_size = 64
train_ds = make_dataset(train_pairs, source_vectorization, target_vectorization, batch_size)
val_ds = make_dataset(val_pairs, source_vectorization, target_vectorization, batch_size)
test_ds = make_dataset(test_pairs, source_vectorization, target_vectorization, batch_size)

from transformer_model import TransformerModel
import tensorflow as tf
transformer = TransformerModel(source_vectorization=source_vectorization,
    target_vectorization=target_vectorization,
    dense_dim=8192, num_heads=8, drop_out=0)

transformer.build_model(optimizer="rmsprop",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"])
transformer.fit(train_ds, epochs=50, validation_data=val_ds,
    callbacks=[
        tf.keras.callbacks.ModelCheckpoint(
            filepath='/content/drive/MyDrive/Project NLP dấu câu /restore_diacritic.keras',
            save_best_only='True',
            monitor='val_accuracy'
        )
    ])

transformer.evaluate(test_ds)

transformer = TransformerModel(source_vectorization='/content/drive/MyDrive/Project NLP dấu câu /source_vectorization_layer.pkl',
    target_vectorization='/content/drive/MyDrive/Project NLP dấu câu /target_vectorization_layer.pkl',
    model_path='/content/drive/MyDrive/Project NLP dấu câu /restore_diacritic.keras')

print(transformer.predict('co phai em la mua thu ha noi'))
print(transformer.predict('em con nho hay em da quen'))
print(transformer.predict('ha noi mua nay vang nhung con mua'))
print(transformer.predict('dat nuoc toi thon tha giot dan bau'))
print(transformer.predict('em cua ngay hom qua'))