""" Plexus Scraper CLI """

import click
import ipaddr
import re

from plexusscraper.plexushistoryfile import PlexusHistoryFile


class PS_IPAddress(click.ParamType):
    def __init__(self):
        self.name = 'ip'

    def convert(self, value, param, ctx):
        try:
            found = ipaddr.IPAddress(value)
        except:
            self.fail(f'{value} is not a valid ip address', param, ctx)
        return value
        

class PS_Url(click.ParamType):
    def __init__(self):
        self.name = 'url'

    def convert(self, value, param, ctx):
        found = re.match(r'^https?://', value)
        if not found:
            self.fail(f'{value} is not a valid url', param, ctx)
        return value


class PS_Sopcast(click.ParamType):
    def __init__(self):
        self.name = 'sopcast'

    def convert(self, value, param, ctx):
        found = re.match(r'sop://', value)
        if not found:
            self.fail(f'{value} is not a valid sopcast url', param, ctx)
        return value


class PS_Acestream(click.ParamType):
    def __init__(self):
        self.name = 'acestream'

    def convert(self, value, param, ctx):
        found = re.match(r'acestream://', value)
        if not found:
            self.fail(f'{value} is not a valid acestream url', param, ctx)
        return value


@click.group()
def main():
    """
CLI to the PlexusScraper Python package.\n 
"""
    pass

@main.command()
@click.option('--url', '-u', 		type=PS_Url(), 		multiple=True, help='website URL')
@click.option('--html-file', '-f', 	type=click.Path(), 	multiple=True, help='path to a local html file')
@click.option('--sopcast', '-s', 	type=PS_Sopcast(), 	multiple=True, help='sopcast url')
@click.option('--acestream', '-a', 	type=PS_Acestream(), 	multiple=True, help='acestream url')
@click.option('--history-file', is_flag=True, help='Generate Plexus history.txt content (to stdout)')
@click.option('--install-ip', '-i',	type=PS_IPAddress(),	multiple=False, help='scp history.txt file to ip address')
@click.option('--osmc', is_flag=True, help='Target Kodi system is OSMC')
@click.option('--openelec', is_flag=True, help='Target Kodi system is OpenElec')
def scrape(url, html_file, sopcast, acestream, history_file, install_ip, osmc, openelec):
    """
    Scrape sopcast and acestream urls from various sources. 
    If requested, display the scraped urls in Plexus history.txt format; otherwise display them as raw links.
    

    Example:\n
        
    python ps_cli.py scrape --url http://someurl.com --html-file /storage/file.html --acestream acestream://78637dab85e7948057165ad0c80b3db475dd9c3d --sopcast sop://broker.sopcast.com:3912/265589 --history-file --ip 192.168.0.13
    """
    ps = PlexusHistoryFile()

    for u in url:
        ps.add_links_from_url(u)

    for h in html_file:
        ps.add_links_from_file(h)

    for s in sopcast:
        ps.add_links_from_string(s)

    for a in acestream:
        ps.add_links_from_string(a)

    if history_file:
        if install_ip:
            ps.set_plexus_helper(get_kodi_type_str(osmc, openelec))
            ps.install_history_file_using_scp(install_ip)
        else:
            print(ps.text)
    else:
        ace_list = ps.get_ace_list()
        count = len(ace_list)
        print("\nAcestream: ", count)
        if count > 0:
            for title, link in ace_list:
                print(link)

        sop_list = ps.get_sop_list() 
        count = len(sop_list)
        print("\nSopcast: ", count)
        if count > 0:
            for title,link in sop_list:
                print(link)

        if count > 0:
            print("")


def get_kodi_type_str(osmc, openelec):
	kodi_type = 'openelec'
	if osmc:
		kodi_type = 'osmc'
	elif openelec:
		kodi_type = 'openelec'
	return kodi_type


if __name__ == "__main__":
    main()

