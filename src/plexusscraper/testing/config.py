""" Class TestConfig: Contains test configuration settings. """

import behave_webdriver
import os


class TestConfig:

	_OPTIONS = { 	'webinterface_webif_path' : '/files/08_Github/webinterface.webif/'	}

	@classmethod
	def get_config_value(cls, name):
		return TestConfig._OPTIONS[name]


	@classmethod
	def set_config_value(cls, name, value):
		TestConfig._OPTIONS[name] = value


	@classmethod
	def get_webdriver(cls):
		""" Return selenium browser driver to use """
		return behave_webdriver.Chrome()


	@classmethod
	def get_env_dict(cls, **extra):
		""" Return dictionary of environment variables, plus optional extra entries """
		e = dict(os.environ)
		e.update(extra)
		return e

