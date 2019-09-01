import os


# /storage/.kodi/userdata/addon_data/program.plexusscraper/settings.xml

if os.environ.get('TESTING_IN_PROGRESS'):
	config = { 'kodi_settings_xml_path' : '/home/jcdc/settings.xml' }
else:
	config = { 'kodi_settings_xml_path' : '/home/jcdc/settings.xml' }

def get_config():
	return config

