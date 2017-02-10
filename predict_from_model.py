from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model, model_from_json
from keras.datasets import mnist
import numpy as np
from keras.callbacks import TensorBoard

import gzip
from keras.utils.data_utils import get_file
from six.moves import cPickle
import sys

from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split
from keras import backend as K
from keras.utils import np_utils
from PIL import Image
import matplotlib.pyplot as plt
import scipy.misc
import h5py
from PIL import Image, ImageMath


nb_channels = 3
kernel = 3
rows, cols = 512, 512
nb_epoch = 2
batch_size = 4

def load_data():
    print("\nloading dataset")
    with h5py.File('dataset.h5', 'r') as hf:
        data = hf['dataset'][:]

    return data[0].reshape(len(data[0]), nb_channels, rows, cols) , data[1].reshape(len(data[1]), nb_channels, rows, cols)


white, black = load_data()

x_train, x_test, y_train, y_test = train_test_split(white, black, test_size = 0.2, random_state = 100)

json_file_path = 'localizing.json'
weight_file_path = 'localizing.h5'
images_to_predict = x_test[0:3:1,:,:,:]
masks = y_test[0:3:1,:,:,:]

# img_arr = y_test[0:1:1,:,:,:]
# img = scipy.misc.toimage(img_arr.reshape(3,512,512), channel_axis=0)
# img.show()

print("predicting on {n} images.".format(n=len(images_to_predict)))


def predict_from_model(model_json_path, model_weight_path, images_to_predict):
    """
    model_weight_path : model weight file path
    model_json_path : odel json file path
    images_to_predict : 4 dimentional images as numpy array to predict.
        Example : (10,3,596,596)

    returns predicted images as numpy array
    """
    json_file = open(model_json_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()

    model = model_from_json(loaded_model_json)

    model.load_weights(model_weight_path)
    predicted_images = model.predict(images_to_predict)
    return predicted_images


def plot_from_predicted_images(predicted_images, images_to_predict, masks):
    """
    predicted_images : 4 dimentional images predicted by model.
        dimention example : (10,3,596,596)
    images_to_predict : 4 dimentional images as numpy array to predict.
        dimention example : (10,3,596,596)

    returns predicted images as numpy array
    """
    n = len(images_to_predict)
    plt.figure(figsize=(n*14, n*7))
    for i in range(n):
        # display original
        ax = plt.subplot(3, n, i+1)
        imgx = images_to_predict[i]
        imgx = np.moveaxis(imgx, -1, 0)
        imgx = np.moveaxis(imgx, -1, 0)
        plt.imshow(imgx)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # display original
        ax = plt.subplot(3, n, i+n+1)
        imgq = masks[i]
        imgq = np.moveaxis(imgq, -1, 0)
        imgq = np.moveaxis(imgq, -1, 0)
        plt.imshow(imgq)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # display reconstruction
        ax = plt.subplot(3, n, i +2*n+1)
        img = predicted_images[i]
        img = np.moveaxis(img, -1, 0)
        img = np.moveaxis(img, -1, 0)
        plt.imshow(img)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.savefig('plotted_prediction.png')
    # plt.show()


predicted_images = predict_from_model(json_file_path, weight_file_path, images_to_predict)
plot_from_predicted_images(predicted_images, images_to_predict, masks)
