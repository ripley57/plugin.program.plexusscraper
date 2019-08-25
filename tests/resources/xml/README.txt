Sample real-life Kodi addon settings.xml files from file:///storage/.kodi/userdata/addon_data/program.plexusscraper/settings.xml

The settings.xml file is updated by this addon by the following Kodi/XMBC call:
	xbmcaddon.Addon(id='program.plexusscraper').setSetting(setting_id,url_path)

See docs here https://codedocs.xyz/AlwinEsch/kodi/group__python__xbmcaddon.html
(This find was found here: https://kodi.wiki/index.php?title=Xbmcaddon_module)

When we first install our addon, we provide a starting settings.xml file, located
here with the addon's program files:
	/storage/.kodi/addons/plugin.program.plexusscraper/resources/
However, when the addon is used, the xml file is copied and replaced with a 'live' 
version located here:
	/storage/.kodi/userdata/addon_data/program.plexusscraper/

