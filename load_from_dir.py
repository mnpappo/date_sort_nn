from keras.layers import Input, Dense, Convolution2D, MaxPooling2D, UpSampling2D
from keras.models import Model
from keras.preprocessing.image import ImageDataGenerator

def load_data(datapath, train_start, train_end, n_training_examples, n_test_examples):
    X_train = HDF5Matrix(datapath, 'features', train_start, train_start+n_training_examples, normalizer=normalize_data)
    y_train = HDF5Matrix(datapath, 'targets', train_start, train_start+n_training_examples)
    X_test = HDF5Matrix(datapath, 'features', test_start, test_start+n_test_examples, normalizer=normalize_data)
    y_test = HDF5Matrix(datapath, 'targets', test_start, test_start+n_test_examples)
    return X_train, y_train, X_test, y_test



# dimensions of our images.
img_width, img_height = 596, 596

train_x_dir = './data/train_x_dir/'
train_y_dir = './data/train_y_dir/'
test_x_dir = './data/test_x_dir/'
test_y_dir = './data/test_y_dir/'

nb_train_samples = 200
nb_validation_samples = 50
nb_epoch = 50
batch_size = 32

input_img = Input(shape=(nb_channels, rows, cols))

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
x = Convolution2D(16, kernel, kernel, activation='relu')(x)
x = UpSampling2D((2, 2))(x)
decoded = Convolution2D(3, kernel, kernel, activation='sigmoid', border_mode='same', name="c6")(x)

autoencoder = Model(input_img, decoded)
autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')

def fixed_generator(generator):
    for batch in generator:
        yield (batch, batch)


# this is the augmentation configuration we will use for training
datagen = ImageDataGenerator( rescale=1./255, shear_range=0.2, zoom_range=0.2, horizontal_flip=True)
test_datagen = ImageDataGenerator(rescale=1./255)
train_generator = datagen.flow_from_directory( train_x_dir, target_size=(img_width, img_height), batch_size=batch_size, class_mode=None)


print type(train_generator)

validation_generator = test_datagen.flow_from_directory( validation_data_dir, target_size=(img_width, img_height), batch_size=batch_size, class_mode=None)

autoencoder.fit_generator(
        fixed_generator(train_generator),
        samples_per_epoch=nb_train_samples,
        nb_epoch=nb_epoch,
        validation_data=fixed_generator(validation_generator),
        nb_val_samples=nb_validation_samples
        )
