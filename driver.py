import image_scraper
import image_builder
import image_analyzer
import image_ordering
import TargetImage
import Image

import argparse
import sys
import os
import math
import cv2 as cv

from PIL import Image as IMAGE

parser = argparse.ArgumentParser(description='Calls MosaIT backend driver with parameters.')

parser.add_argument("keyword", help = "the search term that gathered images correspond to")
parser.add_argument("limit", help = "the number of images to attempt to gather", type = int)
parser.add_argument("x", help = "number of images per row", type = int)
parser.add_argument("y", help = "number of images per column", type = int)
parser.add_argument("-s","--skip", help = "skips the image gathering", action = "store_true")
parser.add_argument("-b","--best", help = "chooses best image, instead of first above threshold", action = "store_true")
parser.add_argument("-r","--repeat", help = "allows repeat of images in mosaic", action = "store_true")
parser.add_argument("-v","--view", help = "views the completed mosaic", action = "store_true")
parser.add_argument("-d","--delete", help = "clears everything in Downloads, Cropped, Grid, Ordered, and Mosaic directories", action = "store_true")
parser.add_argument("-c","--colorSim", help = "sets a color similarity threshold", type = float, default = 0)
parser.add_argument("-i","--input", help = "filename of desired target image in Input directory", default = os.listdir("Input/")[0])


#get all the args
args = parser.parse_args()
keyword = args.keyword
keyword = keyword.replace("_"," ")
limit = args.limit
x = args.x
y = args.y

skip = args.skip
best = args.best
repeat = args.repeat
view = args.view

colorSim = args.colorSim
targetImageFile = args.input
targetImageFileName = targetImageFile.split(".")[0]


if args.delete:
	os.system("sh cleanOutput.sh")

#open targetImage and find height and width
targetImage = TargetImage.TargetImage("Input/"+targetImageFile, x, y)
height = targetImage.grid[0].image.shape[0]
width = targetImage.grid[0].image.shape[1]
print(width,height)
#obtain images and put in Downloads/keyword directory
if not skip:
	downloadTries = 0
	searchSize = ">400*300" #probably remove this
	image_scraper.search(keyword, limit, searchSize)
	while (len(os.listdir("Downloads/"+keyword+"/")) <= 0) and (downloadTries < 100):
		print("false start, attempt number: " + str(downloadTries))
		image_scraper.search(keyword, limit, searchSize)
		downloadTries += 1

#crop downloaded images and put into Cropped/keyword directory
image_scraper.crop(keyword, width, height)

#turn all downloaded images into Image class
downloadImages = []
for download in os.listdir("Cropped/"+keyword+"/"):
	downloadImage = Image.Image("Cropped/"+keyword+"/"+download, None)
	downloadImages.append(downloadImage)

#order images accordingly
orderedImages = image_ordering.OrderImages(targetImage,downloadImages, colorSim, best, repeat)

#save ordered images to directory (for debugging)
orderedDir = "Ordered/" + keyword + "/"
try:
	os.mkdir(orderedDir)
except:
	print(orderedDir,"exists... removing files")
	for f in os.listdir(orderedDir):
		os.remove(orderedDir + f)
for n,ordImg in enumerate(orderedImages):
	cv.imwrite(orderedDir+str(n)+".png",ordImg.image)

#make the filename for the completed mosaic
mosaicFileName = targetImageFileName + str(x) + "_" + str(y)
if best:
	mosaicFileName += "_b"
else:
	mosaicFileName += "_" + str(colorSim)
if repeat:
	mosaicFileName += "_r"
mosaicFileName += ".png"


#build mosaic out of ordered images
image_builder.BuildImage(x, y, orderedImages, outputDirectory="Mosaic/" + keyword + "/", outputName=mosaicFileName)

if view:
	im = IMAGE.open("Mosaic/"+keyword+"/"+mosaicFileName)
	im.show()