from behave import given, when, then
from behave_webdriver.steps import *
from nose.tools import assert_equal


@when(u'I click on the link named "{link_text}"')
def step_impl(context, link_text):
	context.home_page.click_link(link_text)


@When(u'I save a new url {url} in slot {slot}')
def step_impl(context, url, slot):
	context.urls_page.save_url(slot, url)


@then(u'I expect to see some existing plexus scraper urls')
def step_impl(context):
	assert_equal(context.urls_page.get_page_title(), "Plexus Scraper URL uploader")
	assert_equal(5, len(context.urls_page.get_all_urls()))


@then(u'I expect {url} to be saved in slot {slot}')
def step_impl(context, url, slot):
	# This "error" response is expected, due to the fact that we are loading 
	# a web page from one port (the kodi web server port), and saving our new
	# url to a different port (the kodi rpc server). My own research suggests
	# this is due to <a href="https://en.wikipedia.org/wiki/Same-origin_policy">Same-origin security policy</a>.
	# The response we are seeing here is actually from our mock kodi rpc server.

	result_text = context.urls_page.get_url_save_result()
	expected_text = '{"readyState":0,"responseText":"","status":0,"statusText":"error"}'
	assert_equal(expected_text, result_text)

	context.urls_page.refresh()
	expected_text = url
	actual_text = context.urls_page.get_url(slot)
	assert_equal(actual_text, expected_text)

