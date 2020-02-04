import os
import cv2 as cv
import Image

def gridify(x, y, im, filepath):
	#im = cv.imread("Input/"+filepath, cv.IMREAD_COLOR)
	height = im.shape[0]
	y_rem = height%y
	print("Y: ",y_rem)
	width = im.shape[1]
	x_rem = width%x
	print("X: ",x_rem)
	crop_im=im[0:height-y_rem,0:width-x_rem]
	cv.imwrite(filepath,crop_im)

	y_ticks = int(crop_im.shape[0]/y)
	print(y_ticks)
	x_ticks = int(crop_im.shape[1]/x)
	print(x_ticks)
	grids = []
	for i in range(y):
		for j in range(x):
			grid_im = im[i*y_ticks:(i+1)*y_ticks,j*x_ticks:(j+1)*x_ticks]
			filepath = "Grid/" + str(i) + "_" + str(j) + ".png"
			cv.imwrite(filepath,grid_im)
			grids.append(Image.Image(filepath, None))
	return grids



