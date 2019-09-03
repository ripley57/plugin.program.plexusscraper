""" Web: Class to wrap Selenium WebDriver and WebDriverWait """

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from plexusscraper.testing.config import TestConfig


class Browser(object):
	_TIMEOUT = 10

	_driver = None
	_driver_wait = None

	@classmethod
	def get_driver(cls):
		if not Browser._driver:
			Browser._driver = TestConfig.get_webdriver()
			Browser._driver_wait = WebDriverWait(Browser._driver, Browser._TIMEOUT)
		return Browser._driver
	

	@classmethod
	def get_page_title(cls):
		return Browser._driver.title	


	@classmethod
	def navigate(cls, address):
		Browser._driver.get(address)


	@classmethod
	def click_element(cls, *locator):
		Browser._driver_wait.until(EC.visibility_of_element_located(*locator)).click()

	@classmethod
	def click_link(cls, link_text):
		Browser.click_element((By.XPATH, "//a[@href='{}']".format(link_text)))


	@classmethod
	def find_element(cls, *locator):
		return Browser._driver_wait.until(EC.visibility_of_element_located(*locator))


	@classmethod
	def find_all_elements(cls, *locator):
		return Browser._driver_wait.until(EC.visibility_of_all_elements_located(*locator))


	@classmethod
	def reload(cls):
		Browser._driver.refresh()

