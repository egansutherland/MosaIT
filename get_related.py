from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import xml.etree.ElementTree as ET
#from selenium.webdriver.common.exceptions import NoSuchElementException

def getTerms(keyword):
	
	baseurl = "http://www.bing.com/images/search?q=" + keyword
	options = Options()
	options.headless = True
	driver = webdriver.Chrome(chrome_options=options)
	
	driver.get(baseurl)

	elements = driver.find_elements(By.CLASS_NAME, 'it')

	relatedTerms = []

	clean = re.compile('<.*?>')

	for i in range(0, len(elements)):
		relatedTerms.append(elements[i].get_attribute("innerHTML"))
		relatedTerms[i]=re.sub('  ', ' ', re.sub(clean, ' ', relatedTerms[i]).strip())

	# for i in range(0, len(relatedTerms)):
	# 	relatedTerms[i]=re.sub('  ', ' ', re.sub(clean, ' ', relatedTerms[i]).strip())

	driver.close()
	
	return relatedTerms