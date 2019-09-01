""" The environment file is required by behave. This file contains the fixtures. """

from behave import fixture, use_fixture

# To successfully install psutil, using "pip install psutil", 
# you need to first have "Python.h":
#	sudo apt-get install python3-dev
# https://psutil.readthedocs.io/en/latest/
import psutil

import requests
import subprocess
import time

from browser import Browser
from browser_factory import get_browser
from plexusscraper.testing.utils import wait_for_port

from pages.home_page import HomePage
from pages.urls_page import UrlsPage


#
# Fixture: web_browser
#
#	Launch web browser to simulate user interaction
#

@fixture
def web_browser(context):
	# TODO: Make this available to browser.py
	browser = context.config.userdata['browser']

	context.behave_driver = Browser().get_behave_driver()
	context.home_page = HomePage(browser)
	context.urls_page = UrlsPage(browser)
	yield context.behave_driver
	context.behave_driver.quit()


#
# Fixture: external_website
#
# 	Simulate an external website serving web pages to scrape.
#

def stop_external_website():
	""" Our custom web server recognises the following as a request to stop cleanly """
	requests.get('http://localhost:9090/PLEASE_TERMINATE_WEB_SERVER')

@fixture
def external_website(context):
	""" Simulate a regular website on the Internet to scrape """
	wait_for_port(909)
	web_server_pid = subprocess.Popen(["python", "src/plexusscraper/testing/webserver.py", "tests/resources/html/", "9090"]).pid
	#print("web_server_pid=", web_server_pid)
	context.add_cleanup(stop_external_website)
	time.sleep(3)	# Give some time for the web server to start-up


#
# Fixture: kodi_mock
#
# 	Simulate the Kodi web server and rpc server.
#
# 	NOTE: 	The mock kodi web server requires PHP to be installed on the test 
#		machine, plus the PHP "SimpleXML" addon:
#
#			apt-get install php7.2-xml
#			php -m | grep -i simple
#

@fixture
def kodi_mock(context):
	""" Simulate the Kodi web server and the Kodi rpc server """

	# Start mock kodi web server.
	# TODO: Can we avoid using a hard-coded absolute path to the webinterface.webif files?
	wait_for_port(8080, kill_process=True, process_name='php')
	kodi_web_server = psutil.Process(subprocess.Popen(["php", "-S", "localhost:8080", "-t", "/files/08_Github/webinterface.webif/"]).pid)
	print("kodi_web_server: pid=", kodi_web_server.pid)

	# Start mock kodi rpc server.
	wait_for_port(9090, kill_process=True, process_name='python', debug=False)
	kodi_rpc_server = psutil.Process(subprocess.Popen(["python", "src/plexusscraper/testing/webserver.py", "tests/resources/html/", "9090"]).pid)
	print("kodi_rpc_server: pid=", kodi_rpc_server.pid)

	time.sleep(3)	# Give time for web servers to start-up

	yield	

	# Now stop the mock kodi servers.
	# (Comment these if you want to play with the servers manually)
	requests.get('http://localhost:9090/PLEASE_TERMINATE_WEB_SERVER')
	kodi_web_server.terminate()


def before_tag(context, tag):
	if tag == 'fixture.web_browser':
		use_fixture(web_browser, context)
	elif tag == 'fixture.external_website':
		use_fixture(external_website, context)
	elif tag == 'fixture.kodi_mock':
		use_fixture(kodi_mock, context)

