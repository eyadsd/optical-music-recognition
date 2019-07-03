import cv2 as cv
import numpy as np
from copy import deepcopy
import math
from random import randint
from tensorflow import keras
import matplotlib.pyplot as plt
import random


def turn_that_frown_upside_down(image):
    img = deepcopy(image)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] == 255:
                img[i][j] = 0
            elif img[i][j] == 0:
                img[i][j] = 255
    return img


def resize(image, maxheight, maxwidth):
    height = image.shape[0]
    width = image.shape[1]
    aspectRatio = min(maxheight / height, maxwidth / width)
    return cv.resize(image, (math.floor(width * aspectRatio), math.floor(height * aspectRatio)), interpolation=cv.INTER_NEAREST)

def rotate(image,angle):
    rows, cols = image.shape
    M = cv.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    image = cv.warpAffine(image, M, (cols, rows))
    return image


def extract_features(image, window_height, window_width,inverted):
    images = []
    image = image / 255
    foreground = 0
    if(inverted == 1):
        foreground = 1
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (image[i][j] == foreground and i - window_height  > 0 and j - window_width > 0
                    and i + window_height  < image.shape[0] and j + window_width  < image.shape[1]):
                window = image[i - math.ceil(window_height/2):i + math.floor(window_height/2 ),
                         j - math.ceil(window_width/2):j + math.floor(window_width /2)]
                images.append(window)
                del window
    return images

def extract_labels(image,symbol_image,window_height,window_width,inverted):
    labels = []
    image = image / 255
    symbol_image = symbol_image / 255
    foreground = 0
    if (inverted == 1):
        foreground = 1
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (image[i][j] == foreground and i - window_height > 0 and j - window_width > 0
                    and i + window_height < image.shape[0] and j + window_width < image.shape[1]):
                if symbol_image[i][j] == foreground:
                    label = 1  # staff
                else:
                    label = 0  # symbol

                labels.append(label)
    return labels

def extract_labels_symbols(image,annotated,window_height,window_width):
    labels = []
    classes = {33: 1, 31: 2, 29: 3, 37: 4, 58: 5, 50: 6, 52: 7, 54: 8, 60: 9}
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (image[i][j] == 0 and annotated[i][j] != 0 and i - window_height > 0 and j - window_width > 0
                    and i + window_height < image.shape[0] and j + window_width < image.shape[1]):
                if annotated[i][j] in classes:
                    label = classes[annotated[i][j]]
                else:
                    label = 0
                labels.append(label)
    return labels

def extract_features_segmentation(image,annotated, window_height, window_width,inverted):
    images = []
    image = image / 255
    foreground = 0
    if(inverted == 1):
        foreground = 1
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            if (image[i][j] == foreground and annotated[i][j] != 0 and i - window_height  > 0 and j - window_width > 0
                    and i + window_height < image.shape[0] and j + window_width  < image.shape[1]):
                window = image[i - math.ceil(window_height/2):i + math.floor(window_height/2),
                         j - math.ceil(window_width/2):j + math.floor(window_width/2)]
                #window = resize(window,window_height,window_width)
                images.append(window)
                del window
    return images

