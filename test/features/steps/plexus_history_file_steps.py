from behave import given, when, then

from plexusscraper.plexusscraper import PlexusScraper
from plexusscraper.plexushistoryfile import PlexusHistoryFile


@given(u'the following html')
def step_impl(context):
	context.html = context.text


@given(u'the following list of raw urls')
def step_impl(context):
	context.raw_urls = context.text


@when(u'I generate a plexus history file from the html')
def step_impl(context):
	context.result = PlexusScraper.extract_links_from_html(context.html)
	ace_list = context.result['acestream']
	sop_list = context.result['sopcast']
	context.history_file = PlexusHistoryFile()
	context.history_file.add_acestream_urls(ace_list)
	context.history_file.add_sopcast_urls(sop_list)


@when(u'I generate a plexus history file from the list of raw urls')
def step_impl(context):
	context.history_file = PlexusHistoryFile()
	context.history_file.add_raw_urls(context.raw_urls)


@then(u'I expect the plexus history file to look like this')
def step_impl(context):
	assert(context.text == context.history_file.text)

