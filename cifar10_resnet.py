"""
Adapted from keras example cifar10_cnn.py
Train ResNet-18 on the CIFAR10 small images dataset.
GPU run command with Theano backend (with TensorFlow, the GPU is automatically used):
    THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python cifar10.py
"""

from __future__ import print_function
from keras.datasets import cifar10
from keras.preprocessing.image import ImageDataGenerator
from keras.utils import np_utils
from keras.callbacks import ReduceLROnPlateau, CSVLogger, EarlyStopping
import numpy as np
import h5py
from sklearn.cross_validation import train_test_split

import resnet

lr_reducer = ReduceLROnPlateau(monitor='val_loss', factor=np.sqrt(0.1), cooldown=0, patience=5, min_lr=0.5e-6)
early_stopper = EarlyStopping(monitor='val_acc', min_delta=0.001, patience=10)
csv_logger = CSVLogger('resnet18_cifar10.csv')

# batch_size = 32
# nb_classes = 10
# nb_epoch = 200
# data_augmentation = True
#
# # input image dimensions
# img_rows, img_cols = 32, 32
# # The CIFAR10 images are RGB.
# img_channels = 3
#
# # The data, shuffled and split between train and test sets:
# (X_train, y_train), (X_test, y_test) = cifar10.load_data()



nb_channels = 3
img_channels = nb_channels
kernel = 3
rows, cols = 596, 596
img_rows, img_cols = rows, cols
nb_epoch = 2
batch_size = 4
data_augmentation = False
nb_classes = 10


def load_data():
    print("loading dataset................")
    with h5py.File('dataset.h5', 'r') as hf:
        data = hf['dataset'][:]

    return data[0].reshape(len(data[0]), nb_channels, rows, cols) , data[1].reshape(len(data[1]), nb_channels, rows, cols)


white, black = load_data()
# white, black = shuffle(white, black, random_state=100)

x_train, x_test, y_train, y_test = train_test_split(white, black, test_size = 0.2, random_state = 100)



# # Convert class vectors to binary class matrices.
# Y_train = np_utils.to_categorical(y_train, nb_classes)
# Y_test = np_utils.to_categorical(y_test, nb_classes)
#
# X_train = X_train.astype('float32')
# X_test = X_test.astype('float32')
#
# # subtract mean and normalize
# mean_image = np.mean(X_train, axis=0)
# X_train -= mean_image
# X_test -= mean_image
# X_train /= 128.
# X_test /= 128.

model = resnet.ResnetBuilder.build_resnet_18((img_channels, img_rows, img_cols), nb_classes)
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

if not data_augmentation:
    print('Not using data augmentation.')
    model.fit(x_train, y_train,
              batch_size=batch_size,
              nb_epoch=nb_epoch,
              validation_data=(x_test, y_test),
              shuffle=True,
              callbacks=[lr_reducer, early_stopper, csv_logger])
else:
    print('Using real-time data augmentation.')
    # This will do preprocessing and realtime data augmentation:
    datagen = ImageDataGenerator(
        featurewise_center=False,  # set input mean to 0 over the dataset
        samplewise_center=False,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=0,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images

    # Compute quantities required for featurewise normalization
    # (std, mean, and principal components if ZCA whitening is applied).
    datagen.fit(x_train)

    # Fit the model on the batches generated by datagen.flow().
    model.fit_generator(datagen.flow(x_train, y_train, batch_size=batch_size),
                        samples_per_epoch=x_train.shape[0],
                        validation_data=(x_test, y_test),
                        nb_epoch=nb_epoch, verbose=1, max_q_size=100,
                        callbacks=[lr_reducer, early_stopper, csv_logger])
