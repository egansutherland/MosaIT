import cv2 as cv
import numpy
import math

class Image:
	def __init__(self, filepath, source, image=None):
		self.filepath = filepath # filepath to image
		if image is None:
			self.image = cv.imread(filepath, cv.IMREAD_COLOR) # opened image
		else:
			self.image = image
		self.source = source # source on web of image
		self.split = cv.split(self.image)
		self.r_hist = cv.calcHist(self.split, [2], None, [256], (0,256)) # histogram of red channel
		self.g_hist = cv.calcHist(self.split, [1], None, [256], (0,256)) # histogram of green channel
		self.b_hist = cv.calcHist(self.split, [0], None, [256], (0,256)) # histogram of blue channel

	# Compares other histograms to self histograms
	# and returns a value between 0 and 1 representing a
	# similarity rating
	# self and other must be of type Image
	def colorSimilarity(self, other):
		cmpMethod = 0
		rSim = cv.compareHist( self.r_hist, other.r_hist, method=cmpMethod)
		gSim = cv.compareHist( self.g_hist, other.g_hist, method=cmpMethod)
		bSim = cv.compareHist( self.b_hist, other.b_hist, method=cmpMethod)

		sim = (rSim + gSim + bSim)/3

		return sim

	def crop(self, width, height):
		#get actual height and width of image
		realHeight = self.image.shape[0]
		realWidth = self.image.shape[1]
		if realWidth == width and realHeight == height:
			return
		#scale down image
		widthScale = width/realWidth
		heightScale = height/realHeight
		scale = max(widthScale,heightScale)
		im = self.image
		if (scale < 0.9):
			im = cv.resize(self.image, (0,0), fx=scale, fy=scale)
			realHeight = im.shape[0]
			realWidth = im.shape[1]

		#crop image to desired dimensions
		left = math.floor((realWidth - width)/2)
		right = math.floor(width + (realWidth - width)/2)
		top = math.floor((realHeight - height)/2)
		bottom = math.floor(height + (realHeight - height)/2)
		self.image=im[top:bottom,left:right]
