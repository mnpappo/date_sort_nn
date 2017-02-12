from PIL import Image, ImageOps
import os
import glob
import math
from tqdm import tqdm
from resizeimage import resizeimage
from skimage import color
from skimage import io

#


file_location = './resized_txt_white/'
file_location_black = './resized_txt_black/'

image_save_path_txt_white = "./gen_doc_gray/"
image_save_path_txt_black = "./gen_mask_gray/"

image_file_directory = os.path.join(file_location, '*.png')
image_file_list = glob.glob(image_file_directory)
# image_file_list = image_file_list[1300:1310:1]

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
    image_file_directory = os.path.join(source_dir, '*.png')
    image_file_list = glob.glob(image_file_directory)
    index = 0
    # max_height = get_max_img_height_from_direcory(source_dir)
    max_height = 768
    # rounding up to *10
    # max_height = int(math.ceil(max_height / 10.0)) * 10
    pbar = tqdm(total=len(image_file_list))
    for image in image_file_list:
        image = Image.open(image).convert('L')
        # image = image.crop((0, 0, 1000, max_height))
        # image = ImageOps.fit(image, (max_height, max_height), Image.ANTIALIAS)
        # image.thumbnail((512,768), Image.ANTIALIAS)

        #
        # image = resizeimage.resize_contain(image, [max_height, max_height])

        # width, height = image.size
        # print("resized image {id}. new size is: ".format(id=index), image.size)

        image.save(target_dir + "{id}.png".format(id=index))
        index += 1
        pbar.update(1)
    return True


if resize_image_from_direcory(file_location, image_save_path_txt_white) is True:
    print("All white resize job done. :) ")


if resize_image_from_direcory(file_location_black, image_save_path_txt_black) is True:
    print("All black resize job done. :) ")



######invert images##############
# from PIL import Image
# import PIL.ImageOps
# import os
# import glob
#
# file_location_black = './raw_doc_resized/'
# image_save_path_txt_black = "./x/"
#
# image_file_directory = os.path.join(file_location_black, '*.png')
# image_file_list = glob.glob(image_file_directory)
#
# index = 0
# for image in image_file_list:
#     image = Image.open(image).convert('L')
#     image = PIL.ImageOps.invert(image)
#     width, height = image.size
#     print("resized image {id}. new size is: ".format(id=index), image.size)
#     image.save(image_save_path_txt_black + "{id}.png".format(id=index))
#     index += 1


##### Transparent to black bg#############
# import os
# import glob
#
# file_location_black = './raw_mask_resized/'
# image_save_path_txt_black = "./raw_mask_resized/"
#
# image_file_directory = os.path.join(file_location_black, '*.png')
# image_file_list = glob.glob(image_file_directory)
#
#
#
# from PIL import Image
# index = 0
# for image in image_file_list:
#     image = Image.open(image)
#     pixdata = image.load()
#     width, height = image.size
#     for y in xrange(height):
#         for x in xrange(width):
#             if pixdata[x, y] == (255, 255, 255, 0):
#                 pixdata[x, y] = (0, 0, 0, 255)
#
#     width, height = image.size
#     print("resized image {id}. new size is: ".format(id=index), image.size)
#     image.save(image_save_path_txt_black + "{id}.png".format(id=index))
#     index += 1
