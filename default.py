""" Plexus Scraper (c) March 2018 JeremyC

    The is a Kodi Program addon to scrape acestream (and sopcast)
    urls from a web page. Currently up to 5 different pages to be
    scraped can be saved in the settings page. It is also possible
    to save raw acestream links, including a leading link name.
    The purpose of the plugin is to generate a Plexus "history.txt"
    file, which is used by the official Plexus addon. This addon
    effectively automates the generation of a Plexus "history.txt" 
    file.

    This addon directory needs to be installed here:
    /storage/.kodi/addons/plugin.program.plexusscraper

    o Kodi GUI tutorial: https://kodi.wiki/view/GUI_tutorial
    o Kodi color chart: https://forum.kodi.tv/showthread.php?tid=210837

    o To add a url to the list via JSON-RPC (Note: The url_id value is the settings.xml slot being filled).
    http://192.168.1.229/jsonrpc?request={"id": 1, "jsonrpc":"2.0", "method": "Addons.ExecuteAddon", "params": { "addonid": "program.plexusscraper", "params": {"url_path": "http://rptest.html", "mode": "addurl", "url_id": "3"}}}

    o Example using curl.exe from Windows (download pre-built curl.exe from: https://curl.haxx.se/dlwiz/?type=bin):
    curl.exe --header "Content-Type: application/json" --data-binary "{ \"id\":1, \"jsonrpc\":\"2.0\", \"method\":\"Addons.ExecuteAddon\", \"params\":{ \"addonid\":\"program.plexusscraper\", \"params\":{ \"url_path\": \"http://rptest.html\", \"mode\":\"addurl\", \"url_id\":\"3\" }}}" http://192.168.1.229/jsonrpc

    13th May 2018
"""

import json
import os
import re
import sys
import urllib
import urllib2
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import ssl
import subprocess

from shutil import copyfile

# My own modules. 
from resources.Utils import AcestreamHelper
from resources.Utils.DebugHelper import debug


__base_url__ 		= sys.argv[0]
__addon_handle__ 	= int(sys.argv[1])
__args__		= urlparse.parse_qs(sys.argv[2][1:])

# This addon details.
__addonid__ 		= 'program.plexusscraper'
__addon__ 		= xbmcaddon.Addon(id=__addonid__)
__addonpath__ 		= __addon__.getAddonInfo('path').decode('utf-8')
__addonuserdatapath__	= xbmc.translatePath(__addon__.getAddonInfo('profile'))
#debug("addonpath",__addonpath__)
#debug("addonuserdatapath",__addonuserdatapath__)

# Plexus addon details.
__plexus_addonid__     		= 'program.plexus'
__plexus_addon__             	= xbmcaddon.Addon(id=__plexus_addonid__)
__plexus_addonuserdatapath__ 	= xbmc.translatePath(__plexus_addon__.getAddonInfo('profile'))
#debug("plexus addonuserdatapath", __plexus_addonuserdatapath__)

# Location of our new locally built Plexus history.txt file.
__built_history_file__ 	= os.path.join('storage/.kodi/temp/', 'history.txt')

# Location of our test.html file, useful for testing the addon.
# I have manually added this url to the last entry in settings.xml.
__test_html__ = 'file:///storage/.kodi/addons/plugin.program.plexusscraper/resources/test.html'

# Location of the live settings.xml file of this addon.
# This contains all urls we can select from to be scraped, 
# plus any raw acestream links, so we can handle these too.
__addonsettingsxmlpath__= 'file:///storage/.kodi/userdata/addon_data/program.plexusscraper/settings.xml'


def build_addon_url(query):
	return __base_url__ + '?' + urllib.urlencode(query)


def add_text_entry(str):
	li = xbmcgui.ListItem(str, iconImage='DefaultVideo.png')
	url = build_addon_url({'mode': 'debug', 'str': str})
	xbmcplugin.addDirectoryItem(handle=__addon_handle__, url=url, listitem=li, isFolder=False)


def add_url_choice(url_number):
	url_path = __addon__.getSetting(url_number)
	addon_li = xbmcgui.ListItem("" + url_path, iconImage='DefaultVideo.png')
	addon_url = build_addon_url({'mode': 'scrape', 'url_path': url_path})
	xbmcplugin.addDirectoryItem(handle=__addon_handle__, url=addon_url, listitem=addon_li, isFolder=False)


