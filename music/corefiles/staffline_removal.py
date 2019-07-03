from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import math
from music.corefiles.preprocess import *
from copy import deepcopy

from website.settings import GRAPH, model



class Symbol:
    def __init__(self,position, label):
        self.position = position
        self.label = label
        self.position_in_stave = 0



class Stave:
    def __init__(self):
        self.y_start = 0
        self.y_end = 0
        self.staff_positions = []
        self.space_positions = []
        self.staff_thicknesses = []
        self.space_thicknesses = []
        self.components = []
        self.symbols = []


    def get_components(self, components):
        for component in components:
            for pixel in component.pixels:
                if pixel[0] <= self.y_end and pixel[0] >= self.y_start:
                    self.components.append(component)
                    break

    def calculate_symbol_positions(self):
        for symbol in self.symbols:
            count = 1
            for i in range(len(self.staff_positions)):
                if symbol.position[0] >= self.staff_positions[i] - 2 and symbol.position[0] <= self.staff_positions[i] + self.staff_thicknesses[i] + 1:
                    symbol.position_in_stave = 11 - count
                elif symbol.position[0] > self.space_positions[i] and symbol.position[0] < self.space_positions[i] + self.space_thicknesses[i]:
                    symbol.position_in_stave = 11 - (count + 1)
                count += 2
    def sort_symbols(self):
        self.symbols.sort(key=lambda symbol:symbol.position[1])

#model = keras.models.load_model('C:\\Users\\TechnoCity\\Desktop\\website\\media\\test2.h5')

def remove_staffline(image):

    staff_image = np.ones((image.shape[0], image.shape[1]))
    staff_image = staff_image * 255
    window_height = 15
    window_width = 15
    # image = turn_that_frown_upside_down(image)
    image = image / 255

    windows = []
    pixels = []
    print("image processing time")
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # print(image[i][j])
            if (image[i][j] == 0 and i - window_height > 0 and j - window_width > 0
                    and i + window_height < image.shape[0] and j + window_width < image.shape[1]):
                window = np.zeros((window_height, window_width))
                label = ""

                window = image[i - math.ceil(window_height / 2):math.floor(i + window_height / 2),
                         j - math.ceil(window_width / 2):j + math.floor(window_width / 2)]
                windows.append(window)
                pixel = (i, j)
                pixels.append(pixel)
    windows = np.asarray(windows)
    print("prediction time")

    with GRAPH.as_default():
        print(windows.shape)
        predictions = model.predict(windows)

    # for prediction in predictions:
    #     print(np.argmax(prediction))
    image = image * 255
    for i in range(len(predictions)):
        j, k = pixels[i]
        if not (np.argmax(predictions[i]) == 1):
            image[j][k] = 255
            staff_image[j][k] = 0
    return image, staff_image

def get_staves(staff_image):
    staffs = np.zeros(staff_image.shape[0])
    print(staffs.shape)
    for i in range(staff_image.shape[0]):
        count = 0
        for j in range(staff_image.shape[1]):
            if staff_image[i][j] == 0:
                count = count + 1
        if count > staff_image.shape[1]/2:
            staffs[i] = 1
    i = 0
    staves = []
    while(i<staffs.shape[0]):
        if(staffs[i] == 1):
            stave = Stave()
            stave.y_start = i
            count = 0
            while(count < 5):
                stave.staff_positions.append(i)
                thickness = 0
                while(i<staffs.shape[0] and staffs[i] == 1 ):
                    i = i + 1
                    thickness = thickness + 1
                stave.staff_thicknesses.append(thickness)
                if count<4:
                    stave.space_positions.append(i)
                    thickness = 0
                    while(i<staffs.shape[0] and staffs[i] == 0 ):
                        i = i + 1
                        thickness = thickness + 1
                    stave.space_thicknesses.append(thickness)
                else:
                    stave.space_positions.append(i)
                    stave.space_thicknesses.append(stave.space_thicknesses[count-1])
                count = count + 1

            stave.y_end = i -1
            staves.append(stave)
        else:
            i = i + 1
    return staves



