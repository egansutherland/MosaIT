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
import multiprocessing

global sources
global numSources
#global parallelIndex

def search(keyword, limit=100, threads=1):
	linkLimit = math.floor(limit*1.25)

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

	#so we don't spawn more threads than terms
	if len(terms) < threads:
		threads = len(terms)


	sources = []
	numSources = 0

	#tempIndex =  -1

	#parallel version
	testList = pymp.shared.list()
	counter = multiprocessing.Value("i", -1)

	while len(testList) <= linkLimit:
		#tempIndex += 1
		#counter.append(tempIndex)
		with pymp.Parallel(threads) as p:
			for index in p.xrange(0,threads):
				if numSources < linkLimit:
					calcIndex = 0
					with p.lock:
						counter.value += 1
						calcIndex = counter.value
					tempSources = gr.getSrc(terms[calcIndex])
					with p.lock:
						testList.extend(tempSources)
						numSources = len(testList)
						print('term: ' + str(calcIndex) + '\t' +terms[calcIndex] + '\tnumSources: ' + str(numSources))

	print('numSources with dupes: ' + str(len(testList)))
	sources = list(OrderedDict.fromkeys(testList))
	print('numSources no dupes: ' + str(len(sources)))
	return sources

def download(downloadDir, sources, width, height, limit=100, threads=1):
	croppedImages = []
	numSources = len(sources)
	testList = pymp.shared.list()
	downloadCount = multiprocessing.Value("i", 0)

	with pymp.Parallel(threads) as p:
		for source in p.range(0, numSources):
			if len(testList) >= limit:
				break
			#print every 500 downloads
			if (downloadCount.value % 500 == 0) and downloadCount.value != 0:
				print("Has downloaded " + str(downloadCount.value) + ", using " + str(len(testList)))
			try:
				r = requests.get(sources[source])
			except:
				continue
			contentType = r.headers.get('content-type')
			if contentType == None:
				pass
			elif 'image' in contentType:
				tempType = contentType.split('/')[-1]
				filename = downloadDir + '/' + str(source) + '.' + tempType
				open(filename, 'w+b').write(r.content) #saves the file here
				im = Image.Image(filename, sources[source])
				if im.image.shape[0] > height and im.image.shape[1] > width:
					im.crop(width, height)
				with p.lock:
					downloadCount.value += 1
					if im.image.shape[0] == height and im.image.shape[1] == width:
						testList.append(im)
			else:
				pass

	croppedImages = list(testList)
	if len(croppedImages) >= limit:
		print ("Total Downloaded and Cropped: " + str(len(croppedImages)))
	else:
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