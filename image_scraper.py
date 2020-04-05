# from google_images_download import google_images_download as gid
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from collections import OrderedDict
import pymp
import get_related as gr
import numpy as np
import os
import math
import requests
import Image

global sources
global numSources
#global parallelIndex

def search(keyword, limit=100, threads=1):
	linkLimit = math.floor(limit*1.5)

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
	print('numTerms: ' + str(len(terms)))


	sources = []
	numSources = 0

	#parallelIndex = -1
	#i = 0
	# while (len(sources) < 2*limit) and (i < len(terms)):
	# 	sources += gr.getSrc(terms[i])
	# 	i += 1
	# 	#print('numSources: ' + str(len(sources)))

	# numSources = pymp.shared.array((1,), dtype='uint8')
	tempIndex =  -1

	#parallel version
	testList = pymp.shared.list()
	counter = pymp.shared.list()
	while len(testList) <= linkLimit:
		tempIndex += 1
		counter.append(tempIndex)
		with pymp.Parallel(threads) as p:
			for index in p.xrange(0,4):
				if numSources < linkLimit:
					tempSources = gr.getSrc(terms[index + counter[-1]*4])
					with p.lock:
						testList.extend(tempSources)
						numSources = len(testList)
						print('term: ' + str(index + counter[-1]*4) + '\t' +terms[index + counter[-1]*4] + '\tnumSources: ' + str(numSources))

	print('numSources with dupes: ' + str(len(testList)))
	sources = list(OrderedDict.fromkeys(testList))
	print('numSources no dupes: ' + str(len(sources)))
	return sources

def download(downloadDir, sources, width, height, limit=100, threads=1):
	downloadCount = 0
	croppedImages = []
	for source in sources:
		#print every 500 downloads
		if (downloadCount % 500 == 0) and downloadCount != 0:
			print("Has downloaded " + str(downloadCount) + ", using " + str(len(croppedImages)))
		if len(croppedImages) >= limit:
			print ("Total Downloaded and Cropped: " + str(len(croppedImages)))
			return croppedImages
		try:
			r = requests.get(source)
		except:
			continue
		contentType = r.headers.get('content-type')
		if 'image' in contentType:
			tempType = contentType.split('/')[-1]
			filename = downloadDir + str(downloadCount) + '.' + tempType
			open(filename, 'w+b').write(r.content) #saves the file here
			downloadCount += 1
			im = Image.Image(filename, source)
			if im.image.shape[0] >= height and im.image.shape[1] >= width:
				im.crop(width,height)
				croppedImages.append(im)
	print ("Only downloaded and cropped " + str(len(croppedImages)) + "/" + str(limit))
	return croppedImages

def cropDirectory(keyword, width, height, inDir):
	croppedImages = []
	successes = 0
	total = 0
	for file in os.listdir(inDir):
		total += 1
		try:
			im = Image.Image(inDir + file, None)
		except:
			#show files that can't be opened
			#print("Can't open " + inDir + file)
			continue

		#skip images that are too small
		realHeight = im.image.shape[0]
		realWidth = im.image.shape[1]
		if(realWidth < width or realHeight < height):
			continue
		im.crop(width, height)
		croppedImages.append(im)
		successes+=1

	print("Opened and cropped " + str(successes) + " out of " + str(total) + " from " + inDir)
	return croppedImages