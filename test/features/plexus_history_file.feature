Feature: Create a plexus history file.


Scenario: Create a history file from html containing acestream and sopcast urls
  Given the following html
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
   When I generate a plexus history file from the html
   Then I expect the plexus history file to look like this
     """
     ACE_01|acestream://78637dab85e7948057165ad0c80b3db475dd9c3d|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_02|acestream://c389afdd68246467538cec05eace0ca6410e4bb4|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_03|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     SOP_01|sop://broker.sopcast.com:3912/264740|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     SOP_02|sop://broker.sopcast.com:3912/264750|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     SOP_03|sop://broker.sopcast.com:3912/265589|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     """

Scenario: Create a history file from raw acestream and sopcast urls
  Given the following list of raw urls
     """
     SOP_EX_1|sop://broker.sopcast.com:3912/26475,sop://broker.sopcast.com:3912/265589,ACE 1|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9,acestream://c389afdd68246467538cec05eace0ca6410e4bb4
     """
   When I generate a plexus history file from the list of raw urls
   Then I expect the plexus history file to look like this
     """
     ACE 1|acestream://ebace2db83260b4d6097f0a52e86b2aee3c3bba9|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     ACE_01|acestream://c389afdd68246467538cec05eace0ca6410e4bb4|1|/storage/.kodi/addons/program.plexus/resources/art/acestream-menu-item.png
     SOP_01|sop://broker.sopcast.com:3912/265589|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     SOP_EX_1|sop://broker.sopcast.com:3912/26475|2|/storage/.kodi/addons/program.plexus/resources/art/sopcast_logo.jpg
     """

