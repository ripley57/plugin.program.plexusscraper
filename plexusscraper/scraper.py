import os
import re
import bs4


class Scraper:
	def __init__(self):
		self.acestream_links = set()
		self.sopcast_links = set()

	def get_acestream_links(self):
		""" Return list of stored acestream links """
		return list(self.acestream_links)

	def get_sopcast_links(self):
		""" Return list of stored sopcast links """
		return list(self.sopcast_links)

	def add_raw_links(self, links):
		""" Validate the syntax of the passed delimited string of raw links, then store them 
		Returns:
			Dict of count.
		"""
		counts = {"acestream":{"valid":0,"new":0}, "sopcast":{"valid":0,"new":0}}

		# Delimiter space or comma.
		pattern = re.compile(r" |,")
		ll = pattern.split(links)

		for l in ll:
			if self.__class__.is_acestream_link(l):
				counts['acestream']['valid'] += 1
				if l not in self.acestream_links:
					counts['acestream']['new'] +=1
					self.acestream_links.add(l)
			elif self.__class__.is_sopcast_link(l):
				counts['sopcast']['valid'] += 1
				if l not in self.sopcast_links:
					counts['sopcast']['new'] += 1
					self.sopcast_links.add(l)
			else:
				raise ValueError("Bad raw link - {}".format(l))
		return counts

	@classmethod
	def is_acestream_link(cls, link):
		""" Return True is passed link is a syntax-valid acestream link; return False otherwise """
		_regexp_acestream = re.compile('acestream://[abcdef0-9]+$')
		if _regexp_acestream.search(link):
			return True
		return False

	@classmethod
	def is_sopcast_link(cls, link):
		""" Return True is passed link is a syntax-valid sopcast link; return False otherwise """
		_regexp_sopcast = re.compile('^sop://broker.sopcast.com:[0-9]+/[0-9]+$')
		if _regexp_sopcast.search(link):
			return True
		return False

	@classmethod
	def extract_links_from_file(cls, file_path, extract_acestream=True, extract_sopcast=True):
		""" Extract acestream and/or sopcast links from the specified file """
		print("JCDC: os.getcwd()={}".format(os.getcwd()))
		f = open(file_path, 'r')
		text = f.read()
		f.close()
		return Scraper.extract_links_from_text(text)

	@classmethod
	def extract_links_from_text(cls, text):
		bs = bs4.BeautifulSoup(text, "html.parser")
		# Get all <a> elements.
		a_list = bs("a")
		acestream_list = [ x.get('href') for x in a_list if x.get('href') and Scraper.is_acestream_link(x.get('href')) ]
		sopcast_list = [ x.get('href') for x in a_list if x.get('href') and Scraper.is_sopcast_link(x.get('href')) ]
		return {'acestream': acestream_list, 'sopcast': sopcast_list}

