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


nb_channels = 3
kernel = 3
rows, cols = 768, 768
nb_epoch = 2
batch_size = 4

def load_data():
    print("loading dataset................")
    with h5py.File('dataset_raw.h5', 'r') as hf:
        data = hf['dataset'][:]

    return data[0].reshape(len(data[0]), nb_channels, rows, cols) , data[1].reshape(len(data[1]), nb_channels, rows, cols)


white, black = load_data()
# white, black = shuffle(white, black, random_state=100)

x_train, x_test, y_train, y_test = train_test_split(white, black, test_size = 0.2, random_state = 100)

# img_arr = y_test[0:1:1,:,:,:]
# img = scipy.misc.toimage(img_arr.reshape(3,596,596), channel_axis=0)
# img.show()
# print(img_arr.shape)


print ("------------")
print ("training on {n} images".format(n=len(x_train)))
print ("testing on {n} images".format(n=len(x_test)))
print ("------------")


input_img = Input(shape=(nb_channels, rows, cols))
print ("input image shape: 3x596x596")
print ("------------")

x = Convolution2D(16, kernel, kernel, activation='relu', border_mode='same', name="c1")(input_img)
x = MaxPooling2D((2, 2), border_mode='same')(x)
x = Convolution2D(8, kernel, kernel, activation='relu', border_mode='same', name="c2")(x)
x = MaxPooling2D((2, 2), border_mode='same')(x)
x = Convolution2D(8, kernel, kernel, activation='relu', border_mode='same', name="c3")(x)
encoded = MaxPooling2D((2, 2), border_mode='same')(x)

# at this point the representation is (8, 4, 4) i.e. 128-dimensional

x = Convolution2D(8, kernel, kernel, activation='relu', border_mode='same', name="c4")(encoded)
x = UpSampling2D((2, 2))(x)
x = Convolution2D(8, kernel, kernel, activation='relu', border_mode='same', name="c5")(x)
x = UpSampling2D((2, 2))(x)
x = Convolution2D(16, kernel, kernel, activation='relu', border_mode='same', name="c6")(x)
x = UpSampling2D((2, 2))(x)
decoded = Convolution2D(3, kernel, kernel, activation='sigmoid', border_mode='same', name="c7")(x)

autoencoder = Model(input_img, decoded)
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
with open("localizing_raw.json", "w") as json_file:
    json_file.write(model_json)

autoencoder.save_weights('localizing_raw.h5')
