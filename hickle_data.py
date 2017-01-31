import gzip, cPickle
from glob import glob
import numpy as np
from PIL import Image
import os
from tqdm import tqdm
import hickle as hkl


print("converting image to numpy array rgb format ---- White")
imlist = os.listdir('./resized_images_white_n/')

pbar = tqdm(total=len(imlist))
ImageDataWhite = []
for img in imlist:
    img = np.array(Image.open('./resized_images_white_n/'+img).convert('RGB'))
    # from scipy.misc import toimage
    # toimage(img).show()
    ImageDataWhite.append(img)
    pbar.update(1)
pbar.close()
ImageDataWhite = np.array(ImageDataWhite)

print("converting image to numpy array rgb format ---- Black")
imlist = os.listdir('./resized_images_black_n/')

pbar = tqdm(total=len(imlist))
ImageDataBlack = []
for img in imlist:
    img = np.array(Image.open('./resized_images_black_n/'+img).convert('RGB'))
    ImageDataBlack.append(img)
    pbar.update(1)
pbar.close()
ImageDataBlack = np.array(ImageDataBlack)

dataset = np.array([ImageDataWhite, ImageDataBlack])

print("Pickling dataset now. Sit tight :) ")


try:
    # f = gzip.open( direcory + 'dataset.pkl.gz','wb')
    # cPickle.dump(dataset, f, protocol=2)
    # f.close()
    # Dump data, with compression
    hkl.dump(dataset, 'dataset.hkl', mode='w', compression='gzip')
except Exception as e:
    print (e)
    raise

# with open('dataset.pickle', 'wb') as f:
#     cPickle.dump(dataset, f, protocol=4)

print("All done :):)")
