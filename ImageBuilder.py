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
def BuildImage(X, Y, inputDirectory, outputDirectory='Output/', outputName='image.png'):
	images = []

	for index in os.listdir(inputDirectory):
		#temp = np.array(plt.imread(inputDirectory + index)).astype(np.float)
		images.append(Image.open(inputDirectory + index))

	numIms = len(images)
	width, height = images[0].size
	
	if (X * Y) > numIms:
		print('error')
		return

	total_width = width * X
	total_height = height * Y

	outputImage = Image.new('RGB',(total_width,total_height))

	x_offset = 0
	y_offset = 0
	count = 0

	for i in range(0, Y):
		for j in range(0,X):
			outputImage.paste(images[count],(x_offset,y_offset))
			x_offset += width
			count += 1
		x_offset = 0
		y_offset += height
		
	if not os.path.exists(outputDirectory):
		os.makedirs(outputDirectory)

	outputImage.save(outputDirectory + outputName)