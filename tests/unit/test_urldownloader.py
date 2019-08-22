""" Unit tests for the URLDownloader class.

	NOTE: 	This probably shouldn't be a unit test, since it inserts a several
		second delay to wait for the web server to start. This therefore
		should probably be an integration test.
"""

import subprocess
import time
import unittest

from plexusscraper.urldownloader import URLDownloader
from plexusscraper.testing.utils.webserver import WebServer

class TestURLDownloader(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		web_server_pid = subprocess.Popen(["python", "src/plexusscraper/testing/utils/webserver.py", "tests/resources/html/"]).pid
		print("web_server_pid=", web_server_pid)
		time.sleep(3)	# Give time for the web server to start

	@classmethod
	def tearDownClass(cls):
		downloader = URLDownloader()
		text = downloader.download('http://localhost:9090/PLEASE_TERMINATE_WEB_SERVER')

	def test_download_valid_url(self):
		downloader = URLDownloader()
		(status, text) = downloader.download('http://localhost:9090/sample_1.html')
		#print("status=", status)
		self.assertTrue(status == 200 and len(text) > 0, 'web page not downloaded')

