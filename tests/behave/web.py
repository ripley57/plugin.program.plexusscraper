""" Web: helper class to wrap Selenium WebDriver and WebDriverWait """

from contextlib import contextmanager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import staleness_of
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# NOTE: The reason for this class and WebDriverWait:
# https://blog.codeship.com/get-selenium-to-wait-for-page-load/
# https://stackoverflow.com/questions/31492363/how-to-get-page-source-after-button-click-using-selenium
# https://sqa.stackexchange.com/questions/24961/selenium-getpagesource-returns-previous-pages-source
# https://stackoverflow.com/questions/51784033/selenium-python-behave-webdriverwait#51790125
# https://dzone.com/articles/using-the-behave-framework-for-selenium-bdd-testin


class Web:
	__TIMEOUT = 10

	def __init__(self, web_driver):
		super().__init__()
		self._web_driver_wait = WebDriverWait(web_driver, Web.__TIMEOUT)
		self._web_driver = web_driver

	def open(self, url):
		self.__web_driver.get(url)

	def find_by_xpath(self, xpath):
		""" Wait for single element to be present on the web page """
		# NOTE: To debug, run behave with --no-capture
		# Example: behave tests/behave --tags="@wip" --no-capture
		#import pdb; pdb.set_trace()
		return self._web_driver_wait.until(EC.visibility_of_element_located((By.XPATH, xpath)))

	def finds_by_xpath(self, xpath):
		"""" Wait for multiple elements to be present on the web page """
		return self._web_driver_wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

	def quit(self):
		return self._web_driver.quit()

	@contextmanager
	def wait_for_page_load(self, timeout=30):
		""" https://blog.codeship.com/get-selenium-to-wait-for-page-load/ 

		I *thought* I hit this same issue, namely calling Seleniun "click()" indeed loads 
		the new page in the browser (I can see it), but Selenium still refers to the old
		page contents! My cause turned out to be that my page was loading in a new tab 
		(because my html used target="_NEW")! Once I changed my html (to target="_self")
		then everything worked as expected. Note that I don't think the extra waiting
		here is needed, because my functions find(s)_by_xpath() above already include a
		wait and timeout.

		"""
		old_page = self._web_driver.find_element_by_tag_name('html')
		yield
		WebDriverWait(self._web_driver, timeout).until(staleness_of(old_page))

