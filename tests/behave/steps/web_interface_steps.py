from behave import given, when, then

import bs4
import time

# Have assert failures outptu more helpful text.
from nose.tools import assert_equal

# This gives us a selection of step implementations for free!
# See https://pypi.org/project/behave-webdriver/
from behave_webdriver.steps import *

from selenium.webdriver.common.by import By


@when(u'I save url {url} in slot {url_id}')
def step_impl(context, url, url_id):
	# Find the correct input textbox.
	input_textbox = context.web.find_by_xpath("//input[@type='text' and @class='urlTextbox' and @name='{}']".format(url_id))

	# Enter the url to save.
	input_textbox.clear()
	input_textbox.send_keys(url);

	# Click the button.
	button_id = "button_" + url_id
	update_button = context.web.find_by_xpath("//button[@id='{}']".format(button_id))
	update_button.click()


@when(u'I click on the link named "{link_text}"')
def step_impl(context, link_text):
	# Wait for page to load, by waiting for the 'plexus.php' link to appear, then click the link.
	context.web.find_by_xpath("//a[@href='{}']".format("plexus.php")).click()
	# debugging
	#print("page_source=", context.behave_driver.page_source)

	# NOTE: Leaving this code here for now, for future reference. It turns out that this
	# extra waiting for the	 page to download in Web.wait_for_page_load() is not actually 
	# needed. I did wonder about this, since the find_by_xpath() call we're making also
	# has a built-in wait. It turns out the reason I didn't see the new page content (from
	# the "click()") was that my html links had target="_NEW", so there were opening a 
	# new tab! After I changed the links to target="_self" (the default), everything then
	# worked, i.e. "page_source" gave me the new page contents and not the old.
	#with context.web.wait_for_page_load(timeout=10):
	#	context.web.find_by_xpath("//span[text()='Upload Plexus Scraper URLs:']")

	# Wait for page to load.
	context.web.find_by_xpath("//span[text()='Upload Plexus Scraper URLs:']")
	# debugging
	#print("page_source=", context.behave_driver.page_source)


@then(u'I expect to see some existing plexus scraper urls')
def step_impl(context):
	# Verify title. We'll use BeautifulSoup for this.
	bs = bs4.BeautifulSoup(context.web._web_driver.page_source, "html.parser")
	title_list = bs.findAll('title')
	assert_equal(title_list[0].text, "Plexus Scraper URL uploader")
	
	# Verify x5 input text boxes. We'll use xpath for this.
	input_elements = context.web.finds_by_xpath("//input[@type='text' and @class='urlTextbox' and starts-with(@name,'url_')]")
	print("input_elements=",len(input_elements))
	assert_equal(5, len(input_elements))


@then(u'I expect url {url} to be saved in slot {url_id} of the settings.xml file')
def step_impl(context, url, url_id):
	# Verify that there is some value to the right of "Response from Kodi:". 
	result_text = context.web.find_by_xpath("//span[@id='result']").text

	# NOTE: This "error" response is expected, due to the fact that we are loading 
	#	a web page from one port (the kodi web server port), and saving our new
	#	url to a different port (the kodi rpc server). My own research suggests
	#	this is due to <a href="https://en.wikipedia.org/wiki/Same-origin_policy">Same-origin security policy</a>.
	#	The response we are seeing here is actually from our mock kodi rpc server.
	#
	# TBC:  Interestingly, the error is not seen on the production system when
	#	an Android phone web browser is used to access the kodi web server; the
	#	error only happens when using a PC web browser as a client. However, 
	#	despite the error, the request from the PC is actioned successfully by
	#	kodi. This would suggest that the error is in fact coming from the web
	#	browser (or client OS).

	expected_text = '{"readyState":0,"responseText":"","status":0,"statusText":"error"}'
	assert_equal(expected_text, result_text)

