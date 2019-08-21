from behave import given, when, then

from plexusscraper.plexushistoryfile import PlexusHistoryFile


@given(u'a local html file {file}')
def step_impl(context, file):
	context.path = file


@given(u'a string of html')
def step_impl(context):
	context.html = context.text


@given(u'a string of raw urls')
def step_impl(context):
	context.raw_urls = context.text


@given(u'a web url {url}')
def step_impl(context, url):
	context.url = url


@when(u'I generate a plexus history file from a downloaded web page')
def step_impl(context):
	context.history_file = PlexusHistoryFile()
	context.history_file.add_links_from_url(context.url)
	

@when(u'I generate a plexus history file from a local html file')
def step_impl(context):
	context.history_file = PlexusHistoryFile()
	context.history_file.add_links_from_file(context.path)


@when(u'I generate a plexus history file from a string of html')
def step_impl(context):
	context.history_file = PlexusHistoryFile()
	context.history_file.add_links_from_html(context.html)


@when(u'I generate a plexus history file from a string of raw urls')
def step_impl(context):
	context.history_file = PlexusHistoryFile()
	context.history_file.add_links_from_string(context.raw_urls)


@then(u'I expect the plexus history file to look like this')
def step_impl(context):
	assert(context.text == context.history_file.text)

