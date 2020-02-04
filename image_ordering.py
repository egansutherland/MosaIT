import numpy as np
import cv2 as cv
import Image
import TargetImage

# analyses target image and input images. Orders
# input images by changing names based on where
# it matches target image best.
# target is of type TargetImage
# inputImages is an array of type Image
def OrderImages(target, inputImages):

	outputImages = []
	for i in target.grid:
		for j in inputImages:
			colorSim = i.colorSimilarity(j)
			if colorSim > 0.1:
				outputImages.append(j)
				del j
				break

	return outputImages