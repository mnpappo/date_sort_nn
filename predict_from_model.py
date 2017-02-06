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

def difference1(source, color):
    """When source is bigger than color"""
    return (source - color) / (255.0 - color)

def difference2(source, color):
    """When color is bigger than source"""
    return (color - source) / color


def color_to_alpha(image, color=None):
    image = image.convert('RGBA')
    width, height = image.size

    color = map(float, color)
    img_bands = [band.convert("F") for band in image.split()]

    # Find the maximum difference rate between source and color. I had to use two
    # difference functions because ImageMath.eval only evaluates the expression
    # once.
    alpha = ImageMath.eval(
        """float(
            max(
                max(
                    max(
                        difference1(red_band, cred_band),
                        difference1(green_band, cgreen_band)
                    ),
                    difference1(blue_band, cblue_band)
                ),
                max(
                    max(
                        difference2(red_band, cred_band),
                        difference2(green_band, cgreen_band)
                    ),
                    difference2(blue_band, cblue_band)
                )
            )
        )""",
        difference1=difference1,
        difference2=difference2,
        red_band = img_bands[0],
        green_band = img_bands[1],
        blue_band = img_bands[2],
        cred_band = color[0],
        cgreen_band = color[1],
        cblue_band = color[2]
    )

    # Calculate the new image colors after the removal of the selected color
    new_bands = [
        ImageMath.eval(
            "convert((image - color) / alpha + color, 'L')",
            image = img_bands[i],
            color = color[i],
            alpha = alpha
        )
        for i in xrange(3)
    ]

    # Add the new alpha band
    new_bands.append(ImageMath.eval(
        "convert(alpha_band * alpha, 'L')",
        alpha = alpha,
        alpha_band = img_bands[3]
    ))

    return Image.merge('RGBA', new_bands)


def replace_color(image_path, from_color, to_color):
    image = image_path
    image = color_to_alpha(image, from_color)
    background = Image.new('RGB', image.size, to_color)
    background.paste(image.convert('RGB'), mask=image)

    return background





nb_channels = 3
kernel = 3
rows, cols = 596, 596
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
masks = y_test[0:len(images_to_predict):1,:,:,:]
print("predicting on {n} images.".format(n=len(images_to_predict)))

def predict_from_model(model_json_path, model_weight_path, images_to_predict):
    """
    model_weight_path : model weight file path
    model_json_path : model json file path
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

def plot_from_predicted_images(predicted_images, images_to_predict):
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
        ax = plt.subplot(2, n, i+1)
        imgx = images_to_predict[i]
        imgx = np.moveaxis(imgx, -1, 0)
        imgx = np.moveaxis(imgx, -1, 0)
        plt.imshow(imgx)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)

        # display reconstruction
        ax = plt.subplot(2, n, i + n+1)
        img = predicted_images[i]
        img = np.moveaxis(img, -1, 0)
        img = np.moveaxis(img, -1, 0)

        imgq = masks[i]
        imgq = np.moveaxis(imgq, -1, 0)
        imgq = np.moveaxis(imgq, -1, 0)


        imgy = Image.fromarray(img, 'RGB')
        imgz = Image.fromarray(imgq, 'RGB')
        # imgz = replace_color(imgz, (0,0,0,255), (14, 114, 214))
        imgz = replace_color(imgz, (255, 255, 255, 255), (255, 0, 0))

        abc = Image.blend(imgz, imgy, 0.7)
        abc = np.array(abc)
        plt.imshow(img)
        ax.get_xaxis().set_visible(False)
        ax.get_yaxis().set_visible(False)
    plt.savefig('plotted_prediction.png')
    # plt.show()


predicted_images = predict_from_model(json_file_path, weight_file_path, images_to_predict)
plot_from_predicted_images(predicted_images, images_to_predict)
