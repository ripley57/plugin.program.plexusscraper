@functional
@fixture.external_website
Feature: Extract acestream and sopcast links from a web page


Scenario Outline: Extract links given the path to a local html file
  Given the local file <file_path>
   When I extract all links
   Then I should get <ace_count> acestream links and <sop_count> sopcast links

  Examples:
  | file_path                          | ace_count | sop_count |  
  | tests/resources/html/sample_1.html | 5         | 4         |
  | tests/resources/html/sample_2.html | 7         | 5         |


Scenario Outline: Extract links given a url
  Given the url <url>
   When I download and extract all links
   Then I should get <ace_count> acestream links and <sop_count> sopcast links

  Examples:
  | url                                 | ace_count | sop_count |
  | http://localhost:9999/sample_1.html | 5         | 4         |
  | http://localhost:9999/sample_2.html | 7         | 5         |

