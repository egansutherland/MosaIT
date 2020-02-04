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
			colorSim = target.grid[i].colorSimilarity(inputImages[j])
			if colorSim > 0.7:
				outputImages += inputImages[j]
				del inputImages[j]
				break

	return outputImages