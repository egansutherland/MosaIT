from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from collections import OrderedDict
import re
import xml.etree.ElementTree as ET
import time
#from selenium.webdriver.common.exceptions import NoSuchElementException

# get search terms related to provided keyword
def getTerms(driver):
	elements = driver.find_elements(By.CLASS_NAME, 'suggestion-title')

	if not elements:
		bypass_safe(driver)
		print('wait')
		elements = driver.find_elements(By.CLASS_NAME, 'suggestion-title')

	relatedTerms = []

	clean = re.compile('<.*?>')

	for i in range(0, len(elements)):
		relatedTerms.append(elements[i].get_attribute("innerHTML"))
		relatedTerms[i]=re.sub('  ', ' ', re.sub(clean, ' ', relatedTerms[i]).strip())

	# for i in range(0, len(relatedTerms)):
	# 	relatedTerms[i]=re.sub('  ', ' ', re.sub(clean, ' ', relatedTerms[i]).strip())

	driver.close()
	
	return relatedTerms

def bypass_safe(driver):
	driver.find_element_by_css_selector('#sb_form_go').click()

	try:
		elem = driver.find_element(By.CLASS_NAME, 'suggestion-title')

	except NoSuchElementException:
		clickItem = WebDriverWait(driver, 10, poll_frequency=0.25)

		# 'safe-search filter drop down'
		driver.find_element_by_css_selector('#ftr_ss_hl').click()
		
		# 'ok' button
		driver.find_element_by_xpath('//*[@id="ftr_ss_d"]/div/a[2]').click()


# get list of image sources
def getSrc(keyword):

	baseurl = "http://www.bing.com/images/search?q=" + keyword
	options = Options()
	options.headless = False
	driver = webdriver.Chrome(chrome_options=options)

	driver.get(baseurl)

	sources = []
	seeMoreNum = 0

	try:
		elem = driver.find_element(By.CLASS_NAME, 'suggestion-title')
	except NoSuchElementException:
		bypass_safe(driver)

	scrollToBottom(driver)

	elements = driver.find_elements(By.CLASS_NAME, 'mimg')
	
	for i in elements:
		sources.append(i.get_attribute("src"))

	driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

	for j in range(0..12)
		#change dominant color
		changeDomColor(driver, j)

		scrollToBottom(driver)

		elements = driver.find_elements(By.CLASS_NAME, 'mimg')
	
		for i in elements:
			sources.append(i.get_attribute("src"))

		#scroll to top
		driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

	sources = list(OrderedDict.fromkeys(sources))

	driver.close()

	return sources

def scrollToBottom(driver):
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(0.2)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			seeMoreNum += 1
			driver.find_element(By.XPATH, '//*[@id="bop_container"]/div[2]/a')
		if seeMoreNum >= 3:
			break
		last_height = new_height

def changeDomColor(driver, ind):
	colors = ['//*[@id="ftrB"]/ul/li[2]/div/div/div/div[1]', '//*[@id="ftrB"]/ul/li[2]/div/div/div/div[2]', '//*[@id="ftrB"]/ul/li[2]/div/div/div/div[3]', '//*[@id="ftrB"]/ul/li[2]/div/div/div/div[4]', '//*[@id="ftrB"]/ul/li[2]/div/div/div/div[5]', '//*[@id="ftrB"]/ul/li[2]/div/div/div/div[6]', '//*[@id="ftrB"]/ul/li[2]/div/div/div/div[7]', '//*[@id="ftrB"]/ul/li[2]/div/div/div/div[8]', '//*[@id="ftrB"]/ul/li[2]/div/div/div/div[9]', '//*[@id="ftrB"]/ul/li[2]/div/div/div/div[10]', '//*[@id="ftrB"]/ul/li[2]/div/div/div/div[11]', '//*[@id="ftrB"]/ul/li[2]/div/div/div/div[12]']

	
