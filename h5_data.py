import gzip, cPickle
from glob import glob
import numpy as np
from PIL import Image
import os
from tqdm import tqdm
import hickle as hkl
import h5py


print("converting image to numpy array rgb format ---- White")
imlist = os.listdir('./resized_txt_white_512/')

imlist = imlist[0:100:1]

pbar = tqdm(total=len(imlist))
ImageDataWhite = []
for img in imlist:
    img = np.array(Image.open('./resized_txt_white_512/'+img).convert('RGB'))
    img = np.rollaxis(img, -1, -3)
    # print(img.shape)
    ImageDataWhite.append(img)
    pbar.update(1)
pbar.close()
ImageDataWhite = np.array(ImageDataWhite)

print("converting image to numpy array rgb format ---- Black")
imlist = os.listdir('./resized_txt_black_512/')

imlist = imlist[0:100:1]

pbar = tqdm(total=len(imlist))
ImageDataBlack = []
for img in imlist:
    img = np.array(Image.open('./resized_txt_black_512/'+img).convert('RGB'))
    img = np.rollaxis(img, -1, -3)
    # print(img.shape)
    ImageDataBlack.append(img)
    pbar.update(1)
pbar.close()
ImageDataBlack = np.array(ImageDataBlack)

dataset = np.array([ImageDataWhite, ImageDataBlack])

with h5py.File('dataset.h5', 'w') as hf:
    hf.create_dataset("dataset",  data=dataset)
    print ("Done :) ")