def fprintf(stream, format_spec, *args):
	stream.write(format_spec % args)


def add_acestream_entries_to_history_file(output_stream, html):
	count=0
	for match in re.finditer('"(acestream://[^"]*)"', html, re.S):
		count = count +1
		text = match.group(1)
        	fprintf(output_stream,"ACE_LINK_%d|%s|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png\n", count, text)
	return count


def add_sopcast_entries_to_history_file(output_stream, html):
	count=0
	for match in re.finditer('"(sop://[^"]*)"', html, re.S):
        	text = match.group(1)
        	count = count + 1
        	fprintf(output_stream,"SOP_LINK_%d|%s|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg\n", count, text)
	return count


def add_raw_acestream_entries_to_history_file(output_stream):
	count = 0
	proc = subprocess.Popen(["/storage/.kodi/addons/plugin.program.plexusscraper/acestreamsfromxml.php"], stdout=subprocess.PIPE)
	links = proc.communicate()[0]
	for match in re.finditer('(.*)\|(acestream://.*\n)', links):
        	count = count + 1
        	name = match.group(1).rstrip()
        	link = match.group(2).rstrip()
		fprintf(output_stream,"%s|%s|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png\n", name, link)
   	return count


def add_raw_sopcast_entries_to_history_file(output_stream):
	count = 0
	proc = subprocess.Popen(["/storage/.kodi/addons/plugin.program.plexusscraper/acestreamsfromxml.php"], stdout=subprocess.PIPE)
	links = proc.communicate()[0]
	for match in re.finditer('(.*)\|(sop://.*\n)', links):
        	count = count + 1
        	name = match.group(1).rstrip()
        	link = match.group(2).rstrip()
        	fprintf(output_stream,"%s|%s|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg\n", name, link)
   	return count


def geturl_using_curl(url):
	proc = subprocess.Popen(["/usr/bin/curl", url], stdout=subprocess.PIPE)
	html = proc.communicate()[0]
	return html

	
def is_url(arg):
	rtn = False
	matchObj = re.match('^http[s]://', arg)
	if matchObj:
		rtn = True
	#debug("is_url()", "arg=" + arg + ", rtn=" + str(rtn))
	return rtn


def is_html(arg):
	rtn = False
	matchObj = re.match('.*\.(html|htm)', arg)
	if matchObj:
		rtn = True
	#debug("is_html()", "arg=" + arg + ", rtn=" + str(rtn))
	return rtn
	
	
def create_plexus_history_file(url_path):
	count_acestream = 0
	count_sopcast = 0
			
	if is_url(url_path):
		# Download the single specified html to scrape for acestream links.
		#debug("About to download html content from:","url_path="+url_path)
		try:
			# Older Python version, such as 2.7.3, do not support TLS
			# (see https://github.com/twoolie/NBT/issues/78). If we
			# detect that ssl.create_default_context() is not found, 
			# use curl as a fallback to get the html.
			try:
				ctx = ssl.create_default_context()
				ctx.check_hostname = False
				ctx.verify_mode = ssl.CERT_NONE
				response = urllib2.urlopen(url_path, context=ctx)
				html = response.read()
				response.close()
			
			except AttributeError:
				# This is a legacy Python such as 2.7.3 that does not recognise ssl.create_default_context().
				# In this situation we will use curl.exe out-of-process.
				html = geturl_using_curl(url_path)
				
			#debug("Size of html downloaded:", str(len(html)))
			
			# Create locally built history file.
			ofh = open(__built_history_file__,'w')
			count_acestream = add_acestream_entries_to_history_file(ofh, html)
			count_sopcast = add_sopcast_entries_to_history_file(ofh, html)
			ofh.close()

		except Exception, e:
			xbmcgui.Dialog().ok("ERROR: Failed to download url", "URL: " + url_path + "\n" + str(e))
			return 0, 0

	elif is_html(url_path):
		# Read local html file into a string.
		html_file = open(url_path, 'r')
		html = html_file.read()
		html_file.close()
		#debug("Size of html file:", str(len(html)))

		# Create locally built history file 
		ofh = open(__built_history_file__,'w')
		count_acestream = add_acestream_entries_to_history_file(ofh, html)
		count_sopcast = add_sopcast_entries_to_history_file(ofh, html)
		ofh.close()

	elif SopcastHelper.is_raw_sopcast(url_path):
		# The user clicked on a raw sopcast link - we will
		# add only the raw sopcast links to the history file.
		ofh = open(__built_history_file__,'w')
		count_sopcast = add_raw_sopcast_entries_to_history_file(ofh)
		ofh.close()
			
	elif AcestreamHelper.is_raw_acestream(url_path):
		# The user clicked on a raw acestream link - we will
		# add only the raw acestream links to the history file.
		ofh = open(__built_history_file__,'w')
		count_acestream = add_raw_acestream_entries_to_history_file(ofh)
		count_sopcast= 0
		ofh.close()

	# Return count of extracted acestream and sopcast links.
	#debug("count_acestream","count_acestream=" + str(count_acestream))
	#debug("count_sopcast","count_sopcast=" + str(count_sopcast))
	return count_acestream, count_sopcast	
	

