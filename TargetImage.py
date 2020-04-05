import cv2 as cv
import Image
import sys
import tempfile
import os

class TargetImage:
	def __init__(self, filepath, x, y):
		self.filepath = filepath
		#sys.stdout.write(self.filepath)
		self.image = cv.imread(filepath, cv.IMREAD_COLOR)
		if self.image is None:
			print ("Couldn't open TargetImage at " + filepath)
		self.x = x
		self.y = y
		self.grid = TargetImage.gridify(self)

	def gridify(self):
		if self.image is None:
			return None
		#filename = filepath.split("/")[1]
		#sys.stdout.write("filename: " + filename)
		gridDir = tempfile.mkdtemp()

		#slightly crop target image so divisible by x and y
		#sys.stdout.write(filepath)
		height = self.image.shape[0]
		y_rem = height%self.y
		width = self.image.shape[1]
		x_rem = width%self.x
		self.image=self.image[0:height-y_rem,0:width-x_rem]
		#cv.imwrite(filepath,crop_im)
		y_ticks = int(self.image.shape[0]/self.y)
		x_ticks = int(self.image.shape[1]/self.x)

		#break into grid of x and y
		grids = []
		for i in range(self.y):
			for j in range(self.x):
				grid_im = self.image[i*y_ticks:(i+1)*y_ticks,j*x_ticks:(j+1)*x_ticks]
				outpath = gridDir + str(i) + "_" + str(j) + ".png"
				cv.imwrite(outpath,grid_im)
				grids.append(Image.Image(outpath, None))
		return grids

		
