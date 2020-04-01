import sys
import get_related
import image_scraper
import time
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
image_scraper.search(keyword, 'whatever', limit=5000)
end = time.perf_counter()
diff = end - start
print('total time: ' + str(diff))