from PIL import Image, ImageOps
import os
import glob
import math

file_location = './resized_images_white/'
file_location_black = './resized_images_black/'

image_save_path_white = "./resized_images_white_x/"
image_save_path_black = "./resized_images_black_x/"

image_file_directory = os.path.join(file_location, '*.png')
image_file_list = glob.glob(image_file_directory)
image_file_list = image_file_list[0:100:1]

def get_max_img_height_from_direcory(direcory):
    image_file_directory = os.path.join(direcory, '*.png')
    image_file_list = glob.glob(image_file_directory)
    index = 0
    max_height = 0
    for image in image_file_list:
        image = Image.open(file_location + '{id}.png'.format(id=index))
        width, height = image.size
        if max_height < height:
            max_height = height
        index += 1
    return max_height


# print(get_max_img_height_from_direcory(file_location))

def resize_image_from_direcory(source_dir, target_dir):
    index = 0
    # max_height = get_max_img_height_from_direcory(source_dir)
    max_height = 596
    # rounding up to *10
    # max_height = int(math.ceil(max_height / 10.0)) * 10
    for image in image_file_list:
        image = Image.open(source_dir + '{id}.png'.format(id=index))
        # image = image.crop((0, 0, 1000, max_height))
        image = ImageOps.fit(image, (max_height, max_height), Image.ANTIALIAS, centering=(0.0, 0.0))
        width, height = image.size
        print("resized image {id}. new size is: ".format(id=index), image.size)
        image.save(target_dir + "{id}.png".format(id=index))
        index += 1
    return True


if resize_image_from_direcory(file_location, image_save_path_white) is True:
    print("All white resize job done. :) ")

if resize_image_from_direcory(file_location_black, image_save_path_black) is True:
    print("All black resize job done. :) ")
