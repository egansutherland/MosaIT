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
def BuildImage(x, y, inputImages, colorSim, outputDirectory='Output/', outputName='image'):
	images = []

	# for index in os.listdir(inputDirectory):
	# 	#temp = np.array(plt.imread(inputDirectory + index)).astype(np.float)
	# 	images.append(Image.open(inputDirectory + index))

	numIms = len(inputImages)
	# height = inputImages[0].image.shape[0]
	# width = inputImages[0].image.shape[1]
	
	if (x * y) > numIms:
		print('Error: not enough images, needed ' + str(x*y) + " but got " + str(numIms))
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

	mosaicName = outputDirectory + outputName + str(x) + "_" + str(y) + "_" + str(colorSim) + ".png"
	cv.imwrite(outputDirectory + outputName + str(x) + "_" + str(y) + "_" + str(colorSim) + ".png", outputImage)
	print("Success,",mosaicName,"created!")