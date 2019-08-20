@fixture.webserver
Feature: Extract links from an html web page


Scenario Outline: Extract links given the path to a local file
  Given the local file <file_path>
   When I extract all links
   Then I should get <ace_count> acestream links and <sop_count> sopcast links

  Examples:
  | file_path                         | ace_count | sop_count |  
  | test/resources/html/sample_1.html | 5         | 4         |
  | test/resources/html/sample_2.html | 7         | 5         |


# Moved this to feature tag to be feature-level rather than scenario-level (see top of this file).
# This is because here it was triggering the fixture method to start the web server for each 
# individual test, which isn't needed, or ideal.
#@fixture.webserver
Scenario Outline: Extract links given a url
  Given the url <url>
   When I download and extract all links
   Then I should get <ace_count> acestream links and <sop_count> sopcast links

  Examples:
  | url                                 | ace_count | sop_count |
  | http://localhost:9090/sample_1.html | 5         | 4         |
  | http://localhost:9090/sample_2.html | 7         | 5         |

