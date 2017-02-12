from keras.models import Model
from keras.callbacks import TensorBoard
from keras.layers import (
    Input,
    Activation,
    merge,
    Dense,
    Flatten
)
from keras.layers.convolutional import (
    Convolution2D,
    Deconvolution2D,
    MaxPooling2D,
    UpSampling2D,
    AveragePooling2D
)
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from keras import backend as K
import h5py
from sklearn.cross_validation import train_test_split
from keras.utils.visualize_util import plot


nb_channels = 3
kernel = 3
rows, cols = 512, 512
nb_epoch = 100
batch_size = 12

def load_data():
    print("loading dataset................")
    with h5py.File('dataset.h5', 'r') as hf:
        data = hf['dataset'][:]

    return data[0].reshape(len(data[0]), nb_channels, rows, cols) , data[1].reshape(len(data[1]), nb_channels, rows, cols)


white, black = load_data()
# white, black = shuffle(white, black, random_state=100)

x_train, x_test, y_train, y_test = train_test_split(white, black, test_size = 0.2, random_state = 100)

# img_arr = x_train[0:1:1,:,:,:]
# img = misc.toimage(img_arr.reshape(3,512,512), channel_axis=0)
# print(img_arr.shape)


def _bn_relu(input):
    """Helper to build a BN -> relu block
    """
    norm = BatchNormalization(mode=0, axis=CHANNEL_AXIS)(input)
    return Activation("relu")(norm)


def _conv_bn_relu(**conv_params):
    """Helper to build a conv -> BN -> relu block
    """
    nb_filter = conv_params["nb_filter"]
    nb_row = conv_params["nb_row"]
    nb_col = conv_params["nb_col"]
    subsample = conv_params.setdefault("subsample", (1, 1))
    init = conv_params.setdefault("init", "he_normal")
    border_mode = conv_params.setdefault("border_mode", "same")
    W_regularizer = conv_params.setdefault("W_regularizer", l2(1.e-4))

    def f(input):
        conv = Convolution2D(nb_filter=nb_filter, nb_row=nb_row, nb_col=nb_col, subsample=subsample,
                             init=init, border_mode=border_mode, W_regularizer=W_regularizer)(input)
        return _bn_relu(conv)

    return f


def _conv_bn_relu_dc(**conv_params):
    """Helper to build a conv -> BN -> relu block
    """
    nb_filter = conv_params["nb_filter"]
    nb_row = conv_params["nb_row"]
    nb_col = conv_params["nb_col"]
    subsample = conv_params.setdefault("subsample", (1, 1))
    init = conv_params.setdefault("init", "he_normal")
    border_mode = conv_params.setdefault("border_mode", "same")
    W_regularizer = conv_params.setdefault("W_regularizer", l2(1.e-4))

    def f(input):
        conv = Deconvolution2D(nb_filter=nb_filter, nb_row=nb_row, nb_col=nb_col, subsample=subsample,
                             init=init, border_mode=border_mode, W_regularizer=W_regularizer)(input)

        return _bn_relu(conv)

    return f


def _bn_relu_conv(**conv_params):
    """Helper to build a BN -> relu -> conv block.
    This is an improved scheme proposed in http://arxiv.org/pdf/1603.05027v2.pdf
    """
    nb_filter = conv_params["nb_filter"]
    nb_row = conv_params["nb_row"]
    nb_col = conv_params["nb_col"]
    subsample = conv_params.setdefault("subsample", (1,1))
    init = conv_params.setdefault("init", "he_normal")
    border_mode = conv_params.setdefault("border_mode", "same")
    W_regularizer = conv_params.setdefault("W_regularizer", l2(1.e-4))

    def f(input):
        activation = _bn_relu(input)
        return Convolution2D(nb_filter=nb_filter, nb_row=nb_row, nb_col=nb_col, subsample=subsample,
                             init=init, border_mode=border_mode, W_regularizer=W_regularizer)(activation)

    return f


