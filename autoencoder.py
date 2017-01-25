from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras.datasets import mnist
import numpy as np
from keras.callbacks import TensorBoard

import gzip
from keras.utils.data_utils import get_file
from six.moves import cPickle
import sys

from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split

nb_channels = 3
rows, cols = 1120, 1120

def load_data(path='/Users/mnpappo/Documents/projects/python/neural_network/date_sort_nn/file.pkl.gz'):
    path = get_file(path, '')

    if path.endswith('.gz'):
        f = gzip.open(path, 'rb')
    else:
        f = open(path, 'rb')

    if sys.version_info < (3,):
        data = cPickle.load(f)
    else:
        data = cPickle.load(f, encoding='bytes')

    f.close()

    print (len(data))

    print ("white", data[0].shape)
    print ("black", data[1].shape)

    return data[0].reshape(len(data[0]), nb_channels, rows, cols) / np.float32(255), data[1].reshape(len(data[1]), nb_channels, rows, cols) / np.float32(255)  # (x_train, y_train )


white, black = load_data()
white, black = shuffle(white, black, random_state=100)

X_train, X_test, y_train, y_test = train_test_split(white, black, test_size = 0.2, random_state = 100)


# (x_train, _), (x_test, _) = load_data()
#
# x_train = x_train.astype('float32') / 255.
# x_test = x_test.astype('float32') / 255.
# x_train = np.reshape(x_train, (len(x_train), 1, 28, 28))
# x_test = np.reshape(x_test, (len(x_test), 1, 28, 28))



input_img = Input(shape=(nb_channels, rows, cols))

x = Convolution2D(16, 3, 3, activation='relu', border_mode='same', name="c1")(input_img)
x = MaxPooling2D((2, 2), border_mode='same')(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same', name="c2")(x)
x = MaxPooling2D((2, 2), border_mode='same')(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same', name="c3")(x)
encoded = MaxPooling2D((2, 2), border_mode='same')(x)

# at this point the representation is (8, 4, 4) i.e. 128-dimensional

x = Convolution2D(8, 3, 3, activation='relu', border_mode='same', name="c4")(encoded)
x = UpSampling2D((2, 2))(x)
x = Convolution2D(8, 3, 3, activation='relu', border_mode='same', name="c5")(x)
x = UpSampling2D((2, 2))(x)
x = Convolution2D(16, 3, 3, activation='relu')(x)
x = UpSampling2D((2, 2))(x)
decoded = Convolution2D(1, 3, 3, activation='sigmoid', border_mode='same', name="c6")(x)

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')



autoencoder.fit(X_train, y_train,
                nb_epoch=2,
                batch_size=16,
                shuffle=True,
                validation_data=(X_test, y_test),
                callbacks=[TensorBoard(log_dir='/tmp/autoencoder')])
