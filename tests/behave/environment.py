import os
import subprocess
import time
from behave import fixture, use_fixture

from plexusscraper.urldownloader import URLDownloader
from plexusscraper.testing.utils.webserver import WebServer

# See: https://behave.readthedocs.io/en/latest/fixtures.html
# We simply use a '@fixture...' tag in our ".feature" file and look for the tag 
# here in this module in special unittest functions such as "before_feature()".

def stop_web_server():
	downloader = URLDownloader()
	text = downloader.download('http://localhost:9090/PLEASE_TERMINATE_WEB_SERVER')

@fixture
def webserver_http(context):
	# -- SETUP-FIXTURE PART
	web_server_pid = subprocess.Popen(["python", "src/plexusscraper/testing/utils/webserver.py", "tests/resources/html/"]).pid
	print("web_server_pid=", web_server_pid)
	context.add_cleanup(stop_web_server)
	time.sleep(3)	# Give time for the web server to start

# See: https://stackoverflow.com/questions/34126474/running-certain-steps-once-before-a-scenario-outline-python-behave
def before_feature(context, feature):
	if 'fixture.webserver' in feature.tags:
		use_fixture(webserver_http, context)

# See: https://stackoverflow.com/questions/34126474/running-certain-steps-once-before-a-scenario-outline-python-behave
#def before_scenario(context, scenario):
#	if 'fixture.webserver' in scenario.tags:
#		use_fixture(webserver_http, context)