def _bn_relu_conv_dc(**conv_params):
    """Helper to build a BN -> relu -> conv block.
    This is an improved scheme proposed in http://arxiv.org/pdf/1603.05027v2.pdf
    """
    nb_filter = conv_params["nb_filter"]
    nb_row = conv_params["nb_row"]
    nb_col = conv_params["nb_col"]
    subsample = conv_params.setdefault("subsample", (1,1))
    init = conv_params.setdefault("init", "he_normal")
    border_mode = conv_params.setdefault("border_mode", "same")
    W_regularizer = conv_params.setdefault("W_regularizer", l2(1.e-4))

    def f(input):
        activation = _bn_relu(input)
        conv1 = Convolution2D(nb_filter=nb_filter, nb_row=nb_row, nb_col=nb_col, subsample=subsample,
                             init=init, border_mode="same", W_regularizer=W_regularizer)(activation)
        return UpSampling2D(size=subsample)(conv1)


    return f


def _shortcut(input, residual):
    """Adds a shortcut between input and residual block and merges them with "sum"
    """
    # Expand channels of shortcut to match residual.
    # Stride appropriately to match residual (width, height)
    # Should be int if network architecture is correctly configured.
    # print ("input", input._keras_shape[ROW_AXIS])
    # print ("residual", residual._keras_shape[COL_AXIS])
    # print ("input", input._keras_shape[ROW_AXIS])
    # print ("residual", residual._keras_shape[COL_AXIS])

    stride_width = input._keras_shape[ROW_AXIS] // residual._keras_shape[ROW_AXIS]
    stride_height = input._keras_shape[COL_AXIS] // residual._keras_shape[COL_AXIS]
    equal_channels = residual._keras_shape[CHANNEL_AXIS] == input._keras_shape[CHANNEL_AXIS]

    shortcut = input
    # 1 X 1 conv if shape is different. Else identity.
    if stride_width > 1 or stride_height > 1 or not equal_channels:
        shortcut = Convolution2D(nb_filter=residual._keras_shape[CHANNEL_AXIS],
                                 nb_row=1, nb_col=1,
                                 subsample=(stride_width, stride_height),
                                 init="he_normal", border_mode="valid",
                                 W_regularizer=l2(0.0001))(input)

    return merge([shortcut, residual], mode="sum")


def _shortcut_dc(input, residual):
    """Adds a shortcut between input and residual block and merges them with "sum"
    """
    # Expand channels of shortcut to match residual.
    # Stride appropriately to match residual (width, height)
    # Should be int if network architecture is correctly configured.
    # print ("input", input._keras_shape[ROW_AXIS])
    # print ("residual", residual._keras_shape[COL_AXIS])
    # print ("input", input._keras_shape[ROW_AXIS])
    # print ("residual", residual._keras_shape[COL_AXIS])

    stride_width = residual._keras_shape[ROW_AXIS] // input._keras_shape[ROW_AXIS]
    stride_height = residual._keras_shape[COL_AXIS] // input._keras_shape[COL_AXIS]
    equal_channels = input._keras_shape[CHANNEL_AXIS] == residual._keras_shape[CHANNEL_AXIS]

    shortcut = input
    # 1 X 1 conv if shape is different. Else identity.
    if stride_width > 1 or stride_height > 1 or not equal_channels:
        conv1 = Convolution2D(nb_filter=residual._keras_shape[CHANNEL_AXIS],
                                 nb_row=1, nb_col=1,
                                 subsample=(stride_width, stride_height),
                                 init="he_normal", border_mode="same",
                                 W_regularizer=l2(0.0001))(input)
        shortcut = UpSampling2D(size=(4, 4))(conv1)

    return merge([shortcut, residual], mode="sum")



def _residual_block(block_function, nb_filter, repetitions, is_first_layer=False):
    """Builds a residual block with repeating bottleneck blocks.
    """
    def f(input):
        for i in range(repetitions):
            init_subsample = (1, 1)
            if i == 0 and not is_first_layer:
                init_subsample = (2, 2)
            input = block_function(
                    nb_filter=nb_filter,
                    init_subsample=init_subsample,
                    is_first_block_of_first_layer=(is_first_layer and i == 0)
                )(input)
        return input

    return f


