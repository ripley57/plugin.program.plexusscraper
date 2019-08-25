import xmltodict


class KodiSettings:
	def __init__(self, _file_path):
		self.file_path = _file_path
		self.data = xmltodict.parse(open(_file_path).read())


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

