import numpy as np
import os
import sys
import cv2 as cv


#combines images in an ordered list into a single image. Goes through
#input directory, placing images from left to right, top to bottom into
#a new image

# X: number of images per row
# Y: number of images per column
# inputImages: list of image class objects to stitch
# outputDirectory: directory to output images to
# outputName: desired name of output image

def BuildImage(x, y, inputImages, outputDirectory='Output/', outputName='image'):
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

	#check and make if necessary the outputDirectory
	if not os.path.exists(outputDirectory):
		os.makedirs(outputDirectory)

	#save the mosaic
	mosaicName = outputDirectory + outputName
	cv.imwrite(mosaicName, outputImage)
	print("Success,",mosaicName,"created!")