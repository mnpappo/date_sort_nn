import numpy as np
from PIL import Image, ImageOps
import os
import glob
import math
from tqdm import tqdm
from resizeimage import resizeimage
from skimage import color
from skimage import io

doc_dir = './resized_doc_bn_596/'
mask_dir = './resized_mask_bn_596/'

doc_imlist = os.listdir(doc_dir)
# doc_imlist = os.listdir(doc_dir)[0:10:1]
# print(doc_imlist)
mask_imlist = os.listdir(mask_dir)
# mask_imlist = os.listdir(mask_dir)[0:10:1]
# print(mask_imlist)

slide_doc_save_path = './slide_doc/'
slide_mask_save_path = './slide_mask/'

def crop_me_on_slides(image, save_path, slide_height=100, offset=30):
    width, height = image.size
    left, top, right, bottom = 0, 0, 0, 0
    right = left + width

    init_index = len(os.listdir(save_path))

    for index in range(height/slide_height):
        bottom = bottom + slide_height
        # crop (top, left, right, bottom)
        cropped = image.crop((left, top, right, bottom))
        # reduce offset
        top = top + slide_height - offset
        bottom = bottom - offset

        cropped.save(save_path + '{0}.png'.format(init_index))
        init_index += 1


pbar = tqdm(total=len(doc_imlist))
for image_name in doc_imlist:
    image = Image.open(doc_dir + image_name)
    crop_me_on_slides(image, slide_doc_save_path, slide_height=92, offset=30)
    pbar.update(1)
pbar.close()

pbar = tqdm(total=len(mask_imlist))
for image_name in mask_imlist:
    image = Image.open(mask_dir + image_name)
    crop_me_on_slides(image, slide_mask_save_path, slide_height=92, offset=30)
    pbar.update(1)
pbar.close()
