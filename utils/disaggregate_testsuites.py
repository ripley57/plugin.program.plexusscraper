""" Disaggregate the xml file created by pytest 

    The pytest option "--junit-xml=TESTS-out.xml" creates an xml file with the
    executed test suites aggregated together, e.g. the xml starts like this:

        <testsuites><testsuite errors="0"...

    This causes a problem when we use Ant junitreport in our pom.xml file to
    try and convert the xml file to html. The problem is that Ant junitreport 
    does not expect the xml file to contain already-aggregated testsuites.

    (BTW: Converting JUnit xml files to html, as I'm doing here, can apparently also be
    done using the Maven plugins "maven-surefire-plugin" and "maven-surefire-report-plugin".
    However, the "maven-site-plugin" is required in order to invole report plugin, and
    means you would use "mvn site" to convert invoke the report generation. While I did
    get this to work, I didn't like the html output, or the complexity in my pom.xml file.
    That's why I'm instead using Ant from inside Maven, via the "maven-antrun-plugin"
    plugin).

    The purpose of this python program is to disaggregate the specified input
    xml file, creating separate files for each testsuite, e.g. TEST-unit-01.xml,
    TEST-unit-02.xml, etc. (No name of the file doesn't seem to have an affect on
    the final html file that is created.

    JeremyC 26-08-2019
"""

import copy
import os
import sys
import xmltodict

testsuite_count = 0

def disaggregate(in_file_path, out_dir_path):
	global testsuite_count
	data = xmltodict.parse(open(in_file_path).read())

	# NOTE:
	# xmltodict doesn't like it when you only have a list of one item,
	# because xmltodict doesn't treat it as a list. This causes a 
	# problem, as in this script, where we expect it to always be a list
	# of child 'testsuite' items, under a top-level 'testsuites' item.
	# The answer is to use the following syntax, to ensure that a list 
	# is always created. See:
	# https://stackoverflow.com/questions/37207353/xmltodict-does-not-return-a-list-for-one-element 

	data = xmltodict.parse(open(in_file_path).read(), force_list={'testsuite'})

	for ts_dict in data['testsuites']['testsuite']:
		testsuite_count += 1
		new_ts_dict = {'testsuite' : ts_dict}
		basename = "TESTS-testsuite-{}.xml".format(str(testsuite_count).zfill(2))
		with open(os.path.join(out_dir_path, basename), 'w') as file:
			file.write(xmltodict.unparse(new_ts_dict, pretty=True))

if __name__ == '__main__':
	args = sys.argv[1:]
	for in_file_path in args:
		disaggregate(in_file_path, os.path.dirname(in_file_path))

