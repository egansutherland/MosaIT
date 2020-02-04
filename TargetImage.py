import cv2 as cv
import Image
import image_analyzer

class TargetImage:
	def __init__(self, filepath, x, y):
		self.image = cv.imread(filepath, cv.IMREAD_COLOR)
		self.x = x
		self.y = y
		self.grid = image_analyzer.gridify(x, y, target)
		




