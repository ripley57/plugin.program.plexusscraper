from behave import given, when, then

from plexusscraper.linkservice import LinkService
from plexusscraper.plexushistoryfile import PlexusHistoryFile


@given(u'the following html')
def step_impl(context):
	context.html = context.text


@given(u'the following string of raw urls')
def step_impl(context):
	context.raw_urls = context.text


@when(u'I generate a plexus history file from the html')
def step_impl(context):
	links = LinkService.extract_links_from_html(context.html)
	context.history_file = PlexusHistoryFile()
	context.history_file.add_urls(links)


@when(u'I generate a plexus history file from a string of raw urls')
def step_impl(context):
	links = LinkService.extract_links_from_string(context.raw_urls)
	context.history_file = PlexusHistoryFile()
	context.history_file.add_urls(links)


@then(u'I expect the plexus history file to look like this')
def step_impl(context):
	print("\nJCDC: exp=\n", context.text)
	print("JCDC: got=\n", context.history_file.text)
	assert(context.text == context.history_file.text)

