""" Test the command-line interface (ps_cli.py) """

from click.testing import CliRunner

import pytest

import plexusscraper.ps_cli


# Fixture called implicitly by some of the tests below.
def some_links_without_titles(dummy_param):
	""" Note that we have a dummy parameter. This is so that we can replace
	calls to LinkServer.extra_links_html() with it using a mock. We get an 
	error if we try to do this without the declaration of the paramter. 
	"""
	return (
		'acestream://8d9094e60cac92486cd23d1311a4ef1261a337ed',
		'acestream://8d9094e60cac92486cd23d1311a4ef1261a337ee',
		'acestream://8d9094e60cac92486cd23d1311a4ef1261a337ef',
		'sop://broker.sopcast.com:3912/264750',
		'sop://broker.sopcast.com:3912/264751',
		'sop://broker.sopcast.com:3912/264752',
	)


def test_help():
	runner = CliRunner()
	result = runner.invoke(plexusscraper.ps_cli.scrape, ['--help'])
	expected_result = """\
Usage: scrape [OPTIONS]

  Scrape sopcast and acestream urls from various sources.  If requested,
  display the scraped urls in Plexus history.txt format; otherwise display
  them as raw links.

  Example:

       python ps_cli.py scrape --url http://someurl.com --html-file
      /storage/file.html --acestream
      acestream://78637dab85e7948057165ad0c80b3db475dd9c3d --sopcast
      sop://broker.sopcast.com:3912/265589 --history-file --ip 192.168.0.13

Options:
  -u, --url URL              website URL
  -f, --html-file PATH       path to a local html file
  -s, --sopcast SOPCAST      sopcast url
  -a, --acestream ACESTREAM  acestream url
  --history-file             Generate Plexus history.txt content (to stdout)
  -i, --install-ip IP        scp history.txt file to ip address
  --osmc                     Target Kodi system is OSMC
  --openelec                 Target Kodi system is OpenElec
  --help                     Show this message and exit.
"""
	assert result.output == expected_result


def test_url_args(mocker):
	# Mock the call to LinkService.extract_links_from_html() from plexushistoryfile.py
	mocker.patch.object(plexusscraper.plexushistoryfile.LinkService, 'extract_links_from_html', new=some_links_without_titles)
	runner = CliRunner()
	result = runner.invoke(plexusscraper.ps_cli.scrape, ['--url', 'http://somedomain.com'])
	expected_result = """
Acestream:  3
acestream://8d9094e60cac92486cd23d1311a4ef1261a337ed
acestream://8d9094e60cac92486cd23d1311a4ef1261a337ee
acestream://8d9094e60cac92486cd23d1311a4ef1261a337ef

Sopcast:  3
sop://broker.sopcast.com:3912/264750
sop://broker.sopcast.com:3912/264751
sop://broker.sopcast.com:3912/264752

"""
	assert result.output == expected_result


def test_local_file_args(mocker):
	# Mock the call to LinkService.extract_links_from_file() from plexushistoryfile.py
	mocker.patch.object(plexusscraper.plexushistoryfile.LinkService, 'extract_links_from_file', new=some_links_without_titles)
	runner = CliRunner()
	result = runner.invoke(plexusscraper.ps_cli.scrape, ['--html-file', '/tmp/somefile.html'])
	expected_result = """
Acestream:  3
acestream://8d9094e60cac92486cd23d1311a4ef1261a337ed
acestream://8d9094e60cac92486cd23d1311a4ef1261a337ee
acestream://8d9094e60cac92486cd23d1311a4ef1261a337ef

Sopcast:  3
sop://broker.sopcast.com:3912/264750
sop://broker.sopcast.com:3912/264751
sop://broker.sopcast.com:3912/264752

"""
	assert result.output == expected_result 


def test_acestream_args():
	runner = CliRunner()
	result = runner.invoke(plexusscraper.ps_cli.scrape, [	'--acestream', 'acestream://8d9094e60cac92486cd23d1311a4ef1261a337ed',
								'--acestream', 'acestream://8d9094e60cac92486cd23d1311a4ef1261a337ee',
								'--acestream', 'acestream://8d9094e60cac92486cd23d1311a4ef1261a337ef',	])
	expected_result = """
Acestream:  3
acestream://8d9094e60cac92486cd23d1311a4ef1261a337ed
acestream://8d9094e60cac92486cd23d1311a4ef1261a337ee
acestream://8d9094e60cac92486cd23d1311a4ef1261a337ef

Sopcast:  0
"""
	assert result.output == expected_result


def test_sopcast_args(mocker):
	runner = CliRunner()
	result = runner.invoke(plexusscraper.ps_cli.scrape, [	'--sopcast', 'sop://broker.sopcast.com:3912/264750',
								'--sopcast', 'sop://broker.sopcast.com:3912/264751',
								'--sopcast', 'sop://broker.sopcast.com:3912/264752',	])
	expected_result = """
Acestream:  0

Sopcast:  3
sop://broker.sopcast.com:3912/264750
sop://broker.sopcast.com:3912/264751
sop://broker.sopcast.com:3912/264752

"""
	assert result.output == expected_result


def test_history_file(mocker):
	runner = CliRunner()
	result = runner.invoke(plexusscraper.ps_cli.scrape, [	'--sopcast', 'sop://broker.sopcast.com:3912/264750',
								'--acestream', 'acestream://8d9094e60cac92486cd23d1311a4ef1261a337ed',
								'--history-file'	])
	expected_result = """ACE_01|acestream://8d9094e60cac92486cd23d1311a4ef1261a337ed|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
SOP_01|sop://broker.sopcast.com:3912/264750|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
"""
	assert result.output == expected_result

