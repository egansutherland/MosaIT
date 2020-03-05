import numpy as np
import os
import sys
import cv2 as cv


#combines images in an ordered set into a single image. Goes through
#input directory, placing images from left to right, top to bottom into
#a new image
#
#In current form it does not use opencv for image manipulation due to
#installation problems. Will be fixed
# X: number of images per row
# Y: number of images per column
# inputDirectory: directory containing input images
# outputDirectory: directory to output images to
# outputName: desired name of output image
def BuildImage(x, y, inputImages, outputDirectory='Output/', outputName='image'):
	images = []

	numIms = len(inputImages)
	
	if (x * y) > numIms:
		print('Error: not enough images, needed ' + str(x*y) + " but got " + str(numIms))
		return

	outputImage = None
	counter = 0
	col = []
	for j in range(0,y):
		row = []
		for i in range(0,x):
			row.append(inputImages[counter].image)
			# if i == 0:
			# 	row[i] = inputImages[counter].image
			# else:
			# 	row[i] = cv.hconcat((row[i], inputImages[counter].image))
			counter+=1
		col.append(cv.hconcat(row))

		#print(type(col[0]))
	#cv.imwrite(outputDirectory + outputName + ".png", col[0])
	outputImage = cv.vconcat(col)
	#outputImage = np.vstack(col)

	if not os.path.exists(outputDirectory):
		os.makedirs(outputDirectory)

	mosaicName = outputDirectory + outputName
	cv.imwrite(mosaicName, outputImage)
	print("Success,",mosaicName,"created!")