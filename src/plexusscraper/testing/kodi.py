""" Mock Kodi RPC handling """

import ast
import cgitb
cgitb.enable()
from urllib.parse import unquote 

from plexusscraper.config import get_config
from plexusscraper.kodi.settings import KodiSettingsXml


class MockKodiRPCHandler:

	def __init__(self):
		self.kodi_settings_xml = KodiSettingsXml(get_config()['kodi_settings_xml_path'])


	def __add_url(self, params):
		url_path = params['url_path']
		url_id = params['url_id']
		
		# Add url to settings.xml
		# NOTE: In the original version of Plexus Scraper, we only
		#	ever updated the settings.xml file using the Kodi API:
		#	xbmcaddon.Addon(id='program.plexusscraper').setSetting(setting_id,url_path)
		#	From now on, we are going to update the xml file ourself directly.
		#
	
		print("kodi mock rpc server: __addr_url: url_path=", url_path, " url_id=", url_id)
		self.kodi_settings_xml.add_setting('url_'+url_id, url_path)
		


	def handle_rpc(self, _path):
		path, query = _path.split('?')
	
		# Url-decode.
		query_decoded = unquote(query)

		# Example url-decoded query string:
		# request={"id":1,"jsonrpc":"2.0","method":"Addons.ExecuteAddon",
		# "params":{"addonid":"program.plexusscraper",
		# "params":{"url_path":"https://streamingsports.me/aston-villa-vs-everton-live-streaming/173081.html","mode":"addurl","url_id":"2"}}}
		#print("query_decoded =", query_decoded)

		# Remove prefix "request="
		if query_decoded.startswith("request="):
			query_decoded = query_decoded[8:]

		# Convert the json request into a dict.
		query_dict = ast.literal_eval(query_decoded)

		# Perform the appropriate action.
		params = query_dict['params']['params']
		mode = params['mode']
		if mode == "addurl":
			self.__add_url(params)
		else:
			raise ValueError("Bad query string " + string(query_dict))

		# Build a mock success response json:
		# {"id":1,"jsonrpc":"2.0","result":"OK"}
		# Note: The "id" and "jsonrpc" values should match the values in the
		# incoming rpc request, so we copy them into the response string.
		resp = {"id": query_dict['id'], "jsonrpc": query_dict['jsonrpc'], "results":"OK"}
		print("kodi mock rpc server: resp=", str(resp))

		return str(resp)

