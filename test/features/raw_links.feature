Feature: Accept raw links

Scenario Outline: Accept raw acestream or sopcast links
  Given a scraper
   When links <links> are added
   Then the acestream count should be <ace_count> and the sopcast count should be <sop_count>

  Examples: Links
  | links                                                                                                     | ace_count | sop_count | comments       |
  | sop://broker.sopcast.com:3912/264750                                                                      | 0         | 1         |                |
  | acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9                                                      | 1         | 0         |                |
  | sop://broker.sopcast.com:3912/264750,sop://broker.sopcast.com:3912/264751                                 | 0         | 2         |                |
  | sop://broker.sopcast.com:3912/264750 acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9                 | 1         | 1         | space delmiter |
  | sop://broker.sopcast.com:3912/264750,sop://broker.sopcast.com:3912/264750                                 | 0         | 1         | duplicate      |
  | acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9,acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba8 | 2         | 0         |                |
  | acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9,acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9 | 1         | 0         | duplicate      |


Scenario Outline: Raise exception for invalid links
  Given a scraper
   When links <links> are added
   Then the scraper should raise an exception

  Examples: Links
  | links                                                                      |
  | sopcast.com                                                                |
  | sop://broker.sopcast.com:3912/264750,,sop://broker.sopcast.com:3912/264751 |
  | ,,                                                                         |
  
