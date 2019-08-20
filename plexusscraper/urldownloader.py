import requests

class URLDownloader:

	def __init__(self):
		pass

	@classmethod
	def download(cls, url_path):
		""" Download url and return content as a text string """
		response = requests.get(url_path)
		return (response.status_code, response.text)

