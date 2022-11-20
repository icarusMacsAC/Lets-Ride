
# import re
# import os
# import string
# from time import time


# import json
import pickle
# import glob

# import cv2
# from PIL import Image
import numpy as np

# from numpy import array
# import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt


# from sklearn.model_selection import train_test_split
# from sklearn.metrics.pairwise import cosine_similarity

from tensorflow import keras
# import tensorflow as tf
# # import tensorflow.compat.v1 as tf1

# from keras.layers.embeddings import Embedding
# from keras.layers.merge import add

# from tensorflow.keras import backend as K
# from tensorflow.keras.datasets import mnist
# from tensorflow.keras import utils
# from keras.layers.wrappers import Bidirectional

# from tensorflow.keras.preprocessing import image
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.applications.inception_v3 import preprocess_input
# from tensorflow.keras.utils import to_categorical
# from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.preprocessing.sequence import pad_sequences
# from tensorflow.keras.applications.vgg16 import VGG16

from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, array_to_img, load_img

# from tqdm import tqdm


def create_inception():
    # model = InceptionV3(weights='imagenet')
    # # model = VGG16(weights='imagenet')
    # model_new = Model(model.input, model.layers[-2].output)
    # return model_new
    # return keras.models.load_model("C:/Users/amit chourey/Documents/computer vision/image_caption/inceptionv3_model.h5")
    return keras.models.load_model("media/model/inceptionv3_model.h5")


inception_model = create_inception()


def create_real_model():
    # return keras.models.load_model("C:/Users/amit chourey/Documents/computer vision/image_caption/model/da_model39.h5")
    return keras.models.load_model("media/model/da_model92.h5")
    return keras.models.load_model("media/model/hello_38.h5")
    # return keras.models.load_model("S:/All Video/MLDL/3_DJANGO/PROJECTS/data/corpus/model/hi_1.h5")
    # return keras.models.load_model("C:/Users/amit chourey/Documents/computer vision/img_capt/model/foot_3.h5")
    # return keras.models.load_model("C:/Users/amit chourey/Documents/computer vision/img_capt/model/tipa_2.h5")


real_model = create_real_model()
print("jsbjhbsh", real_model.summary())


def preprocess(image_path):
    img = load_img(image_path, target_size=(299, 299))
    x = img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return x


def encode(image):
    image = preprocess(image)
    fea_vec = inception_model.predict(image, use_multiprocessing=True)
    fea_vec = np.reshape(fea_vec, fea_vec.shape[1])
    return fea_vec


def load_pickle(name):
    with open(name, "rb") as handle:
        return pickle.load(handle)


def greedySearch(photo):
    max_length = 34
    wordtoix = load_pickle("media/model/wordtoix.pickle")
    ixtoword = load_pickle("media/model/ixtoword.pickle")
    # max_length = 70
    # wordtoix = load_pickle(
    #     "E:/All Video/MLDL/3_DJANGO/PROJECTS/data/corpus/wordtoix.pickle")
    # ixtoword = load_pickle(
    #     "E:/All Video/MLDL/3_DJANGO/PROJECTS/data/corpus/ixtoword.pickle")

    in_text = 'startseq'
    for i in range(max_length):
        sequence = [wordtoix[w] for w in in_text.split() if w in wordtoix]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = real_model.predict(
            [photo, sequence], verbose=0, use_multiprocessing=True)
        yhat = np.argmax(yhat)
        word = ixtoword[yhat]
        in_text += ' ' + word
        if word == 'endseq':
            break

    final = in_text.split()
    final = final[1:-1]
    final = ' '.join(final)
    return final


def beam_search_predictions(image, beam_index=3):
    max_length = 34
    wordtoix = load_pickle("media/model/wordtoix.pickle")
    ixtoword = load_pickle("media/model/ixtoword.pickle")
    # max_length = 70
    # wordtoix = load_pickle(
    #     "E:/All Video/MLDL/3_DJANGO/PROJECTS/data/corpus/wordtoix.pickle")
    # ixtoword = load_pickle(
    #     "E:/All Video/MLDL/3_DJANGO/PROJECTS/data/corpus/ixtoword.pickle")
    image = encode(image).reshape(1, 2048)
    start = [wordtoix["startseq"]]
    start_word = [[start, 0.0]]
    while len(start_word[0][0]) < max_length:
        temp = []
        for s in start_word:
            par_caps = pad_sequences([s[0]], maxlen=max_length, padding='post')
            preds = real_model.predict([image, par_caps], verbose=0)
            word_preds = np.argsort(preds[0])[-beam_index:]
            # Getting the top <beam_index>(n) predictions and creating a
            # new list so as to put them via the model again
            for w in word_preds:
                next_cap, prob = s[0][:], s[1]
                next_cap.append(w)
                prob += preds[0][w]
                temp.append([next_cap, prob])

        start_word = temp
        # Sorting according to the probabilities
        start_word = sorted(start_word, reverse=False, key=lambda l: l[1])
        # Getting the top words
        start_word = start_word[-beam_index:]

    start_word = start_word[-1][0]
    intermediate_caption = [ixtoword[i] for i in start_word]
    final_caption = []

    for i in intermediate_caption:
        if i != 'endseq':
            final_caption.append(i)
        else:
            break

    final_caption = ' '.join(final_caption[1:])
    return final_caption


def generate_text(url):
    test_features = {}
    test_features["img"] = encode(url)
    image = test_features["img"].reshape((1, 2048))
    return greedySearch(image)


# print(real_model.predict([np.zeros(shape=(1, 2048)), np.zeros(shape=(1, 34))], verbose=0))
print(generate_text("media/original/images.jpg"))
# print(beam_search_predictions("media/original/images.jpg"))

if __name__ == '__main__':
    print('jhjvsjs')

    print("hhhahhahh", generate_text("media/original/images.jpg"))
    pass
