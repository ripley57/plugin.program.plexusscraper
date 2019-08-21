import os
import re
import bs4


class LinkService:
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
	def extract_links_from_string(self, s):
		""" Extract acestream or sopcast links from a passed string.
		The input string can contain multiple links, each with an optional title. 
		Example:
                SOP_EX_1|sop://broker.sopcast.com:3912/26475,sop://broker.sopcast.com:3912/265589,ACE 1|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9
		"""
		ace_list  = []
		sop_list  = []
		for x in s.split(","):
			if x.find("|") > 0:
				title = x.split("|")[0]
				link = x.split("|")[1]
			else:
				title = ''
				link = x
			if LinkService.is_acestream_link(link):
				ace_list.append((title, link))
			elif LinkService.is_sopcast_link(link):
				sop_list.append((title, link))
			else:
				raise ValueError("Bad raw link - {}".format(x))
		return ace_list + sop_list


	@classmethod
	def extract_links_from_file(cls, file_path, extract_acestream=True, extract_sopcast=True):
		""" Extract acestream and/or sopcast links from the specified file """
		print("JCDC: os.getcwd()={}".format(os.getcwd()))
		f = open(file_path, 'r')
		text = f.read()
		f.close()
		return LinkService.extract_links_from_html(text)


	@classmethod
	def extract_links_from_html(cls, text):
		bs = bs4.BeautifulSoup(text, "html.parser")
		# Get all <a> elements.
		a_list = bs("a")
		acestream_list = [ x.get('href') for x in a_list if x.get('href') and LinkService.is_acestream_link(x.get('href')) ]
		sopcast_list = [ x.get('href') for x in a_list if x.get('href') and LinkService.is_sopcast_link(x.get('href')) ]
		return acestream_list + sopcast_list

