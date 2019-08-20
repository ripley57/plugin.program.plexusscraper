from behave import given, when, then
from plexusscraper.scraper import Scraper
import os


@given(u'the local file {file_path}')
def step_impl(context, file_path):
	context.file_path = file_path


@given(u'the url {url}')
def step_impl(context, url):
	context.url = url


@when(u'I extract all links')
def step_impl(context):
	scraper = Scraper()
	context.result = scraper.extract_links_from_file(context.file_path)


@when(u'I download and extract all links')
def step_impl(context):
	scraper = Scraper()
	context.result = scraper.extract_links_from_url(context.url)


@then(u'I should get {ace_count:d} acestream links and {sop_count:d} sopcast links')
def step_impl(context, ace_count, sop_count):
	ace = context.result['acestream']
	sop = context.result['sopcast']
	assert(len(ace) == ace_count)
	assert(len(sop) == sop_count)

