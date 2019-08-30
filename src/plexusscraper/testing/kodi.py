""" Mock Kodi RPC handling """

import ast

import cgitb
cgitb.enable()

from urllib.parse import unquote 


class MockKodiRPCHandler:
	def __addurl(self, params):
		url_path = params['url_path']
		url_id = params['url_id']
		
		# Add url to settings.xml
		#
		# NOTE: In the original version of Plexus Scraper, we only
		#	ever updated the settings.xml file using the Kodi API:
		#
		#	xbmcaddon.Addon(id='program.plexusscraper').setSetting(setting_id,url_path)
		#
		#	From now on, we are going to update the xml file ourself directly.
		#	
		#print("TODO: url_path=", url_path)


	def handle_rpc(self, _path):
		path, query = _path.split('?')
	
		# Url-decode.
		query_decoded = unquote(query)

		# Example decoded query string:
		# request={"id":1,"jsonrpc":"2.0","method":"Addons.ExecuteAddon",
		# "params":{"addonid":"program.plexusscraper",
		# "params":{"url_path":"https://streamingsports.me/aston-villa-vs-everton-live-streaming/173081.html","mode":"addurl","url_id":"2"}}}
		#print("query_decoded =", query_decoded)

		# Remove prefix "request="
		if query_decoded.startswith("request="):
			query_decoded = query_decoded[8:]

		# Decode the json in the request
		query_dict = ast.literal_eval(query_decoded)

		# Extract values, and perform appropriate action.
		params = query_dict['params']['params']
		mode = params['mode']
		if mode == "addurl":
			self.__addurl(params)
		else:
			raise ValueError("Bad query string " + string(query_dict))

		# Build success response json, which will look like this:
		# {"id":1,"jsonrpc":"2.0","result":"OK"}
		# The "id" and "jsonrpc" value should match the incoming rpc
		# request, so we copy them out of the request query string.
		resp = {"id": query_dict['id'], "jsonrpc": query_dict['jsonrpc'], "results":"OK"}
		#print("resp=", str(resp))

		return str(resp)

