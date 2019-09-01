@acceptance
@fixture.web_browser
@fixture.kodi_mock
Feature:  Plexus Scraper web interface
As a user
I should be able to view and save plexus scraper urls


# NOTE: This scenario uses built-in step implementations.
Scenario: Load the main web page
  Given I open the url "http://localhost:8080/index.html"
   Then I expect that the title is "My own Kodi Web Interface Addon"


# NOTE: The "When" step has "..click on the link named.." rather 
#	than simply "..click on the link..". I've done this 
#	intentionally, so I don't trigger the built-in
#	step implementation for "..click on the link..".
#	See https://pypi.org/project/behave-webdriver/
#	I done this because I want to implement my own step
#	function.
Scenario: View the plexus scraper urls web page
  Given I open the url "http://localhost:8080/index.html"
   When I click on the link named "plexus.php"
   Then I expect to see some existing plexus scraper urls


Scenario Outline: Add a new plexus scraper url
  Given I open the url "http://localhost:8080/plexus.php"
   When I save a new url <url> in slot <slot>
   Then I expect <url> to be saved in slot <slot>
 
  Examples:
  | url                              | slot  |
  | http://somedomain.com/page_1.htm | url_1 |
  | http://somedomain.com/page_2.htm | url_2 |
  | http://somedomain.com/page_3.htm | url_3 |
  | http://somedomain.com/page_4.htm | url_4 |
  | http://somedomain.com/page_5.htm | url_5 |