def _residual_block_dc(block_function, nb_filter, repetitions, is_first_layer=False):
    """Builds a residual block with repeating bottleneck blocks.
    """
    def f(input):
        for i in range(repetitions):
            init_subsample = (1, 1)
            if i == 0 and not is_first_layer:
                init_subsample = (2, 2)
            input = block_function(
                    nb_filter=nb_filter,
                    init_subsample=init_subsample,
                    is_first_block_of_first_layer=(is_first_layer and i == 0)
                )(input)
        return input

    return f


def basic_block(nb_filter, init_subsample=(1, 1), is_first_block_of_first_layer=False):
    """Basic 3 X 3 convolution blocks for use on resnets with layers <= 34.
    Follows improved proposed scheme in http://arxiv.org/pdf/1603.05027v2.pdf
    """
    def f(input):

        if is_first_block_of_first_layer:
            # don't repeat bn->relu since we just did bn->relu->maxpool
            conv1 = Convolution2D(nb_filter=nb_filter,
                                 nb_row=3, nb_col=3,
                                 subsample=init_subsample,
                                 init="he_normal", border_mode="same",
                                 W_regularizer=l2(0.0001))(input)
        else:
            conv1 = _bn_relu_conv(nb_filter=nb_filter, nb_row=3, nb_col=3, subsample=init_subsample)(input)

        residual = _bn_relu_conv(nb_filter=nb_filter, nb_row=3, nb_col=3)(conv1)
        return _shortcut(input, residual)

    return f


def basic_block_dc(nb_filter, init_subsample=(1, 1), is_first_block_of_first_layer=False):
    """Basic 3 X 3 convolution blocks for use on resnets with layers <= 34.
    Follows improved proposed scheme in http://arxiv.org/pdf/1603.05027v2.pdf
    """
    def f(input):

        if is_first_block_of_first_layer:
            # don't repeat bn->relu since we just did bn->relu->maxpool
            conv1 = Convolution2D(nb_filter=nb_filter,
                                 nb_row=3, nb_col=3,
                                 subsample=init_subsample,
                                 init="he_normal", border_mode="same",
                                 W_regularizer=l2(0.0001))(input)
            # upsampled = UpSampling2D(size=(1,1))(conv1)
        else:
            conv1 = _bn_relu_conv_dc(nb_filter=nb_filter, nb_row=3, nb_col=3, subsample=init_subsample, border_mode="same")(input)
            conv1 = UpSampling2D(size=init_subsample)(conv1)

        residual = _bn_relu_conv_dc(nb_filter=nb_filter, nb_row=3, nb_col=3)(conv1)
        return _shortcut_dc(input, residual)

    return f


def bottleneck(nb_filter, init_subsample=(1, 1), is_first_block_of_first_layer=False):
    """Bottleneck architecture for > 34 layer resnet.
    Follows improved proposed scheme in http://arxiv.org/pdf/1603.05027v2.pdf
    :return: A final conv layer of nb_filter * 4
    """
    def f(input):

        if is_first_block_of_first_layer:
            # don't repeat bn->relu since we just did bn->relu->maxpool
            conv_1_1 = Convolution2D(nb_filter=nb_filter,
                                 nb_row=1, nb_col=1,
                                 subsample=init_subsample,
                                 init="he_normal", border_mode="same",
                                 W_regularizer=l2(0.0001))(input)
        else:
            conv_1_1 = _bn_relu_conv(nb_filter=nb_filter, nb_row=1, nb_col=1, subsample=init_subsample)(input)

        conv_3_3 = _bn_relu_conv(nb_filter=nb_filter, nb_row=3, nb_col=3)(conv_1_1)
        residual = _bn_relu_conv(nb_filter=nb_filter * 4, nb_row=1, nb_col=1)(conv_3_3)
        return _shortcut(input, residual)

    return f


def handle_dim_ordering():
    global ROW_AXIS
    global COL_AXIS
    global CHANNEL_AXIS
    if K.image_dim_ordering() == 'tf':
        ROW_AXIS = 1
        COL_AXIS = 2
        CHANNEL_AXIS = 3
    else:
        CHANNEL_AXIS = 1
        ROW_AXIS = 2
        COL_AXIS = 3


