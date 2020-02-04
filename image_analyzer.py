import os
import cv2 as cv

def gridify(x, y, im):
	#im = cv.imread("Input/"+filepath, cv.IMREAD_COLOR)
	height = im.shape[0]
	y_rem = height%y
	print("Y: ",y_rem)
	width = im.shape[1]
	x_rem = width%x
	print("X: ",x_rem)
	crop_im=im[0:height-y_rem,0:width-x_rem]
	cv.imwrite("Input/"+filepath,crop_im)

	y_ticks = int(crop_im.shape[0]/y)
	print(y_ticks)
	x_ticks = int(crop_im.shape[1]/x)
	print(x_ticks)
	for i in range(y):
		for j in range(x):
			grid_im = im[i*y_ticks:(i+1)*y_ticks,j*x_ticks:(j+1)*x_ticks]
			cv.imwrite("Grid/"+str(i)+"_"+str(j)+".png",grid_im)



