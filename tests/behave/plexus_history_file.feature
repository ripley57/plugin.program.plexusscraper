@acceptance
@fixture.external_website
Feature: Create a plexus history file.


Scenario: Create a history file from a downloaded web page and save to a txt file
  Given a web url http://localhost:9999/sample_2.html
   When I generate a plexus history file from a downloaded web page and save to a txt file 
   Then I expect the plexus history file to look like this:
    """
    ACE_01|acestream://78637dab85e7948057165ad0c80b3db475dd9c3d|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
    ACE_02|acestream://8d9094e60cac92486cd23d1311a4ef1261a337ed|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
    ACE_03|acestream://c389afdd68246467538cec05eace0ca6410e4bb4|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
    ACE_04|acestream://ea1b551f853a6b2caa23eba805c5d093cba8754d|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
    ACE_05|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
    ACE_06|acestream://edea841c6cf26dae745d6bb71e62176402f30d35|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
    ACE_07|acestream://fdfee279394421f2ea89078150e1a2bb7d13f5ce|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
    SOP_01|sop://broker.sopcast.com:3912/264740|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
    SOP_02|sop://broker.sopcast.com:3912/264750|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
    SOP_03|sop://broker.sopcast.com:3912/264752|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
    SOP_04|sop://broker.sopcast.com:3912/264830|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
    SOP_05|sop://broker.sopcast.com:3912/265589|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
    """


Scenario: Create a history file from a local html file
  Given a local html file tests/resources/html/sample_1.html
   When I generate a plexus history file from a local html file
   Then I expect the plexus history file to look like this
     """
     ACE_01|acestream://78637dab85e7948057165ad0c80b3db475dd9c3d|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_02|acestream://c389afdd68246467538cec05eace0ca6410e4bb4|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_03|acestream://ea1b551f853a6b2caa23eba805c5d093cba8754d|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_04|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_05|acestream://edea841c6cf26dae745d6bb71e62176402f30d35|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     SOP_01|sop://broker.sopcast.com:3912/264740|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     SOP_02|sop://broker.sopcast.com:3912/264750|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     SOP_03|sop://broker.sopcast.com:3912/264830|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     SOP_04|sop://broker.sopcast.com:3912/265589|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     """


Scenario: Create a history file from a downloaded web page
  Given a web url http://localhost:9999/sample_1.html
   When I generate a plexus history file from a downloaded web page
   Then I expect the plexus history file to look like this
     """
     ACE_01|acestream://78637dab85e7948057165ad0c80b3db475dd9c3d|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_02|acestream://c389afdd68246467538cec05eace0ca6410e4bb4|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_03|acestream://ea1b551f853a6b2caa23eba805c5d093cba8754d|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_04|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_05|acestream://edea841c6cf26dae745d6bb71e62176402f30d35|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     SOP_01|sop://broker.sopcast.com:3912/264740|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     SOP_02|sop://broker.sopcast.com:3912/264750|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     SOP_03|sop://broker.sopcast.com:3912/264830|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     SOP_04|sop://broker.sopcast.com:3912/265589|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     """

 
Scenario: Create a history file from html containing acestream and sopcast urls
  Given a string of html
     """
     <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
     <html lang="de">
     <head>
     <title>Sheffield Utd &ndash; Crystal Palace. LiveStream, Live Übertragung: / Fu&#223;ball. England. Premier League / 18 August / LiveTV</title>
     <META HTTP-EQUIV="Content-Type" CONTENT="text/html; CHARSET=ISO-8859-1">
     </head>
     <body>
     <table  width=166 height=26 cellpadding=0 cellspacing=0  class="lnktbj">
     <tr>					
     <td align="right" width=15><a href="sop://broker.sopcast.com:3912/264750"><img title="Îòêðûòü â ïðèëîæåíèè" src="//cdn.livetvcdn.club/img/webtv.gif"></a></td>
     <td align="right" width=15><a href="sop://broker.sopcast.com:3912/265589"><img title="Îòêðûòü â ïðèëîæåíèè" src="//cdn.livetvcdn.club/img/webtv.gif"></a></td>
     <td align="right" width=15><a href="sop://broker.sopcast.com:3912/264740"><img title="Îòêðûòü â ïðèëîæåíèè" src="//cdn.livetvcdn.club/img/webtv.gif"></a></td>
     </tr>
     </table>
     <table  width=166 height=26 cellpadding=0 cellspacing=0  class="lnktbj">
     <tr>
     <td align="right" width=15><a href="acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9"><img title="Îòêðûòü â ïðèëîæåíèè" src="//cdn.livetvcdn.club/img/webtv.gif"></a></td>
     <td align="right" width=15><a href="acestream://78637dab85e7948057165ad0c80b3db475dd9c3d"><img title="Îòêðûòü â ïðèëîæåíèè" src="//cdn.livetvcdn.club/img/webtv.gif"></a></td>
     <td align="right" width=15><a href="acestream://c389afdd68246467538cec05eace0ca6410e4bb4"><img title="Îòêðûòü â ïðèëîæåíèè" src="//cdn.livetvcdn.club/img/webtv.gif"></a></td>
     </tr>
     </table>
     </body>
     </html>
     """
   When I generate a plexus history file from a string of html
   Then I expect the plexus history file to look like this
     """
     ACE_01|acestream://78637dab85e7948057165ad0c80b3db475dd9c3d|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_02|acestream://c389afdd68246467538cec05eace0ca6410e4bb4|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_03|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     SOP_01|sop://broker.sopcast.com:3912/264740|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     SOP_02|sop://broker.sopcast.com:3912/264750|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     SOP_03|sop://broker.sopcast.com:3912/265589|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     """

Scenario: Create a history file from a string of raw acestream and sopcast urls
  Given a string of raw urls
     """
     SOP_EX_1|sop://broker.sopcast.com:3912/26475,sop://broker.sopcast.com:3912/265589,ACE 1|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9,acestream://c389afdd68246467538cec05eace0ca6410e4bb4
     """
   When I generate a plexus history file from a string of raw urls
   Then I expect the plexus history file to look like this
     """
     ACE 1|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_01|acestream://c389afdd68246467538cec05eace0ca6410e4bb4|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     SOP_01|sop://broker.sopcast.com:3912/265589|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     SOP_EX_1|sop://broker.sopcast.com:3912/26475|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     """

