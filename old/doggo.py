#  CONFIG AN VARS I DONT UNDERSTAND YET



# path = './data/dogsandcats/sample/'

# path = '../test'

from __future__ import division,print_function

import os, json
from glob import glob
import numpy as np
np.set_printoptions(precision=4, linewidth=100)
from matplotlib import pyplot as plt
from scipy import misc, ndimage
from scipy.ndimage.interpolation import zoom

import utils; reload(utils)
from utils import plots

import datetime

from numpy.random import random, permutation
from scipy.ndimage.interpolation import zoom

from keras import backend as K
from keras.layers.normalization import BatchNormalization
from keras.utils.data_utils import get_file
from keras.models import Sequential
from keras.layers.core import Flatten, Dense, Dropout, Lambda
from keras.layers.convolutional import Convolution2D, MaxPooling2D, ZeroPadding2D
from keras.layers.pooling import GlobalAveragePooling2D
from keras.optimizers import SGD, RMSprop, Adam
from keras.preprocessing import image

# In case we are going to use the TensorFlow backend we need to explicitly set the Theano image ordering
K.set_image_dim_ordering('th')


path = './data/dogsandcats/'


FILES_PATH = 'http://files.fast.ai/models/'; CLASS_FILE='imagenet_class_index.json'
# Keras' get_file() is a handy function that downloads files, and caches them for re-use later
fpath = get_file(CLASS_FILE, FILES_PATH+CLASS_FILE, cache_subdir='models')
with open(fpath) as f: class_dict = json.load(f)
# Convert dictionary with string indexes into an array
classes = [class_dict[str(i)][1] for i in range(len(class_dict))]



def ConvBlock(layers, model, filters):
    for i in range(layers): 
        model.add(ZeroPadding2D((1,1)))
        model.add(Convolution2D(filters, 3, 3, activation='relu'))
    model.add(MaxPooling2D((2,2), strides=(2,2)))
    
# Fully connected block
def FCBlock(model):
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    
    
    
    
# Mean of each channel as provided by VGG researchers
vgg_mean = np.array([123.68, 116.779, 103.939]).reshape((3,1,1))



def vgg_preprocess(x):
    x = x - vgg_mean     # subtract mean
    return x[:, ::-1]    # reverse axis bgr->rgb



def VGG_16():
    model = Sequential()
    model.add(Lambda(vgg_preprocess, input_shape=(3,224,224)))

    ConvBlock(2, model, 64)
    ConvBlock(2, model, 128)
    ConvBlock(3, model, 256)
    ConvBlock(3, model, 512)
    ConvBlock(3, model, 512)

    model.add(Flatten())
    FCBlock(model)
    FCBlock(model)
    model.add(Dense(1000, activation='softmax'))
    return model
    
    
model = VGG_16()


trained_model = '2017-11-14-doggo.h5'
# model = 'vgg16.h5'

fpath = get_file('vgg16.h5', FILES_PATH+'vgg16.h5', cache_subdir='models')


model.load_weights(fpath)
batch_size = 4

def get_batches(dirname, gen=image.ImageDataGenerator(), shuffle=True, 
                batch_size=batch_size, class_mode='categorical'):
    return gen.flow_from_directory(path+dirname, target_size=(224,224), 
                class_mode=class_mode, shuffle=shuffle, batch_size=batch_size)



batches = get_batches('train', batch_size=batch_size)
val_batches = get_batches('valid', batch_size=batch_size)


"""
    Modifies the original VGG16 network architecture and updates self.classes for new training data.

"""
"""
    Replace the last layer of the model with a Dense (fully connected) layer of num neurons.
    Will also lock the weights of all layers except the new layer so that we only learn
    weights for the last layer in subsequent training.

"""
model.pop()
for layer in model.layers: layer.trainable=False
model.add(Dense(batches.nb_class, activation='softmax'))
"""
    Configures the model for training.
    See Keras documentation: https://keras.io/models/model/
"""
model.compile(optimizer=Adam(lr=0.001),
        loss='categorical_crossentropy', metrics=['accuracy'])


classes = list(iter(batches.class_indices)) # get a list of all the class labels

# batches.class_indices is a dict with the class name as key and an index as value
# eg. {'cats': 0, 'dogs': 1}

# sort the class labels by index according to batches.class_indices and update model.classes
for c in batches.class_indices:
    classes[batches.class_indices[c]] = c

    
"""
    Fits the model on data yielded batch-by-batch by a Python generator.
    See Keras documentation: https://keras.io/models/model/
"""
#  this is the model being trained batch by batch
model.fit_generator(batches, samples_per_epoch=batches.nb_sample, nb_epoch=1,
        validation_data=val_batches, nb_val_samples=val_batches.nb_sample)

# save weights to file when training is done
model.save_weights('{}-doggo'.format(datetime.datetime.now().strftime("%Y-%m-%d"))+".h5")


