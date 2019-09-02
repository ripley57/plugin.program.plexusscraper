""" Web: Class to wrap Selenium WebDriver and WebDriverWait """

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from plexusscraper.testing.config import TestConfig


class Browser(object):

	_TIMEOUT = 10

	_driver = TestConfig.get_webdriver()
	_driver_wait = WebDriverWait(_driver, _TIMEOUT)
	

	def get_driver(self):
		return self._driver
	

	def get_page_title(self):
		return self._driver.title	


	def navigate(self, address):
		self._driver.get(address)


	def click_element(self, *locator):
		self._driver_wait.until(EC.visibility_of_element_located(*locator)).click()


	def click_link(self, link_text):
		self.click_element((By.XPATH, "//a[@href='{}']".format(link_text)))


	def find_element(self, *locator):
		return self._driver_wait.until(EC.visibility_of_element_located(*locator))


	def find_all_elements(self, *locator):
		return self._driver_wait.until(EC.visibility_of_all_elements_located(*locator))


	def refresh(self):
		self._driver.refresh()

