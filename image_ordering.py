import numpy as np
import cv2 as cv
import Image
import TargetImage
import pymp

# analyses target image and input images. Orders
# input images by changing names based on where
# it matches target image best.
# target is of type TargetImage
# inputImages is an array of type Image
def OrderImages(target, inputImages, colorSimIn, best=False, repeat=False, threads=1):
	if best and repeat and threads > 1:
		return threadedOrderImages(target, inputImages, threads)
	else:
		print("Using non-threaded ordering")
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

def threadedOrderImages(target, inputImages, threads):
	print("Using threaded ordering")
	numGridImages = len(target.grid)
	outputImages = pymp.shared.list([None]*numGridImages)
	with pymp.Parallel(threads) as p:
		for gridIdx in p.range(0, numGridImages):
			gridIm = target.grid[gridIdx]
			imBest = None
			colorSimBest = 0
			for downloadIm in inputImages:
				colorSim = gridIm.colorSimilarity(downloadIm)
				if colorSim > colorSimBest:
					colorSimBest = colorSim
					imBest = downloadIm
			outputImages[gridIdx]=imBest
	return outputImages

