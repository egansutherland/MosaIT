import sys
import get_related
import image_scraper
import image_ordering
import image_builder
import TargetImage
import time
import cv2 as cv
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

keyword = "cats"

# baseurl = "http://www.bing.com/images/search?q=" + keyword
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(chrome_options=options)
	
# driver.get(baseurl)

#print(get_related.getTerms(driver))
#sources = get_related.getSrc(keyword)
#print(sources)
#print(len(sources))
x = 30
y = 30
targetImageFile = 'Input/input.jpg'
targetImage = TargetImage.TargetImage(targetImageFile, x, y)
height = targetImage.grid[0].image.shape[0]
width = targetImage.grid[0].image.shape[1]


startTotal = time.perf_counter()
sources = image_scraper.search(keyword, limit=15000)
croppedImages = image_scraper.download('Downloads/', sources, width, height, limit=15000)

#cv.imwrite('croppedTest/0.png',crop[0].image)
#print(crop[0].image)
print('length of crop: ' + str(len(croppedImages)))

orderedImages = image_ordering.OrderImages(targetImage,croppedImages, 0, True, False)
image_builder.BuildImage(x, y, orderedImages, outputDirectory='Mosaic/', outputName='yay.png')
#cv.imshow('windo', crop[0].image)
endTotal = time.perf_counter()
totalDiff = endTotal - startTotal
print('total time: ' + str(totalDiff))