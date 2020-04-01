# from google_images_download import google_images_download as gid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from collections import OrderedDict
from PIL import Image
import pymp
import get_related as gr
import numpy as np
import os
import math

global sources
global numSources
global parallelIndex

#assumes not bigger than 640*480
def search(keyword, outDir, limit=100, searchSize=">400*300"):
	####### Old code based on google_images_download #########
	# response = gid.googleimagesdownload()
	# cwd = os.getcwd()
	# arguments = {"chromedriver":cwd+"/chrome/chromedriver", "keywords":keyword,"limit":limit,"print_urls":True,"size":searchSize,"output_directory":outDir}
	# paths = response.download(arguments)
	# #print(paths)

	# # for path in paths:
	# # 	print("THIS IS A PATH\n")
	# # 	print(path)

	baseurl = "http://www.bing.com/images/search?q=" + keyword
	options = Options()
	options.headless = True
	driver = webdriver.Chrome("/usr/local/bin/chromedriver",chrome_options=options)
	
	driver.get(baseurl)

	# get related terms
	terms = []
	terms.append(keyword)
	terms += gr.getTerms(driver)
	numTerms = len(terms)

	# for ind in range(0,numTerms):
	# 	parallelTerms[ind] = terms[ind]

	print('numTerms: ' + str(len(terms)))
	sources = []
	numSources = 0
	parallelIndex = -1
	i = 0

	# while (len(sources) < 2*limit) and (i < len(terms)):
	# 	sources += gr.getSrc(terms[i])
	# 	i += 1
	# 	#print('numSources: ' + str(len(sources)))

	# numSources = pymp.shared.array((1,), dtype='uint8')
	linkLimit = 2*limit
	tempIndex = 0
	#parallel version
	with pymp.Parallel(4) as p:
		for index in p.xrange(0,numTerms):
			if numSources < linkLimit:
				# tempIndex = 0
				# with p.lock:
				# 	parallelIndex += 1
				# 	tempIndex = parallelIndex
				tempSources = gr.getSrc(terms[index])
				with p.lock:
					sources += tempSources
					numSources = len(sources)
					print('term: ' + str(index) + '    numSources: ' + str(numSources))

	print('numSources with dupes: ' + str(len(sources)))				
	sources = list(OrderedDict.fromkeys(sources))
	#print(sources)
	print('numSources no dupes: ' + str(len(sources)))



	#python requests for download

def crop(keyword, width, height, inDir, outDir): #add inDir outDir as args
	# inDir = "Downloads/" + keyword + "/"
	# outDir = "Cropped/" + keyword + "/"
	print(outDir)
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
			print("inDir: ", inDir, "    file: ", file)
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
