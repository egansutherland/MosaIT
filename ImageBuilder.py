import cv2 as cv
import numpy as np
#import matplotlib.pyplot as plt
import os
import sys

directory = sys.argv[1]
images = []

for index in os.listdir(directory):
	images.append(cv.imread(directory+index))

dims = images[0].shape
print(dims)
cv.imshow('img',images[1])