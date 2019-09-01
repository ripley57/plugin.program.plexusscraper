import collections

from selenium.webdriver.common.by import By
from browser import Browser


class UrlsPage(Browser):

	Url = collections.namedtuple('Url', 'id tb btn')

	urls = ( Url(id='url_1', tb=(By.XPATH, "//input[@type='text' and @class='urlTextbox' and @name='url_1']"), btn=(By.XPATH, "//button[@id='button_url_1']")),
	         Url(id='url_2', tb=(By.XPATH, "//input[@type='text' and @class='urlTextbox' and @name='url_2']"), btn=(By.XPATH, "//button[@id='button_url_2']")),
                 Url(id='url_3', tb=(By.XPATH, "//input[@type='text' and @class='urlTextbox' and @name='url_3']"), btn=(By.XPATH, "//button[@id='button_url_3']")),
	         Url(id='url_4', tb=(By.XPATH, "//input[@type='text' and @class='urlTextbox' and @name='url_4']"), btn=(By.XPATH, "//button[@id='button_url_4']")),
	         Url(id='url_5', tb=(By.XPATH, "//input[@type='text' and @class='urlTextbox' and @name='url_5']"), btn=(By.XPATH, "//button[@id='button_url_5']")) )

	ALL_URLS = (By.XPATH, "//input[@type='text' and @class='urlTextbox' and starts-with(@name,'url_')]")
	URL_SAVE_RESULT = (By.XPATH, "//span[@id='result']")


	def __init__(self, _browser):
		pass


	def _save_url(self, url, tb, btn):
		url_input = super().find_element(tb)
		url_button = super().find_element(btn)
		url_input.clear()
		url_input.send_keys(url)
		url_button.click()


	def find_url(self, id):
		u = [x for x in UrlsPage.urls if x.id == id]
		if len(u) != 1:
			raise RuntimeError("Could not find url id: " + id)
		return u[0]


	def save_url(self, id, url):
		u = self.find_url(id)
		self._save_url(url, u.tb, u.btn)


	def get_url(self, id):
		u = self.find_url(id)
		return super().find_element(u.tb).get_attribute('value')


	def get_all_urls(self):
		return super().find_all_elements(UrlsPage.ALL_URLS)


	def get_url_save_result(self):
		return super().find_element(UrlsPage.URL_SAVE_RESULT).text

