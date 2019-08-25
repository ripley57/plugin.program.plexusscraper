import pytest

from plexusscraper.kodi.settings import KodiSettings


@pytest.fixture()
def sample_settings_xml_file(tmpdir):
	xml_file = tmpdir.join('settings.xml')
	#print("file path:", str(xml_file))
	
	xml = """
<settings>
    <setting id="url_1" value="https://streamingsports.me/aston-villa-vs-everton-live-streaming/173081.html" />
    <setting id="url_2" value="https://streamingsports.me/aston-villa-vs-everton-live-streaming/173081.html" />
    <setting id="url_3" value="/storage/chel.html" />
    <setting id="url_4" value="/storage/wolves.html" />
    <setting id="url_5" value="acestream://ea1b551f853a6b2caa23eba805c5d093cba8754d" />
</settings>
"""
	xml_file.write(xml)
	return xml_file


def test_read_sample_settings_xml(sample_settings_xml_file):
	settings = KodiSettings(str(sample_settings_xml_file))
	settings_dict = settings.get_settings_dict()
	assert(len(settings_dict.keys()) == 5)
	assert(settings.get_setting('url_4') == "/storage/wolves.html")

