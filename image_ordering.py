import numpy as np
import cv2 as cv
import Image
import TargetImage

# analyses target image and input images. Orders
# input images by changing names based on where
# it matches target image best.
# target is of type TargetImage
# inputImages is an array of type Image
def OrderImages(target, inputImages, colorSimIn, best=False, repeat=False):

	outputImages = []
	for i in target.grid:
		colorSimBest = 0
		imBest = None
		for j in inputImages:
			colorSim = i.colorSimilarity(j)
			if not best:
				if colorSim > colorSimIn:
					outputImages.append(j)
					if not repeat:
						inputImages.remove(j)
					break
			else:
				if colorSim > colorSimBest:
					colorSimBest = colorSim
					imBest = j
		if best:
			outputImages.append(imBest)
			if not repeat:
				inputImages.remove(imBest)
	return outputImages