import numpy as np
import os
import sys
import cv2 as cv


#combines images in an ordered list into a single image. Goes through
#input directory, placing images from left to right, top to bottom into
#a new image. returns the image

# X: number of images per row
# Y: number of images per column
# inputImages: list of image class objects to stitch

def BuildImage(x, y, inputImages):
	#check if enough images
	numIms = len(inputImages)
	if (x * y) > numIms:
		print('Error: not enough images, needed ' + str(x*y) + " but got " + str(numIms))
		return

	#concatenate the images
	outputImage = None
	counter = 0
	col = []
	for j in range(0,y):
		row = []
		for i in range(0,x):
			row.append(inputImages[counter].image)
			counter+=1
		col.append(cv.hconcat(row))
	outputImage = cv.vconcat(col)

	return outputImage