from google_images_download import google_images_download as gid
from PIL import Image
import os
import math

#assumes not bigger than 640*480
def search(keyword, limit=100, width=100, height=100, searchSize=">400*300"):

	response = gid.googleimagesdownload()
	cwd = os.getcwd()
	arguments = {"chromedriver":cwd+"/chrome/chromedriver", "keywords":keyword,"limit":limit,"print_urls":True,"size":searchSize,"output_directory":"Output"}
	paths = response.download(arguments)
	#print(paths)

	for path in paths:
		print("THIS IS A PATH\n")
		print(path)

	imgDir = "Output/" + keyword + "/"
	for file in os.listdir(imgDir):
		try:
			im = Image.open(imgDir + file)
		except:
			os.remove(imgDir + file)
			continue

		#remove images that are too small
		realWidth, realHeight = im.size
		if(realWidth < width or realHeight < height):
			os.remove(imgDir + file)
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
		left = (realWidth - width)/2
		right = width + (realWidth - width)/2
		top = (realHeight - height)/2
		bottom = height + (realHeight - height)/2
		im1 = im.crop((left,top,right,bottom))

		#if it can't be saved as a png file, remove it
		try:
			print(file+"\n")
			im1.save(imgDir + file, format="png")
		except:
			os.remove(imgDir + file)
