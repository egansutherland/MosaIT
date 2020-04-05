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
	startSearchTime = time.perf_counter()
	sources = image_scraper.search(keyword, limit, threads)
	endSearchTime = time.perf_counter()
	print("Search time: " + str(endSearchTime - startSearchTime) + "\n")
	startDownloadTime = time.perf_counter()
	croppedImages = image_scraper.download(downloadsDirectory, sources, width, height, limit, threads)
	endDownloadTime = time.perf_counter()
	print("Download time: " + str(endDownloadTime - startDownloadTime) + "\n")
else:
	croppedImages = image_scraper.cropDirectory(keyword, width, height, databaseDirectory)

#order images accordingly
startMosaicTime = time.perf_counter()
orderedImages = image_ordering.OrderImages(targetImage,croppedImages, colorSim, best, repeat)

#make the filename for the completed mosaic (if not given)
if outputName == None:
	outputName = targetImageFileName + str(x) + "_" + str(y)
	if best:
		outputName += "_b"
	else:
		outputName += "_" + str(colorSim)
	if repeat:
		outputName += "_r"
	outputName += ".png"

#build mosaic out of ordered images
image_builder.BuildImage(x, y, orderedImages, outputDirectory=outputPath, outputName=outputName)
endMosaicTime = time.perf_counter()
print("Mosaic Build Time: " + str(endMosaicTime - startMosaicTime)+"\n")

#print total timer
endTotalTime = time.perf_counter()
print("Total Time: " + str(endTotalTime - startTotalTime))

if view:
	im = IMAGE.open(outputPath+"/"+outputName)
	im.show()