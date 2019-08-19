Feature: Extract links from an html web page


Scenario Outline: Extract links given the path to a local file
  Given the local file <file_path>
   When I extract all links
   Then I should get <ace_count> acestream links and <sop_count> sopcast links

  Examples:
  | file_path                         | ace_count | sop_count |  
  | test/resources/html/sample_1.html | 5         | 4         |
  | test/resources/html/sample_2.html | 7         | 5         |

