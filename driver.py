#!/usr/bin/python3
import image_scraper
import image_builder
import image_ordering
import TargetImage
import Image

import argparse
import sys
import os
import math
import tempfile
import cv2 as cv
import time
#only used for displaying image with -v option
from PIL import Image as IMAGE

parser = argparse.ArgumentParser(description='Calls MosaIT backend driver with parameters.')

#required arguments
parser.add_argument("keyword", help = "the search term that gathered images correspond to")
parser.add_argument("limit", help = "the number of images to attempt to gather", type = int)
parser.add_argument("x", help = "number of images per row", type = int)
parser.add_argument("y", help = "number of images per column", type = int)

#toggle options
parser.add_argument("-s","--skip", help = "skips the image gathering", action = "store_true")
parser.add_argument("-b","--best", help = "chooses best image, instead of first above threshold", action = "store_true")
parser.add_argument("-r","--repeat", help = "allows repeat of images in mosaic", action = "store_true")
parser.add_argument("-v","--view", help = "views the completed mosaic", action = "store_true")

#options with values
parser.add_argument("-c","--colorSim", help = "sets a color similarity threshold", type = float, default = 0)
parser.add_argument("-i","--input", help = "filepath to target image", default = None)
parser.add_argument("-o","--outputPath", help = "path to output Mosaic", default = "Mosaic/")
parser.add_argument("-n","--outputName", help = "name of output file", default = None)
parser.add_argument("-a", "--databaseDirectory", help = "path to directory of images if -s is used", default = "/root/MosaIT/Downloads/") #"/root/MosaIT"
parser.add_argument("-t", "--threads", help = "number of threads to use for source searching and image downloading", type=int, default=1)
parser.add_argument("-x", "--blend", help = "saves another image consisting of the mosaic superimposed on the target image, blend value between 0 ->just mosaic and 1->just target image", type=float, default=None)

#start timer
startTotalTime = time.perf_counter()

#get all the args
args = parser.parse_args()
keyword = args.keyword
keyword = keyword.replace("_"," ")
limit = args.limit
x = args.x
y = args.y

#get toggle options
skip = args.skip
best = args.best
repeat = args.repeat
view = args.view

#get options with values
colorSim = args.colorSim
targetImageFile = args.input
targetImageFileName = targetImageFile.split("/")[-1].split(".")[0]
outputPath = args.outputPath #output file path
outputName = args.outputName #output file name
databaseDirectory = args.databaseDirectory #the directory of images to use if using skip
threads = args.threads
blend = args.blend

#open targetImage and find height and width
if not "/" in targetImageFile:
	targetImage = TargetImage.TargetImage("/root/MosaIT/Input/"+targetImageFile, x, y)
else:
	sys.stdout.write("TargetImage path: " + targetImageFile + "\n")
	targetImage = TargetImage.TargetImage(targetImageFile, x, y)
if targetImage.image is None:
	exit()
totalHeight = targetImage.image.shape[0]
totalWidth = targetImage.image.shape[1]
print("Dimensions of target image (w,h): ", totalWidth, totalHeight)
height = targetImage.grid[0].image.shape[0]
width = targetImage.grid[0].image.shape[1]
print("Dimensions of grid image (w,h): ", width, height)

#obtain images and put in temp Downloads directory
croppedImages =[]
if not skip:
	downloadsDirectory = tempfile.mkdtemp()
	print("DownloadDir: ", str(downloadsDirectory))
	startSearchTime = time.perf_counter()
	sources = image_scraper.search(keyword, limit, threads)
	endSearchTime = time.perf_counter()
	print("Search time: " + str(endSearchTime - startSearchTime))
	#check for error state
	if sources is None or len(sources) == 0:
		print("Error, no sources obtained\n")
		exit()
	else:
		print("Search time per source: " + str((endSearchTime - startSearchTime)/len(sources)) + "\n")
	startDownloadTime = time.perf_counter()
	croppedImages = image_scraper.download(downloadsDirectory, sources, width, height, limit, threads)
	endDownloadTime = time.perf_counter()
	print("Download time: " + str(endDownloadTime - startDownloadTime))
	#check for error state
	if croppedImages is None or len(croppedImages) == 0:
		print("Error, no downloaded and cropped images obtained\n")
		exit()
	else:
		print("Download time per image: " + str((endDownloadTime - startDownloadTime)/len(croppedImages)) + "\n")
else:
	croppedImages = image_scraper.cropDirectory(keyword, width, height, databaseDirectory)

#order images accordingly
startMosaicTime = time.perf_counter()
numIterations = len(croppedImages)*x*y #for use with timers
orderedImages = image_ordering.OrderImages(targetImage,croppedImages, colorSim, best, repeat)

#build mosaic out of ordered images
mosaicIm = image_builder.BuildImage(x, y, orderedImages)
#check for error state
if mosaicIm is None:
	print("Error, unable to make mosaic")
	exit()

#make the filename for the completed mosaic (if not given)
if outputName == None:
	outputName = targetImageFileName + "_" + keyword + "_" + str(x) + "_" + str(y)
	if best:
		outputName += "_b"
	else:
		outputName += "_" + str(colorSim)
	if repeat:
		outputName += "_r"
	outputName += ".png"

#check and make if necessary the outputPath directory
if not os.path.exists(outputPath):
	os.makedirs(outputPath)

#save the mosaic
mosaicName = outputPath + outputName
cv.imwrite(mosaicName, mosaicIm)
print("Success,", mosaicName, "created!")

#if blend option used, save the mosaic and target image blended together in outputPath directory
if blend is not None:
	blendIm = cv.addWeighted(targetImage.image, blend, mosaicIm, 1-blend, 0.0)
	blendImName = outputPath + "blend_" + str(blend) + "_" + outputName
	cv.imwrite(blendImName, blendIm)
	print("Saved " + blendImName)

endMosaicTime = time.perf_counter()
print("Mosaic Build Time: " + str(endMosaicTime - startMosaicTime))
print("Build time per grid image: " + str((endMosaicTime - startMosaicTime)/(x*y)))
print("Build time per iteration: " + str((endMosaicTime - startMosaicTime)/numIterations) + "\n")

#print total timer
endTotalTime = time.perf_counter()
print("Total Time: " + str(endTotalTime - startTotalTime))

if view:
	im = IMAGE.open(outputPath+outputName)
	im.show()