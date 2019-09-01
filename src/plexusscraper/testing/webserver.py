""" Simple file web server to serve files from a specific directory 

    To stop the web server, include "PLEASE_TERMINATE_WEB_SERVER" in a request, e.g:
    http://localhost:9090/PLEASE_TERMINATE_WEB_SERVER
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import os
import sys
import time

from plexusscraper.testing.kodi import MockKodiRPCHandler


g_terminate = False

class MyRequestHandler(SimpleHTTPRequestHandler):
	def do_GET(self):
		""" Override do_GET 
		    See https://blog.anvileight.com/posts/simple-python-http-server/
		"""
		if self.path and (self.path.find("PLEASE_TERMINATE_WEB_SERVER") > 0):
			global g_terminate
			g_terminate = True
			self.send_response(200)
			self.end_headers()
			self.wfile.write(b'Terminating web server!')

		elif self.path and (self.path.startswith("/jsonrpc") > 0):
			kodi = MockKodiRPCHandler()
			self.send_response(200)
			self.send_header('Content-type', 'application/json')
			self.end_headers()
			self.wfile.write(str.encode(kodi.handle_rpc(self.path)))

		else:
			return super().do_GET()

class WebServer:
	def __init__(self, _dir, _port):
		self.dir = _dir		# We will serve the files in this directory
		self.port = _port

	def keep_running(self):
		global g_terminate
		return not g_terminate

	def start(self):
		os.chdir(self.dir)
		httpd = HTTPServer(('', self.port), MyRequestHandler)
		while self.keep_running():
			try:
				httpd.handle_request()
			except:		
				pass

# Example usage:
#	python3 webserver.py 'test/resources/html/'
#
if __name__ == '__main__':
	dir = sys.argv[1] if len(sys.argv) > 1 else "."
	port = int(sys.argv[2]) if len(sys.argv) > 2 else 9090
	web_server = WebServer(dir, port)
	web_server.start()
	print("WebServer exiting.")

