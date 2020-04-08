import cv2 as cv
import numpy as np
import math

class Image: # If split is needed, uncomment cv.split line
	def __init__(self, filepath, source):
		self.filepath = filepath # filepath to image
		self.image = cv.imread(filepath, cv.IMREAD_COLOR) # opened image
		self.source = source # source on web of image
		self.split = cv.split(self.image)
		self.r_hist = cv.calcHist(self.image, [2], None, [256], (0,256)) # histogram of red channel
		self.g_hist = cv.calcHist(self.image, [1], None, [256], (0,256)) # histogram of green channel
		self.b_hist = cv.calcHist(self.split, [0], None, [256], (0,256)) # histogram of blue channel

	# Compares other histograms to self histograms
	# and returns a value between 0 and 1 representing a
	# similarity rating
	# self and other must be of type Image
	def colorSimilarity(self, other):
		# cmpMethod = 0
		# rSim = cv.compareHist( self.r_hist, other.r_hist, method=cmpMethod)
		# gSim = cv.compareHist( self.g_hist, other.g_hist, method=cmpMethod)
		# bSim = cv.compareHist( self.b_hist, other.b_hist, method=cmpMethod)

		# colorSim = (rSim + gSim + bSim)/3

		# comparison using diffs
		diff = np.subtract(self.image, other.image)
		diff = diff.astype('float64')
		diff += abs(np.min(diff))
		#diff /= np.ptp(diff)
		diffMean = np.mean(diff)

		# sim = ((0.95 * diffMean) + (0.05 * colorSim))
		sim = diffMean

		return sim

	def crop(self, width, height):
		#get actual height and width of image
		realHeight = self.image.shape[0]
		realWidth = self.image.shape[1]
		#print("realHeight: ",realHeight,"realWidth",realWidth)
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
		#print("size after resize",self.image.shape)