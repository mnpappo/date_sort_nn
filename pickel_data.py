import gzip, cPickle
from glob import glob
import numpy as np
from PIL import Image
import os
from tqdm import tqdm
import hickle as hkl
import h5py


print("converting image to numpy array rgb format ---- White")
imlist = os.listdir('./resized_images_white_x/')

# imlist = imlist[0:20:1]

pbar = tqdm(total=len(imlist))
ImageDataWhite = []
for img in imlist:
    img = np.array(Image.open('./resized_images_white_x/'+img).convert('RGB'))
    img = np.rollaxis(img, -1, -3)
    # print(img.shape)
    ImageDataWhite.append(img)
    pbar.update(1)
pbar.close()
ImageDataWhite = np.array(ImageDataWhite)

print("converting image to numpy array rgb format ---- Black")
imlist = os.listdir('./resized_images_black_x/')

# imlist = imlist[0:20:1]

pbar = tqdm(total=len(imlist))
ImageDataBlack = []
for img in imlist:
    img = np.array(Image.open('./resized_images_black_x/'+img).convert('RGB'))
    img = np.rollaxis(img, -1, -3)
    # print(img.shape)
    ImageDataBlack.append(img)
    pbar.update(1)
pbar.close()
ImageDataBlack = np.array(ImageDataBlack)

dataset = np.array([ImageDataWhite, ImageDataBlack])

with h5py.File('dataset.h5', 'w') as hf:
    hf.create_dataset("dataset",  data=dataset)

# print("Pickling dataset now. Sit tight :) ")
#
#
# try:
#     f = gzip.open('dataset.pkl.gz','wb')
#     cPickle.dump(dataset, f)
#     f.close()
# except Exception as e:
#     raise
#
# print("All done :):)")
