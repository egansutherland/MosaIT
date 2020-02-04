import numpy as np
import os
import sys
from PIL import Image

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
def BuildImage(X, Y, inputImages, outputDirectory='Output/', outputName='image.png'):
	images = []

	# for index in os.listdir(inputDirectory):
	# 	#temp = np.array(plt.imread(inputDirectory + index)).astype(np.float)
	# 	images.append(Image.open(inputDirectory + index))

	numIms = len(inputImages)
	# height = inputImages[0].image.shape[0]
	# width = inputImages[0].image.shape[1]
	
	if (X * Y) > numIms:
		print('Error: not enough images')
		return

	#total_width = width * X
	#total_height = height * Y

	#outputImage = Image.new('RGB',(total_width,total_height))

	# x_offset = 0
	# y_offset = 0
	# count = 0

	# for i in range(0, Y):
	# 	for j in range(0,X):
	# 		outputImage.paste(inputImages[count].image,(x_offset,y_offset))
	# 		x_offset += width
	# 		count += 1
	# 	x_offset = 0
	# 	y_offset += height
	outputImage = None
	counter = 0
	row = []
	for j in range(0,Y):
		for i in range(0,X):
			row[i] = cv.hconcat((row[i], inputImages[counter].Image))
			counter+=1
	outputImage = cv.vconcat(row)
	del row

	if not os.path.exists(outputDirectory):
		os.makedirs(outputDirectory)

	cv.imwrite(outputDirectory + outputName + ".png", outputImage)