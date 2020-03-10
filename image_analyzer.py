import os
import cv2 as cv
import Image
import tempfile

def gridify(x, y, im, filepath):
	filename = filepath.split("/")[1]
	gridDir = tempfile.mkdtemp()
	try:
		os.mkdir(gridDir)
	except:
		print(gridDir,"exists... removing files")
		for f in os.listdir(gridDir):
			os.remove(gridDir + f)

	#slightly crop target image so divisible by x and y
	height = im.shape[0]
	y_rem = height%y
	width = im.shape[1]
	x_rem = width%x
	crop_im=im[0:height-y_rem,0:width-x_rem]
	cv.imwrite(filepath,crop_im)
	print(filepath)
	y_ticks = int(crop_im.shape[0]/y)
	x_ticks = int(crop_im.shape[1]/x)

	#break into grid of x and y
	grids = []
	for i in range(y):
		for j in range(x):
			grid_im = im[i*y_ticks:(i+1)*y_ticks,j*x_ticks:(j+1)*x_ticks]
			outpath = gridDir + str(i) + "_" + str(j) + ".png"
			cv.imwrite(outpath,grid_im)
			grids.append(Image.Image(outpath, None))
	return grids