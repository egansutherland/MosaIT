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
	for gridIm in target.grid:
		if len(outputImages)%100 == 0 and len(outputImages) != 0:
			print("Selected " + str(len(outputImages)) + " out of " + str(len(target.grid)))
		colorSimBest = 0
		imBest = None
		for downloadIm in inputImages:
			colorSim = gridIm.colorSimilarity(downloadIm)
			if not best:
				if colorSim > colorSimIn:
					outputImages.append(downloadIm)
					if not repeat:
						inputImages.remove(downloadIm)
					break
			else:
				if colorSim > colorSimBest:
					colorSimBest = colorSim
					imBest = downloadIm
		if best:
			outputImages.append(imBest)
			if not repeat:
				try:
					inputImages.remove(imBest)
				except:
					print('Failed to remove', end = ' ')
					try:
						print(imBest.filepath)
					except:
						pass
	return outputImages