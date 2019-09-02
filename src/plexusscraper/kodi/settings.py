import xmltodict


class KodiSettingsXml:

	def __init__(self, _file_path):
		self.file_path = _file_path
		self.reload_xml()


	def reload_xml(self):
		self.data = xmltodict.parse(open(self.file_path).read(), force_list={'setting'})


	def get_settings_dict(self):
		settings_dict = {}
		for s_dict in self.data['settings']['setting']:
			s_key = s_dict['@id']
			s_val = s_dict['@value']
			settings_dict.update({s_key: s_val})
		return settings_dict


	def get_setting(self, id):
		settings_dict = self.get_settings_dict()
		return settings_dict[id]


	def add_setting(self, id, url):
		old_dict = self.get_settings_dict()
		new_list = []
		for s_key, s_val in old_dict.items():
			if s_key == id:
				s_val = url
			new_list.append({'@id': s_key, '@value': s_val})
		new_dict = {'settings': {'setting': new_list}}
		with open(self.file_path, 'w') as file:
			file.write(xmltodict.unparse(new_dict, pretty=True))
		self.reload_xml()


	@classmethod
	def create(cls, file_path):
		""" Create an empty settings.xml file """
		new_dict = { 'settings'  : { 'setting' : [ 	{ '@id' : 'url_1', '@value' : '' },
								{ '@id' : 'url_2', '@value' : '' },
								{ '@id' : 'url_3', '@value' : '' },
								{ '@id' : 'url_4', '@value' : '' },
								{ '@id' : 'url_5', '@value' : '' }	]	}	}
		with open(file_path, 'w') as file:
			file.write(xmltodict.unparse(new_dict, pretty=True))

