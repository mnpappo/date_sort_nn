from PIL import Image, ImageOps
import os
import glob
import math
from tqdm import tqdm
from resizeimage import resizeimage
from skimage import color
from skimage import io
import simplejson
#


file_location = './test/'

image_save_path = "./if_date_data/"

image_file_directory = os.path.join(file_location, '*.png')
image_file_list = glob.glob(image_file_directory)

# image_file_list = image_file_list[1300:1310:1]

def get_max_img_height_from_direcory(direcory):
    image_file_directory = os.path.join(direcory, '*.png')
    image_file_list = glob.glob(image_file_directory)
    pbar = tqdm(total=len(image_file_list))
    index = 0
    max_height = 0
    max_width = 0
    for image in image_file_list:
        image = Image.open(image)
        width, height = image.size
        if max_height < height:
            max_height = height
        if max_width < width:
            max_width = width
        index += 1
        pbar.update(1)
    return max_width, max_height


# print(get_max_img_height_from_direcory(file_location))

def resize_image_from_direcory(source_dir, target_dir):
    index = 0
    max_width, max_height = get_max_img_height_from_direcory(source_dir)
    max_width = 192
    max_height = 48
    # rounding up to *10
    # max_height = int(math.ceil(max_height / 10.0)) * 10
    pbar = tqdm(total=len(image_file_list))
    for image in image_file_list:
        image = Image.open(image).convert('L')
        # image = image.crop((0, 0, 1000, max_height))
        # image = ImageOps.fit(image, (max_width, max_height), Image.ANTIALIAS)
        # image.thumbnail((596,596), Image.ANTIALIAS)

        #
        image = resizeimage.resize_contain(image, [max_width, max_height])

        # width, height = image.size
        # print("resized image {id}. new size is: ".format(id=index), image.size)

        image.save(target_dir + "{id}.png".format(id=index))
        index += 1
        pbar.update(1)
    return True



# resize_image_from_direcory(file_location, image_save_path)

##### Transparent to black bg#############

# image_save_path = "./if_date_data_156x48/"

# file_location = './data/date/'
file_location = './data/not_date/'
image_save_path = "./bin_date_data/"

image_file_directory = os.path.join(file_location, '*.png')
image_file_list = glob.glob(image_file_directory)

def transparent_to_black():
    index = 45265
    pbar = tqdm(total=len(image_file_list))
    for image in image_file_list:
        image = Image.open(image)
        pixdata = image.load()
        width, height = image.size
        for y in xrange(height):
            for x in xrange(width):
                if pixdata[x, y] == (255, 255, 255, 0):
                    pixdata[x, y] = (0, 0, 0, 255)

        width, height = image.size
        image.save(image_save_path + "{id}.png".format(id=index))
        index += 1
        pbar.update(1)


# transparent_to_black()

print("hola")
data = {}

file_location = './test/'

image_file_directory = os.path.join(file_location, '*.png')
image_file_list = glob.glob(image_file_directory)

image_save_path_date = './data/date/'
image_save_path_not_date = './data/not_date/'

# image_file_list = image_file_list[0:100:1]


# date_list = np.array([0,3,10,11,14])
def create_labels():
    max_width = 192
    max_height = 48
    i = 0
    pbar = tqdm(total=len(image_file_list))
    image_index = 0
    for image in range(len(image_file_list)):
        date_list = [0,3,10,11,14]
        image = './test/'+str(image)+'.png'
        if i in date_list:
            data_type = 1
            image = Image.open(image).convert('L')
            image = resizeimage.resize_contain(image, [max_width, max_height])
            image.save(image_save_path_date + "{id}.png".format(id=image_index))
            # print(image_index)
        else:
            data_type = 0
            image = Image.open(image).convert('L')
            image = resizeimage.resize_contain(image, [max_width, max_height])
            image.save(image_save_path_not_date + "{id}.png".format(id=image_index))
            # print(image_index)

        data[image_index] = data_type
        i += 1
        if i >= 17:
            i = 0
        pbar.update(1)
        image_index += 1

    print(len(data))
    f = open('labelsx.json', 'w')
    simplejson.dump(data, f)
    f.close()

# create_labels()