class ResnetBuilder(object):
    @staticmethod
    def build(input_shape, block_fn, repetitions):
        """Builds a custom ResNet like architecture.
        :param input_shape: The input shape in the form (nb_channels, nb_rows, nb_cols)
        :param block_fn: The block function to use. This is either :func:`basic_block` or :func:`bottleneck`.
        The original paper used basic_block for layers < 50
        :param repetitions: Number of repetitions of various block units.
        At each block unit, the number of filters are doubled and the input size is halved
        :return: The keras model.
        """
        handle_dim_ordering()
        if len(input_shape) != 3:
            raise Exception("Input shape should be a tuple (nb_channels, nb_rows, nb_cols)")

        # Permute dimension order if necessary
        if K.image_dim_ordering() == 'tf':
            input_shape = (input_shape[1], input_shape[2], input_shape[0])

        input = Input(shape=input_shape)
        conv1 = _conv_bn_relu(nb_filter=128, nb_row=7, nb_col=7, subsample=(2, 2))(input)
        pool1 = MaxPooling2D(pool_size=(3, 3), strides=(2, 2), border_mode="same")(conv1)

        block = pool1
        nb_filter = 128
        for i, r in enumerate(repetitions):
            block = _residual_block(block_fn, nb_filter=nb_filter, repetitions=r, is_first_layer=(i == 0))(block)
            nb_filter /= 2

        encoded = block


        block_fn = basic_block_dc

        # upsampled = UpSampling2D(size=(2, 2))(conv1)

        block = encoded
        nb_filter = 16
        repetitions.append(repetitions[-1])
        # repetitions = [3, 4, 6, 3, 3]
        for i, r in enumerate(repetitions):
            block = _residual_block_dc(block_fn, nb_filter=nb_filter, repetitions=r, is_first_layer=(i == 0))(block)
            nb_filter *= 2

        norm = _bn_relu(block)
        # conv1 = _conv_bn_relu(nb_filter=128, nb_row=7, nb_col=7, border_mode="same")(norm)
        decoded = UpSampling2D(size=(2, 2))(norm)

        decoded = _conv_bn_relu(nb_filter=3, nb_row=3, nb_col=3, border_mode="same")(decoded)

        model = Model(input=input, output=decoded)
        return model

    @staticmethod
    def build_resnet_18(input_shape):
        return ResnetBuilder.build(input_shape, basic_block, [2, 2, 2, 2])

    @staticmethod
    def build_resnet_34(input_shape):
        return ResnetBuilder.build(input_shape, basic_block, [3, 4, 6, 3])

    @staticmethod
    def build_resnet_50(input_shape):
        return ResnetBuilder.build(input_shape, bottleneck, [3, 4, 6, 3])

    @staticmethod
    def build_resnet_101(input_shape):
        return ResnetBuilder.build(input_shape, bottleneck, [3, 4, 23, 3])

    @staticmethod
    def build_resnet_152(input_shape):
        return ResnetBuilder.build(input_shape, bottleneck, [3, 8, 36, 3])


def main():
    # autoencoder = ResnetBuilder.build_resnet_18((3, 512, 512))
    autoencoder = ResnetBuilder.build_resnet_34((3, 768, 768))
    autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
    autoencoder.summary()
    # plot(autoencoder, to_file='model.png')
    # plot(autoencoder, to_file='model_with_name.png', show_shapes=True)
    #
    # autoencoder.fit(x_train, y_train,
    #                 nb_epoch=nb_epoch,
    #                 batch_size=batch_size,
    #                 shuffle=True,
    #                 validation_data=(x_test, y_test),
    #                 callbacks=[TensorBoard(log_dir='/tmp/autoencoder')])
    #
    #
    # # serialize model to JSON
    # model_json = autoencoder.to_json()
    # with open("localizing_resnet.json", "w") as json_file:
    #     json_file.write(model_json)
    #
    # autoencoder.save_weights('localizing_resnet.h5')


if __name__ == '__main__':
    main()
