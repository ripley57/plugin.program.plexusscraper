from behave import given, when, then

import bs4
import time

# Have assert failures outptu more helpful text.
from nose.tools import assert_equal

# This gives us a selection of step implementations for free!
# See https://pypi.org/project/behave-webdriver/
from behave_webdriver.steps import *

from selenium.webdriver.common.by import By


@when(u'I add new url {url}')
def step_impl(context, url):
	pass


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


@then(u'I expect the new url to be saved')
def step_impl(context):
	# TO BE IMPLEMENTED!
	pass

