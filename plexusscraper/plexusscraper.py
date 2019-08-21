""" PlexusScraper class. Hides lower-level business classes """

from plexusscraper.scraper import Scraper

class PlexusScraper:

	@classmethod
	def extract_links_from_html(cls, html):
		scraper = Scraper()
		return scraper.extract_links_from_html(html)

