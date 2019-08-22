#!/storage/.kodi/addons/webinterface.webif/bin/php-cgi -q 

<?php 

	// Description:
	//	Extract raw acestreams links from the addon settings.xml file.
	//
	//	Raw acestream links we will recognise looks like one of these:
	//
	//	    acestream://9eba690be925a98e8aecfc758070b874e19260c6
	//	    SPORTS NEWS acestream://9eba690be925a98e8aecfc758070b874e19260c6
	//
	//	If a link name is included, add a '|' separator, e.g.:
	//	    SPORTS NEWS|acestream://9eba690be925a98e8aecfc758070b874e19260c6
	//
	//	If a link name is NOT included, create our own name, e.g.:
	//	    RAW_1|acestream://9eba690be925a98e8aecfc758070b874e19260c6

 	$xml=simplexml_load_file("file:///storage/.kodi/userdata/addon_data/program.plexusscraper/settings.xml") 
				or die("Error: Cannot create object");

	$count = 1;
	foreach($xml->children() as $setting) {
		$value = $setting['value'];

		if (ereg('acestream://', $value) == true) {

			// This is an acestream link in some format.

			if (ereg('[^\s]+acestream://', $value) == true) {

				// This acestream link includes a link name.

				preg_match('/(.+)\s+(acestream:\/\/[^\s]+)/', $value, $matches);
				printf("%s|%s\n", trim($matches[1]), trim($matches[2]));

			} else {

				// Create our own link name.

       				printf("RAW_%d|%s\n", $count, $value);

				$count++;
			}
		}
	}
?> 
