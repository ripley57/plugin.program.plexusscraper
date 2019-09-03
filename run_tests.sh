#!/usr/bin/env bash
#
# Run acceptance and unit tests.
#
# Example usage:
#
# 	Run all tests (generating json/xml results in the "reports/" directory):
#	./run_tests.sh all
#
#	Run unit and acceptance tests:
#	./run_tests.sh unit acceptance
#
#	To generate html test reports (from the json/xml results):
#	mvn verify
#
#
# 	Location of html test reports
# 	=============================
# 	acceptance tests 	-	reports/html/cucumber-html-reports/overview-features.html
# 	unit tests		-	reports/html/unit/junit-noframes.html
# 	code coverage		-	reports/html/coverage/index.html
#
#
# JeremyC

set -e
set +x

SCRIPTNAME=$0
PYTHON=python3	

if [[ "$1" = --help ]]
then
	cat <<EOI

usage:
	$SCRIPTNAME [--help|unit|acceptance|coverage|all]

EOI
	exit 1
fi


# We access the webinterface_webif add files as a git submodule.
# First we will ensure we have the latest files of the submodule.
# References:
# https://github.blog/2016-02-01-working-with-submodules/
# https://www.vogella.com/tutorials/GitSubmodules/article.html
git submodule update --init --recursive


