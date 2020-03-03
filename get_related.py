from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
import time
#from selenium.webdriver.common.exceptions import NoSuchElementException

def getTerms(keyword, headless=True, sleeptime = 0):
	
	baseurl = "http://www.bing.com/images/search?q=" + keyword
	options = Options()
	if headless:
		options.headless = True
	driver = webdriver.Chrome(chrome_options=options)

	driver.get(baseurl)

	elements = driver.find_elements(By.CLASS_NAME, 'it')

	if not elements:
		searchAgain = driver.find_element(By.ID, 'sb_go_par')
		searchAgain.click()
		time.sleep(sleeptime)
		safeSearchDropDown = driver.find_element(By.ID, 'ftr_ss_hl')
		safeSearchDropDown.click()
		time.sleep(sleeptime)
		safeOptions = driver.find_element(By.CLASS_NAME, "ftrD_MmVert")
		optionsList = safeOptions.find_elements(By.TAG_NAME, "a")
		optionsList[1].click()
		time.sleep(sleeptime)
		elements = driver.find_elements(By.CLASS_NAME, 'it')

	relatedTerms = []

	clean = re.compile('<.*?>')

	for i in range(0, len(elements)):
		relatedTerms.append(elements[i].get_attribute("innerHTML"))
		relatedTerms[i]=re.sub('  ', ' ', re.sub(clean, ' ', relatedTerms[i]).strip())

	driver.close()
	
	return relatedTerms