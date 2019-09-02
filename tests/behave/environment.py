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

from plexusscraper.kodi.settings import KodiSettingsXml

from plexusscraper.testing.browser.browser import Browser
from plexusscraper.testing.browser.pages.home_page import HomePage
from plexusscraper.testing.browser.pages.urls_page import UrlsPage
from plexusscraper.testing.config import TestConfig
from plexusscraper.testing.utils import wait_for_port, create_tmpfile, delete_file


#
# Fixture: web_browser
#
#	Launch web browser to simulate user interaction
#

@fixture
def web_browser(context):
	# Read value from behave.ini
	#browser = context.config.userdata['browser']

	context.behave_driver = Browser().get_driver()
	context.home_page = HomePage()
	context.urls_page = UrlsPage()

	yield context.behave_driver

	context.behave_driver.quit()


#
# Fixture: external_website
#
# 	Simulate an external website serving web pages to scrape.
#

@fixture
def external_website(context):
	""" Simulate a regular website on the Internet to scrape """

	wait_for_port(9999, debug=False)
	web_server_pid = subprocess.Popen(["python", "src/plexusscraper/testing/webserver.py", "tests/resources/html/", "9999"]).pid
	print("web_server_pid=", web_server_pid)
	time.sleep(2)	# Give some time for the server to start.

	yield

	""" Our custom web server recognises the following as a request to stop cleanly """
	requests.get('http://localhost:9999/PLEASE_TERMINATE_WEB_SERVER')
	time.sleep(2)	# Give time for the server to stop.


#
# Fixture: settings_xml
#
#	Create a settings.xml file
#

@fixture
def settings_xml(context):
	context.settings_xml_path = create_tmpfile(_suffix='settings_xml')
	KodiSettingsXml.create(context.settings_xml_path)

	# Add some example url entries.
	xml_file = KodiSettingsXml(context.settings_xml_path)
	xml_file.add_setting('url_1', 'http://somedomain.com/pagex.html')
	xml_file.add_setting('url_2', 'acestream://d387bd5bd1d3f0fd2683eba654aeaf44acac660c')
	xml_file.add_setting('url_5', 'sop://broker.sopcast.com:3912/264820')

	yield

	# Finished with the xml file.
	delete_file(context.settings_xml_path)


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
	wait_for_port(8080, kill_process=True, process_name='php', debug=False)
	webinterface_webif_path = TestConfig.get_config_value('webinterface_webif_path')
	d = TestConfig.get_env_dict(SETTINGS_XML_PATH=context.settings_xml_path)
	kodi_web_server = psutil.Process(subprocess.Popen(["php", "-S", "localhost:8080", "-t", webinterface_webif_path], env=d).pid)
	print("kodi_web_server: pid=", kodi_web_server.pid)

	# Start mock kodi rpc server.
	wait_for_port(9090, kill_process=True, process_name='python', debug=False)
	kodi_rpc_server = psutil.Process(subprocess.Popen(["python", "src/plexusscraper/testing/webserver.py", "tests/resources/html/", "9090"], env=d).pid)
	print("kodi_rpc_server: pid=", kodi_rpc_server.pid)

	time.sleep(3)	# Give time for the servers to start.

	yield	

	# Now stop the mock kodi servers.
	# (Note: Comment these if you want to play with the servers manually)
	requests.get('http://localhost:9090/PLEASE_TERMINATE_WEB_SERVER')
	kodi_web_server.terminate()
	time.sleep(3)	# Give time for the servers to stop.


def before_tag(context, tag):
	if tag == 'fixture.web_browser':
		use_fixture(web_browser, context)
	elif tag == 'fixture.settings_xml':
		use_fixture(settings_xml, context)
	elif tag == 'fixture.external_website':
		use_fixture(external_website, context)
	elif tag == 'fixture.kodi_mock':
		use_fixture(kodi_mock, context)

