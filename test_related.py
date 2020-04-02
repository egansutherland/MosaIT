import sys
import get_related
import image_scraper
import time
import cv2 as cv
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options

keyword = "dogs"

# baseurl = "http://www.bing.com/images/search?q=" + keyword
# options = Options()
# options.headless = True
# driver = webdriver.Chrome(chrome_options=options)
	
# driver.get(baseurl)

#print(get_related.getTerms(driver))
#sources = get_related.getSrc(keyword)
#print(sources)
#print(len(sources))
start = time.perf_counter()
sources = image_scraper.search(keyword, limit=200)
crop = image_scraper.download('Downloads/', sources, 100, 100, limit=200)
cv.imwrite('croppedTest/0.png',crop[0].image)
print(crop[0].image)
print('length of crop: ' + str(len(crop)))
cv.imshow('windo', crop[0].image)
end = time.perf_counter()
diff = end - start
print('total time: ' + str(diff))