""" PlexusScraper class. Hides lower-level business classes """

from plexusscraper.linkservice import LinkService

class PlexusScraper:

	@classmethod
	def extract_links_from_html(cls, html):
		return LinkService.extract_links_from_html(html)

