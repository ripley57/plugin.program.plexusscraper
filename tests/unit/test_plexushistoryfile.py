""" Unit tests for the PlexusHistoryFile class. """

import pytest
from pytest_mock import mocker 

from plexusscraper.plexushistoryfile import PlexusHistoryFile
from plexusscraper.linkservice import LinkService


class TestPlexusHistoryFile():

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
		history_file.add_urls(urls)
		self.assertEqual(history_file.text, expected_content, 'acestream urls not handled correctly')


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
		history_file.add_urls(urls)
		self.assertEqual(history_file.text, expected_content, 'sopcast urls not handled correctly')


	def test_add_raw_urls(self):
		raw_urls = 'SOP_EX_1|sop://broker.sopcast.com:3912/26475,sop://broker.sopcast.com:3912/265589,ACE 1|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9,acestream://c389afdd68246467538cec05eace0ca6410e4bb4'
		expected_content = """\
ACE 1|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
ACE_01|acestream://c389afdd68246467538cec05eace0ca6410e4bb4|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
SOP_01|sop://broker.sopcast.com:3912/265589|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
SOP_EX_1|sop://broker.sopcast.com:3912/26475|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg\
"""
		history_file = PlexusHistoryFile()
		links = LinkService.extract_links_from_string(raw_urls)
		history_file.add_urls(links)
		self.assertEqual(history_file.text, expected_content, 'raw acestream or sopcast urls not handled correctly')


	def test_install_history_file_using_scp(self, mocker):
		tmp_file = '/tmp/history_123456.txt'

		# Mock PlexusHistoryFile._create_tmp_history_file()
		mocker.patch.object(PlexusHistoryFile, '_create_tmp_history_file')
		PlexusHistoryFile._create_tmp_history_file.return_value = tmp_file
		
		# Mock PlexusHistoryFile._install_history_file_using_scp()
		mocker.patch.object(PlexusHistoryFile, '_install_history_file_using_scp')

		ip = '192.168.0.13'
		history_file = PlexusHistoryFile()
		history_file.install_history_file_using_scp('192.168.0.13')
		expected_cmd = ['scp', '/tmp/history_123456.txt', 'root@192.168.0.13:/storage/.kodi/userdata/addon_data/program.plexus/history.txt']

		PlexusHistoryFile._install_history_file_using_scp.assert_called_with(expected_cmd)

