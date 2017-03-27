from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model, model_from_json
from keras.datasets import mnist
import numpy as np
from keras.callbacks import TensorBoard

import gzip
from keras.utils.data_utils import get_file
from six.moves import cPickle
import hickle as hkl
import sys

from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split
from keras import backend as K
from keras.utils import np_utils
from PIL import Image
import matplotlib.pyplot as plt
import scipy.misc
import h5py


nb_channels = 1
kernel = 3
rows, cols = 596, 92
nb_epoch = 2
batch_size = 4

def load_data():
    print("loading dataset................")
    with h5py.File('dataset_slide.h5', 'r') as hf:
        data = hf['dataset'][:]

    print(data.shape)
    doc = data[0].reshape(len(data[0]), nb_channels, rows, cols)
    mask = data[1].reshape(len(data[1]), nb_channels, rows, cols)
    return  doc, mask


white, black = load_data()
# white, black = shuffle(white, black, random_state=100)

x_train, x_test, y_train, y_test = train_test_split(white, black, test_size = 0.2, random_state = 100)

# print(x_train.shape)
# img_arr = x_train[-1, :, :, :]
# print(img_arr.shape)
# img = img_arr.reshape((512,512))
# img = Image.fromarray(img, 'L')
# img.save('test.png')


print ("------------")
print ("training on {n} images".format(n=len(x_train)))
print ("testing on {n} images".format(n=len(x_test)))
print ("------------")


input_img = Input(shape=(nb_channels, rows, cols))
print ("input image shape: 1x596x92")
print ("------------")

x = Convolution2D(32, kernel, kernel, activation='relu', border_mode='same', name="c1")(input_img)
x = MaxPooling2D((2, 2), border_mode='same')(x)

x = Convolution2D(32, kernel, kernel, activation='relu', border_mode='same', name="c2")(x)
x = MaxPooling2D((2, 2), border_mode='same')(x)

x = Convolution2D(64, kernel, kernel, activation='relu', border_mode='same', name="c3")(x)
x = MaxPooling2D((2, 2), border_mode='same')(x)

x = Convolution2D(128, kernel, kernel, activation='relu', border_mode='same', name="c4")(x)
x = MaxPooling2D((2, 2), border_mode='same')(x)

x = Convolution2D(256, kernel, kernel, activation='relu', border_mode='same', name="c5")(x)
x = MaxPooling2D((2, 2), border_mode='same')(x)

x = Convolution2D(256, kernel, kernel, activation='relu', border_mode='same', name="c6")(x)
x = MaxPooling2D((2, 2), border_mode='same')(x)

x = Flatten()(x)
x = Dense(64)(x)
x = Activation('relu')(x)
x = Dropout(0.5)(x)

x = Dense(nb_class)(x)
final = Activation('sigmoid')(x)

model = Model(input_img, final)


autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

# model.compile(loss="categorical_crossentropy", optimizer="sgd")
autoencoder.summary()

autoencoder.fit(x_train, y_train,
                nb_epoch=nb_epoch,
                batch_size=batch_size,
                shuffle=True,
                validation_data=(x_test, y_test),
                callbacks=[TensorBoard(log_dir='/tmp/autoencoder')])


# date localizing test
# serialize model to JSON
model_json = autoencoder.to_json()
with open("localizing_slide.json", "w") as json_file:
    json_file.write(model_json)

autoencoder.save_weights('localizing_slide.h5')
