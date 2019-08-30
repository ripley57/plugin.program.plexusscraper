""" Return Web instance for configured browser in behave.ini """

import behave_webdriver 

from selenium import webdriver

from web import Web


def get_web(browser):
	if browser == "chrome":
		return Web(behave_webdriver.Chrome())

