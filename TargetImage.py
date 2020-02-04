import cv2 as cv
import Image
import image_analyzer

class TargetImage:
	def __init__(self, filepath, x, y):
		self.filepath = filepath
		self.image = cv.imread(filepath, cv.IMREAD_COLOR)
		self.x = x
		self.y = y
		self.grid = image_analyzer.gridify(self.x, self.y, self.image, self.filepath)
		




