from google_images_download import google_images_download as gid
from PIL import Image
import os
import math

#assumes not bigger than 640*480
def search(keyword, outDir, limit=100, searchSize=">400*300"):

	response = gid.googleimagesdownload()
	cwd = os.getcwd()
	arguments = {"chromedriver":cwd+"/chrome/chromedriver", "keywords":keyword,"limit":limit,"print_urls":True,"size":searchSize,"output_directory":outDir}
	paths = response.download(arguments)
	#print(paths)

	# for path in paths:
	# 	print("THIS IS A PATH\n")
	# 	print(path)

def crop(keyword, width, height, inDir, outDir): #add inDir outDir as args
	# inDir = "Downloads/" + keyword + "/"
	# outDir = "Cropped/" + keyword + "/"
	try:
		os.mkdir(outDir)
	except:
		print(outDir,"exists... removing files")
		for f in os.listdir(outDir):
			os.remove(outDir + f)
	for file in os.listdir(inDir):
		try:
			im = Image.open(inDir + file)
		except:
			#remove files that can't be opened
			os.remove(inDir + file)
			continue

		#skip images that are too small
		realWidth, realHeight = im.size
		if(realWidth < width or realHeight < height):
			#os.remove(inDir + file)
			continue

		#Scaling down images
		widthScale = realWidth/width
		heightScale = realHeight/height
		scale = min(widthScale,heightScale)
		if (scale > 1):
			realWidth = math.floor(realWidth/scale)
			realHeight = math.floor(realHeight/scale)
			im = im.resize((realWidth,realHeight), resample=Image.NEAREST)

		#Crop images
		extraWidthPixel = 0
		if (width % 2 != 0):
			extraWidthPixel = 1
		extraHeightPixel = 0
		if (height % 2 != 0):
			extraHeightPixel = 1
		left = (realWidth - width)/2
		right = width + (realWidth - width)/2 - extraWidthPixel
		top = (realHeight - height)/2
		bottom = height + (realHeight - height)/2 - extraHeightPixel
		im1 = im.crop((left,top,right,bottom))

		#if it can't be saved as a png file, remove it
		try:
			im1.save(outDir + "/" + file, format="png")
		except:
			print("couldnt save")
			#os.remove(inDir + file)
