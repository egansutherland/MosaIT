import image_scraper
import image_builder
import sys
import os
import math
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

X = 5
Y = 5
if len(sys.argv) > 6:
	X = int(sys.argv[5])
	Y = int(sys.argv[6])

justInCase = 0

image_scraper.search(keyword,limit, width, height, searchSize)
while (len(os.listdir("Output/"+keyword+"/")) <= 0) and (justInCase < 100):
	print("false start, attempt number: " + str(justInCase))
	image_scraper.search(keyword,limit, width, height, searchSize)
	justInCase += 1
	
image_builder.BuildImage(X,Y, "Output/"+keyword+"/", outputDirectory="Mosaic/" + keyword + "/")
# im = Image.open("Mosaic/" + keyword + "/image.png")
# im.show()