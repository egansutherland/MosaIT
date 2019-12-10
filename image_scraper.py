from google_images_download import google_images_download as gid
from PIL import Image
import os
import math

#assumes not bigger than 640*480
def search(keyword, limit=100, width=100, height=100, searchSize=">400*300"):

	response = gid.googleimagesdownload()
	arguments = {"keywords":keyword,"limit":limit,"print_urls":True,"size":searchSize,"output_directory":"Output"}
	paths = response.download(arguments)
	print(paths)

	#cwd = os.getcwd()
	imgDir = "Output/" + keyword + "/"
	for file in os.listdir(imgDir):
		im = Image.open(imgDir + file)
		realWidth, realHeight = im.size
		if(realWidth < width or realHeight < height):
			print("not big enough, removing")
			os.remove(imgDir + file)
			continue
		widthScale = realWidth/width
		heightScale = realHeight/height
		scale = min(widthScale,heightScale)
		if (scale > 1):
			realWidth = math.floor(realWidth/scale)
			realHeight = math.floor(realHeight/scale)
			print("resizing to ",realWidth,realHeight)
			im = im.resize((realWidth,realHeight), resample=Image.NEAREST)
		left = (realWidth - width)/2
		right = width + (realWidth - width)/2
		top = (realHeight - height)/2
		bottom = height + (realHeight - height)/2
		im1 = im.crop((left,top,right,bottom))
		im1.save(imgDir + file, format="png")
		print(im1.size)