def add_settings_shortcut():
	addon_li = xbmcgui.ListItem('[B][COLOR chartreuse]'+'Settings page'+'[/COLOR][/B]', iconImage='DefaultVideo.png')
	addon_url = build_addon_url({'mode': 'settings'})
	xbmcplugin.addDirectoryItem(handle=__addon_handle__, url=addon_url, listitem=addon_li, isFolder=False)
    

def add_menu():
	add_text_entry('[B][COLOR fuchsia]'+'Use the Settings page to edit the URLs below.'+'[/COLOR][/B]')
	add_settings_shortcut()
	add_text_entry('')
	add_url_choice('url_1')
	add_url_choice('url_2')
	add_url_choice('url_3')
	add_url_choice('url_4')
	add_text_entry('')
	add_text_entry('[B][COLOR gold]'+'Test URL:'+'[/COLOR][/B]')
	add_url_choice('url_5')
	xbmcplugin.endOfDirectory(__addon_handle__)


def copy_history_file_to_plexus():
	src = __built_history_file__
	dst = os.path.join(__plexus_addonuserdatapath__, 'history.txt')
	#debug("copy_history_file_to_plexus()","src="+src+", dst="+dst)
	copyfile(src, dst)


# Add a url path (obtained from a JSON-RPC call) to the addon 
# configuration page, filling-in the specified url slot number.
# Note: This will create a settings.xml file under directory:
# /storage/.kodi/userdata/addon_data/program.plexusscraper/
# This file is created by the "setSetting()" call and it seems
# that this file then overrides the default settings.xml file
# found in the main addon directory:
# /storage/.kodi/addons/plugin.program.plexusscraper/resources/
def add_url_path(url_path, url_id):
	print("JCDC: url_path="+url_path+", url_id="+url_id)
	setting_id = "url_" + url_id
	xbmcaddon.Addon(id='program.plexusscraper').setSetting(setting_id,url_path)
    

mode = __args__.get('mode', 'none')
#print("JCDC: mode: " + mode)

if mode=='none':
    add_menu()

elif mode[0]=='scrape':
    # User has clicked on a url to process.
    url_path = __args__['url_path'][0]

    (acestream_links, sopcast_links) = create_plexus_history_file(url_path)
    if (acestream_links > 0 or sopcast_links > 0):
        try:
	    copy_history_file_to_plexus()   
            xbmcgui.Dialog().ok("Successfully copied history.txt to Plexus :-)",
                                "Acestream links: "+str(acestream_links)+"\n"+"Sopcast links:"+str(sopcast_links))
        except IOError, e:
            xbmcgui.Dialog().ok("ERROR: Failed to copy history.txt to Plexus :-(", str(e))

elif mode[0]=='settings':
    # Display the addon settings page - so a user can manually edit the URLs there.
    xbmcaddon.Addon(id='program.plexusscraper').openSettings()

elif mode[0]=='addurl':
    url_path = __args__['url_path'][0]
    url_id = __args__['url_id'][0]
    print("JCDC: addurl() url_path=" + url_path)
    add_url_path(url_path,url_id)

