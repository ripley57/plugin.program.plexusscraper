from plexusscraper.linkservice import LinkService

import os
import subprocess
import tempfile


class PlexusHelper:
	pass


class PlexusHelperOSMC(PlexusHelper):
	ACE_SUFFIX = '|1|/home/osmc/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png'
	SOP_SUFFIX = '|2|/home/osmc/.kodi/addons/program.plexus/resources/art/sopcast-menu-item.png'
	HISTORY_FILE_LOCATION_PI = '/home/osmc/.kodi/userdata/addon_data/program.plexus/history.txt'


class PlexusHelperOpenElec(PlexusHelper):
	ACE_SUFFIX = '|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png'
	SOP_SUFFIX = '|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg'
	HISTORY_FILE_LOCATION_PI = '/storage/.kodi/userdata/addon_data/program.plexus/history.txt'


class PlexusHelperFactory:
	@classmethod
	def createHelper(cls, kodi_type='openelec'):
		if kodi_type == 'osmc':
			return PlexusHelperOSMC()
		elif kodi_type == 'openelec':
			return PlexusHelperOpenElec()
		else:
			return PlexusHelperOpenElec()


class PlexusHistoryFile:

	SCP_TIMEOUT_SECS = 10

	def __init__(self):
		self.ace_list = []	# title,link, e.g. [('','acestream://...'),('MYNAME','acestream:/...'),...
		self.sop_list = []	# title,link, e.g. [('SOMENAME','sop://...'),('','sop://...'),...
		self.plexus_helper = PlexusHelperFactory.createHelper()

	def set_plexus_helper(self, kodi_type):
		self.plexus_helper = PlexusHelperFactory.createHelper(kodi_type)

	def get_ace_list(self):
 		return self.ace_list

	def get_sop_list(self):
		return self.sop_list

	@property
	def text(self):
		lines = self.__build_all_history_file_lines()
		return "\n".join(lines)


	def save_to_file(self, path):
		f = open(path, 'w')
		content = self.text
		f.write(content)
		f.close()


	def __add_missing_titles(self, items, prefix):
		""" Given a list of (title,link) types, add any missing title values """

		# Separate the tuples into w/wo title.
		w_title = [ v for v in items if v[0] ]		# original tuples
		wo_title = [ v[1] for v in items if not v[0] ]	# just the links

		# Sorting the links from the tuples w/o a title. Doing this
		# makes the final list deterministic which helps testing.
		wo_title.sort()

		# Create the missing titles, using the passed prefix, e.g. ACE_01, ACE_O2, ...
		titles = [ prefix+str(i+1).zfill(2) for i in range(len(wo_title)) ]

		# Create the final sorted list of tuples.
		final_list = list(zip(titles, wo_title))
		final_list = final_list + w_title
		final_list.sort()
		return final_list
		

	def __build_all_history_file_lines(self):
		""" Build list of lines to go in the plexus history file """

		# Generate and add any misisng link titles.
		ace_list = self.__add_missing_titles(self.ace_list, "ACE_")
		sop_list = self.__add_missing_titles(self.sop_list, "SOP_")

		lines_ace = [ self.__build_ace_history_line(t, l) for t, l in ace_list]
		lines_sop = [ self.__build_sop_history_line(t, l) for t, l in sop_list]

		return lines_ace + lines_sop


	def __build_ace_history_line(self, title, link):
		return title + "|" + link + self.plexus_helper.ACE_SUFFIX


	def __build_sop_history_line(self, title, link):
		return title + "|" + link + self.plexus_helper.SOP_SUFFIX


	def __create_link_tuple(self, x):
		if isinstance(x, tuple):
			title = x[0]
			link = x[1]
		else:
			title = ''
			link = x
		return (title, link)


	def add_urls(self, urls):
		for x in urls:
			(title, link) = self.__create_link_tuple(x)
			if LinkService.is_acestream_link(link):
				self.ace_list.append((title, link))
			elif LinkService.is_sopcast_link(link):
				self.sop_list.append((title, link))

	def add_links_from_html(self, html):
		links = LinkService.extract_links_from_html(html)
		self.add_urls(links)

	
	def add_links_from_string(self, s):
		links = LinkService.extract_links_from_string(s)
		self.add_urls(links)
		pass

	
	def add_links_from_file(self, path):
		links = LinkService.extract_links_from_file(path)
		self.add_urls(links)

	
	def add_links_from_url(self, url):
		links = LinkService.extract_links_from_url(url)
		self.add_urls(links)


	def _build_scp_cmd(self, new_history_file_path, ip):
		return ['scp', '-v', '-o', 'ConnectTimeout=' + str(PlexusHistoryFile.SCP_TIMEOUT_SECS), new_history_file_path, 'root@' + ip + ':' + self.plexus_helper.HISTORY_FILE_LOCATION_PI]


	def _create_tmp_history_file(self):
		fd, path = tempfile.mkstemp(suffix='.txt', prefix='history_', text=True)
		with os.fdopen(fd, 'w') as f:
			f.write(self.text)
		return path


	def install_history_file_using_scp(self, ip):
		tmp_history_file = self._create_tmp_history_file()
		self._install_history_file_using_scp(self._build_scp_cmd(tmp_history_file, ip))
		try:
			os.unlink(tmp_history_file)
		except:
			pass
	

	def _install_history_file_using_scp(self, scp_cmd):
		print('\n' + ' '.join(scp_cmd) + ' ...\n')
		x = ' '.join(scp_cmd)
		subprocess.call(x, shell=True)

