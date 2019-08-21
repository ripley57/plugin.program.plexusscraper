""" Unit tests for the PlexusHistoryFile class.
"""

import unittest

from plexusscraper.plexushistoryfile import PlexusHistoryFile
from plexusscraper.scraper import Scraper


class TestPlexusHistoryFile(unittest.TestCase):

	def test_add_acestream_urls(self):
		urls = ['acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9',
			'acestream://78637dab85e7948057165ad0c80b3db475dd9c3d',
			'acestream://c389afdd68246467538cec05eace0ca6410e4bb4']
		expected_content = """\
ACE_01|acestream://78637dab85e7948057165ad0c80b3db475dd9c3d|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
ACE_02|acestream://c389afdd68246467538cec05eace0ca6410e4bb4|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
ACE_03|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png\
"""
		history_file = PlexusHistoryFile()
		history_file.add_acestream_urls(urls)
		assert(history_file.text == expected_content)


	def test_add_sopcast_urls(self):
		urls = ['sop://broker.sopcast.com:3912/264750',
			'sop://broker.sopcast.com:3912/265589',
			'sop://broker.sopcast.com:3912/264740']
		expected_content = """\
SOP_01|sop://broker.sopcast.com:3912/264740|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
SOP_02|sop://broker.sopcast.com:3912/264750|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
SOP_03|sop://broker.sopcast.com:3912/265589|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg\
"""
		history_file = PlexusHistoryFile()
		history_file.add_sopcast_urls(urls)
		assert(history_file.text == expected_content)


	def test_add_raw_urls(self):
		raw_urls = 'SOP_EX_1|sop://broker.sopcast.com:3912/26475,sop://broker.sopcast.com:3912/265589,ACE 1|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9,acestream://c389afdd68246467538cec05eace0ca6410e4bb4'
		expected_content = """\
ACE 1|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
ACE_01|acestream://c389afdd68246467538cec05eace0ca6410e4bb4|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
SOP_01|sop://broker.sopcast.com:3912/265589|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
SOP_EX_1|sop://broker.sopcast.com:3912/26475|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg\
"""
		history_file = PlexusHistoryFile()
		history_file.add_raw_urls(raw_urls)
		assert(history_file.text == expected_content)

