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
import time

global sources
global numSources

#searches the web based on keyword and related keywords and returns ~1.25*limit image sources (urls). Spawns as many threads as passed in
def search(keyword, limit=100, threads=1):

	#should get more sources than limit, just in case some urls don't work, or the image is too small
	linkLimit = math.floor(limit*1.25)

	#start the selenium chrome driver for getting related terms
	baseurl = "http://www.bing.com/images/search?q=" + keyword
	options = Options()
	options.headless = True
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-dev-shm-usage')
	driver = webdriver.Chrome(chrome_options=options)
	driver.get(baseurl)

	#get related terms
	terms = []
	terms.append(keyword)
	terms += gr.getTerms(driver)
	print('numTerms: ' + str(len(terms)))

	#so we don't spawn more threads than terms
	if len(terms) < threads:
		threads = len(terms)

	sources = []
	numSources = 0

	#parallel variables used by all threads
	srcList = pymp.shared.list()
	counter = multiprocessing.Value("i", -1)

	#iterate through terms getting sources until 
	while len(srcList) <= linkLimit:
		with pymp.Parallel(threads) as p:
			for index in p.xrange(0,threads):
				if numSources < linkLimit:
					calcIndex = 0
					with p.lock:
						counter.value += 1
						calcIndex = counter.value
					tempSources = gr.getSrc(terms[calcIndex])
					with p.lock:
						srcList.extend(tempSources)
						numSources = len(srcList)
						print('term: ' + str(calcIndex) + '\t' +terms[calcIndex] + '\tnumSources: ' + str(numSources))

	print('numSources with dupes: ' + str(len(srcList)))
	#remove duplicates
	try:
		sources = list(OrderedDict.fromkeys(srcList))
	except:
		time.sleep(5)
		sources = list(OrderedDict.fromkeys(srcList))

	print('numSources no dupes: ' + str(len(sources)))
	return sources

#downloads limit amount of images from the list sources and crop them to width and height. Spawns as many threads as are passed in.
def download(downloadDir, sources, width, height, limit=100, threads=1):
	croppedImages = []
	numSources = len(sources)

	#parallel variables
	downloadList = pymp.shared.list()
	downloadCount = multiprocessing.Value("i", 0)

	with pymp.Parallel(threads) as p:
		#iterate through each source, attempting to download, open as image, and crop to right size
		for source in p.range(0, numSources):
			if len(downloadList) >= limit:
				break
			#print every 500 downloads
			if (downloadCount.value % 500 == 0) and downloadCount.value != 0:
				print("Has downloaded " + str(downloadCount.value) + ", using " + str(len(downloadList)))
			try:
				#download from source
				r = requests.get(sources[source])
				contentType = r.headers.get('content-type')
				#check if image
				if 'image' in contentType:
					tempType = contentType.split('/')[-1]
					filename = downloadDir + '/' + str(source) + '.' + tempType
					#saves the file here
					open(filename, 'w+b').write(r.content)
					#make image object
					im = Image.Image(filename, sources[source])
					#crop to right size
					if im.image.shape[0] > height and im.image.shape[1] > width:
						im.crop(width, height)
					#get parallel list and append image to it if right size
					with p.lock:
						downloadCount.value += 1
						if im.image.shape[0] == height and im.image.shape[1] == width:
							downloadList.append(im)
			except:
				#unsuccessful in downloading from src
				continue

	#convert to regular list
	try:
		croppedImages = list(downloadList)
	except:
		time.sleep(5)
		croppedImages = list(downloadList)

	if len(croppedImages) >= limit:
		print ("Total Downloaded and Cropped: " + str(len(croppedImages)))
	else:
		print ("Only downloaded and cropped " + str(len(croppedImages)) + "/" + str(limit))
	return croppedImages

#takes in a directory inDir, tries to open all files as images and crop to width and height, then returns a list of cropped images
def cropDirectory(keyword, width, height, inDir):
	croppedImages = []
	successes = 0
	total = 0
	#iterate through files trying to open as image and crop to right size
	for file in os.listdir(inDir):
		total += 1
		try:
			im = Image.Image(inDir + file, None)
		except:
			continue

		#skip images that are too small
		realHeight = im.image.shape[0]
		realWidth = im.image.shape[1]
		if(realWidth < width or realHeight < height):
			continue
		#crop to right size and add to list
		im.crop(width, height)
		croppedImages.append(im)
		successes+=1

	print("Opened and cropped " + str(successes) + " out of " + str(total) + " from " + inDir)
	return croppedImages