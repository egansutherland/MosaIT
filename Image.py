import cv2 as cv
import numpy
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
		rSim = cv.compareHist( self.r_hist, other.r_hist, method=cv.HISTCMP_CORREL)
		gSim = cv.compareHist( self.g_hist, other.g_hist, method=cv.HISTCMP_CORREL)
		bSim = cv.compareHist( self.b_hist, other.b_hist, method=cv.HISTCMP_CORREL)

		sim = (rSim + gSim + bSim)/3

		return sim

	def crop(self, width, height): #NEEEEEEEEDS WORK
		#self.image = self.image #TODO
		#realWidth, realHeight = self.image.shape
		realHeight = self.image.shape[0]
		realWidth = self.image.shape[1]
		if(realWidth < width or realHeight < height):
			return None

		#Scaling down images
		widthScale = realWidth/width
		heightScale = realHeight/height
		scale = min(widthScale,heightScale)
		if (scale > 1):
			realWidth = math.floor(realWidth/scale)
			realHeight = math.floor(realHeight/scale)
			im = self.image.resize((realWidth,realHeight))

		cv.imshow("cropped", im)
		cv.waitKey(0)
		#Crop images
		extraWidthPixel = 0
		if (width % 2 != 0):
			extraWidthPixel = 1
		extraHeightPixel = 0
		if (height % 2 != 0):
			extraHeightPixel = 1
		left = (realWidth - width)/2
		right = width + (realWidth - width)/2 - extraWidthPixel
		top = (realHeight - height)/2
		bottom = height + (realHeight - height)/2 - extraHeightPixel
		try:
			im1 = im.crop((left,top,right,bottom))
			im1.save(outDir + file, format="png")
			self.image = im1
			return self
		except:
			print("coulndt save")
			return None


		#if it can't be saved as a png file, remove it
		#try:
		#	im1.save(outDir + file, format="png")
		#	self.image = im1
		#	return self.image
		#except:
		#	print("couldnt save")
		#	return None