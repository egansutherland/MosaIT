# from google_images_download import google_images_download as gid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from collections import OrderedDict
from PIL import Image as IMAGE
import pymp
import get_related as gr
import numpy as np
import os
import math
import requests
import Image

global sources
global numSources
global parallelIndex

#assumes not bigger than 640*480
def search(keyword, limit=100):
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
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(chrome_options=options)
	
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
	tempIndex =  -1
	#parallel version
	testList = pymp.shared.list()
	counter = pymp.shared.list()
	while len(testList) <= linkLimit:
		tempIndex += 1
		counter.append(tempIndex)
		with pymp.Parallel(1) as p:
			for index in p.xrange(0,4):
				if numSources < linkLimit:
					tempSources = gr.getSrc(terms[index + counter[-1]*4])
					with p.lock:
						testList.extend(tempSources)
						numSources = len(testList)
						print('term: ' + str(index + counter[-1]*4) + '    numSources: ' + str(numSources))

	print('numSources with dupes: ' + str(len(testList)))
	sources = list(OrderedDict.fromkeys(testList))
	#print(sources)
	print('numSources no dupes: ' + str(len(sources)))
	return sources

def download(downloadDir, sources, width, height, limit=100):
	index = 0
	croppedImages = []
	for source in sources:
		if len(croppedImages) >= limit:
			return croppedImages
		try:
			r = requests.get(source)
		except:
			continue
		contentType = r.headers.get('content-type')
		if 'image' in contentType:
			tempType = contentType.split('/')[-1]
			filename = downloadDir + str(index) + '.' + tempType
			open(filename, 'w+b').write(r.content)
			index += 1
			im = Image.Image(filename, source)
			# need to save here
			if im.image.shape[0] >= height and im.image.shape[1] >= width:
				im.crop(width,height)
				croppedImages.append(im)

	return croppedImages

def cropDirectory(keyword, width, height, inDir): #add inDir outDir as args
	# inDir = "Downloads/" + keyword + "/"
	# outDir = "Cropped/" + keyword + "/"
	#print(outDir)
	# try:
	# 	os.mkdir(outDir)
	# except:
	# 	print(outDir,"exists... removing files")
	# 	for f in os.listdir(outDir):
	# 		os.remove(outDir + f)
	for file in os.listdir(inDir):
		try:
			im = IMAGE.open(inDir + file)
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
			im = im.resize((realWidth,realHeight), resample=IMAGE.NEAREST)

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
		# try:
		# 	im1.save(outDir + "/" + file, format="png")
		# except:
		# 	print("couldnt save")
			#os.remove(inDir + file)
