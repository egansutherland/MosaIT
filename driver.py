import image_scraper
import image_builder
import image_analyzer
import image_ordering
import TargetImage
import Image
import sys
import os
import math
import cv2 as cv
# from PIL import Image

# keyword limit widthpx heightpx X Y
# dft =	100 100 100 5 5

# options are >400*300, >640*480, >800*600, >1024*768
searchSize = ">400*300"

if len(sys.argv) < 2:
	print("Error: no keyword entered")
	exit()
keyword = sys.argv[1]
keyword = keyword.replace("_"," ")
limit = 100
if len(sys.argv) > 2:
	limit = sys.argv[2]
width = 100
height = 100
if len(sys.argv) > 4:
	width = int(sys.argv[3])
	height = int(sys.argv[4])

x = 5
y = 5
if len(sys.argv) > 6:
	x = int(sys.argv[5])
	y = int(sys.argv[6])



targetImagePath = os.listdir("Input/")[0]
#image_analyzer.gridify(X,Y,targetImagePath)

targetImage = TargetImage.TargetImage("Input/"+targetImagePath, x, y)
height = targetImage.grid[0].image.shape[0]
width = targetImage.grid[0].image.shape[1]
downloadTries = 0

image_scraper.search(keyword,limit, width, height, searchSize)
while (len(os.listdir("Output/"+keyword+"/")) <= 0) and (downloadTries < 100):
	print("false start, attempt number: " + str(downloadTries))
	image_scraper.search(keyword,limit, width, height, searchSize)
	downloadTries += 1

downloadImages = []
for download in os.listdir("Output/"+keyword+"/"):
	downloadImage = Image.Image("Output/"+keyword+"/"+download, None)
	downloadImages.append(downloadImage)

orderedImages = image_ordering.OrderImages(targetImage,downloadImages)

for n,ordImg in enumerate(orderedImages):
	cv.imwrite("Ordered/"+str(n)+".png",ordImg.image)

image_builder.BuildImage(x,y, orderedImages, outputDirectory="Mosaic/" + keyword + "/")

# im = Image.open("Mosaic/" + keyword + "/image.png")
# im.show()