# Keep track of the tests that have run to completion, or not.
# With all the output streaming past, it is difficult to see
# which tests actually completed. We use a simple bash hash.
declare -A tests_run_array
function test_started()
{	
	local _name=$1
	tests_run_array["$_name"]="STARTED"
}
function test_completed()
{
	local _name=$1
	tests_run_array["$_name"]="COMPLETED"
}
function tests_run_summary()
{
	local _name
	local _state

	if [[ ${#tests_run_array[@]} -gt 0 ]]; then
		printf "\n\tTests run:\n"
		for _name in "${!tests_run_array[@]}"; do 
			_state=${tests_run_array["$_name"]}
			printf "\t%-15s : %s\n" "$_name" "$_state"
		done
		printf "\n"
		how_to_generate_html_reports
	fi
}

# Display tests summary if unexpected error occurs.
# Note: We have "set -e" at the top of this script.
function cleanup()
{
	exit_status=$?
	echo "Caught an error!"
	tests_run_summary
	exit $exit_status
}
trap cleanup 0 1 2 3 15


function install_python_dependencies()
{
	# We use the "--ignore-installed" (-I) option to ensure that we install
	# local copies of any extra packages we need. This will stop us seeing 
	# "Requirement already satisfied" because pip has found the requested
	# package somewhere else in the module search path (sys.path).

	# dependencies for testing
	pip install pytest pytest-cov pytest-mock behave behave-webdriver wheel behave2cucumber nose psutil --ignore-installed

	# dependencies of our program
	pip install bs4 requests click xmltodict --ignore-installed
}


function update_python_syspath()
{
	# BY setting PYTHONPATH, this value gets added to front of sys.path
	# (See https://pymotw.com/2/site/)
	# This ensures that "pip install" installs packages to our local
	# "site-packages" directory, and not anywhere else.

	site_packages_dir=$(find ./venv -type d -name site-packages)
	site_packages_dir_fullpath=$(cd "$site_packages_dir" && pwd)
	export PYTHONPATH=$site_packages_dir_fullpath

	# NOTE:
	# The commented-out use of "sitecustomize.py" didn't work, because
	# we still need to use the base Python installation for the Python
	# standard library (which includes, for example, the "re" package).
        # (See my additional comments in "sitecustomize.py").
	#cp ./utils/sitecustomize.py "$site_packages_dir_fullpath/"
}


# Create local python virtual environment to run our tests.
if [ ! -d venv ]; then
	echo "Creating a Python virtual environment in \"venv\" ..."
	command -v deactivate >/dev/null 2>&1 && deactivate
	${PYTHON} -m venv venv
	source venv/bin/activate
	update_python_syspath
	install_python_dependencies
fi

update_python_syspath
source venv/bin/activate


# The simplest way for our test modules (in the "tests/" directory) to be able 
# to import the packages we are testing (in the "src/" directory), is to install
# our program package ("plexusscraper") locally. We do this here using:  
# 	"pip install -e .". 
# This creates a link ( "<package-name>.egg-link") file under the Python 
# installation's "site-packages" directory.
# NOTE: Running "pip install -e ." requires our "setup.py" file.
# The "-e" is short for "--editable" and means we can continue to edit our
# program files locally, with needing to keep re-installing them.
if ! pip show plexusscraper >/dev/null 2>&1
then
	pip install -e .
fi


function run_acceptance_tests()
{
# We will use Python Behave (https://behave.readthedocs.io)
#
# Behave (https://behave.readthedocs.io) is a Gherkin-based BDD tool for Python 
# programs. Similar BDD tools for Python are Lettuce (http://pythonhosted.org/lettuce) 
# and Freshen (https://github.com/rlisagor/freshen). I have also come across pytest-bdd
# (https://pytest-bdd.readthedocs.io), but have not tried it yet. Behave is apparently
# "...the most stable, best documented, and most feature-rich of the three" (from 
# eBook "BDD In Action" (2015).
#
# Installation:
# pip install behave
#
# To run one particular feature, specify the path to the feature file, e.g.:
#	behave tests/behave/extract_links.feature
#
# To run one particular scenario of a feature, add "@wip" above the scenario in
# the feature file, and then run:
#	behave tests/behave --tags="@wip"
# 
	test_started "acceptance"

	behave tests/behave/ -f json -o "reports/TESTS-behave-acceptance.json"

	python -m behave2cucumber -i reports/TESTS-behave-acceptance.json -o reports/TESTS-cucumber-acceptance.json

	# Remove zero-byte file that is annoyingly left behind.
	[ ! -s behave2cucumber.log ] && rm -f behave2cucumber.log

	test_completed "acceptance"
}


function run_unit_tests()
{
# We will use pytest (https://docs.pytest.org/)
#
# The pytest framework can run regular tests written for "unittest" of the Python 
# standard library. But pytest provides additional features, and it produces a
# much nicer output.
#
# Installation:
# pip install pytest pytest-mock
#
# pytest handy options:
#	-x			Stops at the first test failure.
#	-s			Turn off stdout capture; instead display during tests.
#	--lf			Re-run only tests that failed last time.
#	--ff			Run test that failed last time first.
#	-l			Display local variables in failed test.
#	--fixtures		List all fixtures available to test.
#	--setup-show		Display full output from fixtures.
#	--doctest-modules	Test the code in function/module docstrings.
#	--markers		List all markers (custom and built-in).
#	-m <marker>		Run only tests marked with this (e.g. smoke).
#	-x --pdb 		Starts the debugger at the first test failure.
#				(-x prevents pdb from looking at the next failure).
#				NOTE: To stop the pdb debugger at a line of code:
#					import pdb; pdb.set_trace()
#
	test_started "unit"

	# Run unit tests, skipping any slow ones.
	pytest tests/unit -vv --junit-xml=reports/TESTS-unit.xml -m 'not slow'

	# We later use the Maven Ant plugin (see pom.xml) to convert this xml
	# file to html. The Ant junitreport task only expects the xml file to
	# contain a single testsuite result; so we need to split-up this file
	# into one xml file per testsuite.

	python utils/disaggregate_testsuites.py reports/TESTS-unit.xml

	# If we ever need to, it's possible to run tests against both Python 2 and 
	# Python 3 versions using Tox. See https://tox.readthedocs.io
	# NOTE: webserver.py currently fails on Python 2. Due to changes in HTTPServer
	#       in Python 3, we need seperate versions of webserver.py for Python 2 and 
	#       Python 3. Creating these is not a problem using "2to3" - the problem is 
	#	how to dynically find the correct version at runtime.
	#tox tests/unit

	test_completed "unit"
}


function run_code_coverage()
{
# We will use pytest-cov (https://pytest-cov.readthedocs.io)
#
# Installation:
# pip install pytest-cov
#
       test_started "code coverage"

       pytest -vv -s --cov=src --cov-report html:reports/html/coverage tests/unit/

       test_completed "code coverage"
}


function generate_html_reports()
{
       test_started "generate html reports"

       mvn verify

       test_completed "generate html reports"
}


function how_to_generate_html_reports()
{
	cat << EOI

	To generate html test reports in "reports/html":
	(Note: You will need to install Maven to run this)

	mvn verify

EOI
}


function run_test()
{
	# "-s" includes output (captured by default, any only displayed if test fails)
	pytest -s tests/unit/test_urldownloader.py
} 


for arg in "$@"; do

	case $arg in
	"unit")
		run_unit_tests "$@"
		;;
	"acceptance")
		run_acceptance_tests "$@"
		;;
	"coverage")
		run_code_coverage "$@"
		;;
	"html")
		generate_html_reports "$@"
		;;
	"all")	
		run_unit_tests "$@"
		run_acceptance_tests "$@"
		run_code_coverage "$@"
		;;
	"run_test")
		run_test "$@"
		;;
	esac
done

tests_run_summary

# Disable our trap.
trap '' 0 1 2 3 15

