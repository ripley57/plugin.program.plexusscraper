""" Unit tests for the URLDownloader class. """

import pytest
import requests
import subprocess
import time

from plexusscraper.urldownloader import URLDownloader
from plexusscraper.testing.utils import wait_for_port


@pytest.fixture()
def external_website():
	wait_for_port(9000, debug=False)
	web_server_pid = subprocess.Popen(["python", "src/plexusscraper/testing/webserver.py", "tests/resources/html/", "9000"]).pid
	print("web_server_pid=", web_server_pid)
	time.sleep(2)
	yield
	requests.get('http://localhost:9000/PLEASE_TERMINATE_WEB_SERVER')


@pytest.mark.slow
def test_download_valid_url(external_website):
	time.sleep(10)	# NOTE: Need this for some reason - to avoid connection error (errno 111).
	(status, text) = URLDownloader.download('http://localhost:9000/sample_1.html')
	assert(status == 200 and len(text) > 0)

