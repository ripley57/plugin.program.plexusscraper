import os
from behave import given, when, then

from plexusscraper.linkservice import LinkService
from plexusscraper.urldownloader import URLDownloader


@given(u'the local file {file_path}')
def step_impl(context, file_path):
	context.file_path = file_path


@given(u'the url {url}')
def step_impl(context, url):
	context.url = url


@when(u'I extract all links')
def step_impl(context):
	context.links = LinkService.extract_links_from_file(context.file_path)


@when(u'I download and extract all links')
def step_impl(context):
	downloader = URLDownloader()
	(status, text) = downloader.download(context.url)
	context.links = LinkService.extract_links_from_html(text)


@then(u'I should get {ace_count:d} acestream links and {sop_count:d} sopcast links')
def step_impl(context, ace_count, sop_count):
	assert(len(context.links) == ace_count + sop_count)

