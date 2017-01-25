import gzip, cPickle
from glob import glob
import numpy as np, array
from PIL import Image
import os

def dir_to_dataset(glob_files):
    print("Gonna process:\n\t %s"%glob_files)
    dataset = []
    for file_count, file_name in enumerate( sorted(glob(glob_files),key=len) ):
        image = Image.open(file_name)
        #tograyscale
        # image = Image.open(file_name).convert('LA')
        pixels = [f[0] for f in list(image.getdata())]
        dataset.append(pixels)
        if file_count % 10 == 0:
            print("\t %s files processed"%file_count)

    return np.array(dataset)


imlist = os.listdir('./resized_images_white/')
ImageDataWhite = np.array([np.array(Image.open('./resized_images_white/'+img).convert('RGB')).flatten() for img in imlist], 'f')

imlist = os.listdir('./resized_images_black/')
ImageDataBlack = np.array([np.array(Image.open('./resized_images_black/'+img).convert('RGB')).flatten() for img in imlist], 'f')

# ImageDataWhite = dir_to_dataset("resized_images_white/*.png")
# ImageDataBlack = dir_to_dataset("resized_images_black/*.png")

train_set = ImageDataWhite
test_set = ImageDataBlack

dataset = [train_set, test_set]

print("Pickling dataset now. Sit tight :) ")
f = gzip.open('file.pkl.gz','wb')
cPickle.dump(dataset, f, protocol=2)
f.close()
print("All done :):)")
