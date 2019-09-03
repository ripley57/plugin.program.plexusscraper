""" Page object for the URLs page """

import collections
from selenium.webdriver.common.by import By

from plexusscraper.testing.browser import Browser


class UrlsPage(Browser):

	Url = collections.namedtuple('Url', 'id tb btn')

	# Individual lLocators for each url entry textbox.
	urls = ( Url(id='url_1', tb=(By.XPATH, "//input[@type='text' and @class='urlTextbox' and @name='url_1']"), btn=(By.XPATH, "//button[@id='button_url_1']")),
	         Url(id='url_2', tb=(By.XPATH, "//input[@type='text' and @class='urlTextbox' and @name='url_2']"), btn=(By.XPATH, "//button[@id='button_url_2']")),
                 Url(id='url_3', tb=(By.XPATH, "//input[@type='text' and @class='urlTextbox' and @name='url_3']"), btn=(By.XPATH, "//button[@id='button_url_3']")),
	         Url(id='url_4', tb=(By.XPATH, "//input[@type='text' and @class='urlTextbox' and @name='url_4']"), btn=(By.XPATH, "//button[@id='button_url_4']")),
	         Url(id='url_5', tb=(By.XPATH, "//input[@type='text' and @class='urlTextbox' and @name='url_5']"), btn=(By.XPATH, "//button[@id='button_url_5']")) )

	ALL_URLS = (By.XPATH, "//input[@type='text' and @class='urlTextbox' and starts-with(@name,'url_')]")
	URL_SAVE_RESULT = (By.XPATH, "//span[@id='result']")


	@classmethod
	def _save_url(cls, url, tb, btn):
		""" Save a new url by clicking the url element's save button """
		url_input = super().find_element(tb)
		url_button = super().find_element(btn)
		url_input.clear()
		url_input.send_keys(url)
		url_button.click()


	@classmethod
	def find_url(cls, id):
		""" Return url element given by id """
		u = [x for x in UrlsPage.urls if x.id == id]
		if len(u) != 1:
			raise RuntimeError("UrlsPage::find_url() Could not find url id: " + id)
		return u[0]


	@classmethod
	def save_url(cls, id, url):
		""" Save new url in url element given by id """
		u = UrlsPage.find_url(id)
		UrlsPage._save_url(url, u.tb, u.btn)


	@classmethod
	def get_url(cls, id):
		""" Return the value of url element given by id """
		u = UrlsPage.find_url(id)
		return super().find_element(u.tb).get_attribute('value')


	@classmethod
	def get_all_urls(cls):
		""" Return all url elements """
		return super().find_all_elements(UrlsPage.ALL_URLS)


	@classmethod
	def get_url_save_result(cls):
		""" Return the last result from saving a url """
		return super().find_element(UrlsPage.URL_SAVE_RESULT).text

