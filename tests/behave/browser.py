""" Web: Class to wrap Selenium WebDriver and WebDriverWait """

import behave_webdriver

from contextlib import contextmanager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Browser(object):
	__TIMEOUT = 10

	_behave_driver = behave_webdriver.Chrome()
	_driver_wait = WebDriverWait(_behave_driver, __TIMEOUT)


	@classmethod
	def get_behave_driver(cls):
		return Browser._behave_driver
	

	def get_page_title(self):
		return Browser._behave_driver.title	


	def navigate(self, address):
		Browser._behave_driver.get(address)


	def click_link(self, link_text):
		Browser.click_element((By.XPATH, "//a[@href='{}']".format(link_text)))


	def click_element(self, *locator):
		Browser._driver_wait.until(EC.visibility_of_element_located(*locator)).click()


	def find_element(self, *locator):
		return Browser._driver_wait.until(EC.visibility_of_element_located(*locator))


	def find_all_elements(self, *locator):
		return Browser._driver_wait.until(EC.visibility_of_all_elements_located(*locator))


	def refresh(self):
		Browser._behave_driver.refresh()


	#@contextmanager
	#def wait_for_page_load(self, timeout=30):
	#	""" From https://blog.codeship.com/get-selenium-to-wait-for-page-load/ 
	#
	#	I *thought* I had this same issue; namely calling Seleniun "click()" loads a 
	#	new page in the browser (i.e. I can see it visually), but Selenium values still 
	#	refers to the old page contents! The cause of my problem turned out to be my 
	#	page was loading in a new tab (because my html used target="_NEW"). Once I 
	#	changed my html to target="_self", everything then worked as expected.
	#
	#	Note: I don't think this function (wait_for_page_load()) is actually needed, 
	#	because we are calling it together with find(s)_by_xpath(), which already
	#	includes another wait. Example usage:
	#
	#	with context.web.wait_for_page_load(timeout=10):
	#		context.web.find_by_xpath("//span[text()='Upload Plexus Scraper URLs:']")
	#
	#	"""
	#	old_page = self._web_driver.find_element_by_tag_name('html')
	#	yield
	#	WebDriverWait(self._web_driver, timeout).until(staleness_of(old_page))

