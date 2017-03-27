import gzip, cPickle
from glob import glob
import numpy as np
from PIL import Image
import os
from tqdm import tqdm
import hickle as hkl
import h5py
import scipy.misc
from PIL import Image


print("converting image to numpy array rgb format ---- White")
imlist = os.listdir('./gen_doc_gray/')

imlist = imlist[0:100:1]

pbar = tqdm(total=len(imlist))
ImageDataWhite = []
for img in imlist:
    img = np.array(Image.open('./gen_doc_gray/'+img).convert('L'))
    # img = img[0:92:1,]
    # print(img.shape)
    # img = img.reshape((1,512,512))
    # img = np.rollaxis(img, 0, 3)

    # img_arr = img
    # print(img_arr.shape)
    # img = Image.fromarray(img_arr, 'L')
    # img.save('test.png')
    # img = scipy.misc.toimage(img_arr, channel_axis=0)
    # img.show()

    # print(img.shape)
    ImageDataWhite.append(img)
    pbar.update(1)
pbar.close()
ImageDataWhite = np.array(ImageDataWhite)

print("converting image to numpy array rgb format ---- Black")
imlist = os.listdir('./gen_mask_gray/')

imlist = imlist[0:100:1]

pbar = tqdm(total=len(imlist))
ImageDataBlack = []
for img in imlist:
    img = np.array(Image.open('./gen_mask_gray/'+img).convert('L'))
    # img = img[0:92:1,]
    # img = img.reshape((1,512,512))
    # img = np.rollaxis(img, -1, -3)
    # print(img.shape)
    ImageDataBlack.append(img)
    pbar.update(1)
pbar.close()
ImageDataBlack = np.array(ImageDataBlack)

dataset = np.array([ImageDataWhite, ImageDataBlack])

with h5py.File('dataset_gray.h5', 'w') as hf:
    hf.create_dataset("dataset",  data=dataset)
    print ("Done :) ")
