import numpy as np
import cv2 as cv
import Image
import TargetImage
import pymp

#takes in a target image, a list of downloaded images, and a color similarity threshold colorSimIn, and booleans best and repeat. It returns an ordered list of images from inputImages to use in mosaic.
def OrderImages(target, inputImages, colorSimIn, best=False, repeat=False, threads=1):
	outputImages = []
	#check if not enough inputImages
	if len(inputImages) < len(target.grid):
		return outputImages
	#check if can use threaded version
	if best and repeat and threads > 1:
		#try:
		return threadedOrderImages(target, inputImages, threads)
		#except:
			#print("Problem using threaded ordering")
	else:
		print("Using non-threaded ordering")
	#iterate through grid images
	for gridIm in target.grid:
		if len(outputImages)%100 == 0 and len(outputImages) != 0:
			print("Selected " + str(len(outputImages)) + " out of " + str(len(target.grid)))
		colorSimBest = 0
		imBest = None
		#iterate through downloaded images, selecting either best image for grid image or first above threshold colorSim. Delete image from list if repeat is not enabled.
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

#the threaded version of the above function, if best and repeat are enabled. Spawns as many threads as passed in.
def threadedOrderImages(target, inputImages, threads):
	print("Using threaded ordering")
	numGridImages = len(target.grid)
	#parallel variable
	sharedInputImages = pymp.shared.list(inputImages)
	outputImages = pymp.shared.list([None]*numGridImages)
	with pymp.Parallel(threads) as p:
		for gridIdx in p.range(0, numGridImages):
			gridIm = target.grid[gridIdx]
			imBest = None
			colorSimBest = 0
			for downloadIm in sharedInputImages:
				colorSim = gridIm.colorSimilarity(downloadIm)
				if colorSim > colorSimBest:
					colorSimBest = colorSim
					imBest = downloadIm
			outputImages[gridIdx]=imBest
	return outputImages

