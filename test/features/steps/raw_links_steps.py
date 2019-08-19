from behave import given, when, then
from plexusscraper.scraper import Scraper


@given(u'a scraper')
def step_impl(context):
	context.scraper = Scraper()


@when(u'links {links} are added')
def step_impl(context, links):
	try:
		context.scraper.add_raw_links(links)
	except ValueError as e:
		context.caught_exception = e

@then(u'the acestream count should be {ace_count:d} and the sopcast count should be {sop_count:d}')
def step_impl(context, ace_count, sop_count):
	actual_ace_count = len(context.scraper.get_acestream_links())
	assert(actual_ace_count == ace_count)

	actual_sop_count = len(context.scraper.get_sopcast_links())
	assert(actual_sop_count == sop_count)


@then(u'the scraper should raise an exception')
def step_impl(context):
	assert(context.caught_exception)
