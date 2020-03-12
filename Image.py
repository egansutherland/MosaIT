import cv2 as cv
import numpy

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
		cmpMethod = 0
		try:
			rSim = cv.compareHist( self.r_hist, other.r_hist, method=cmpMethod)
			gSim = cv.compareHist( self.g_hist, other.g_hist, method=cmpMethod)
			bSim = cv.compareHist( self.b_hist, other.b_hist, method=cmpMethod)

			sim = (rSim + gSim + bSim)/3
		except:
			return 0

		return sim