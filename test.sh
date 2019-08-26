#!/usr/bin/env bash
#
# Run acceptance (BDD) and unit tests.
#
# On Linux, to run all tests and generate html reports, and code coverage report:
# ./test.sh all
#
# See html report files in reports/html/
# 
# Maven is used for the final step of converting the test results from xml/json
# (see reports/) to html (see reports/html/. To re-run that last step, simply 
# run "mvn verify".
#
# JeremyC 26-08-2019

set -e
set +x

PYTHON=python3	

if [[ "$1" = --help ]]
then
	cat <<EOI

usage:
	./test.sh [--help|unit|acceptance|functional|coverage|html|all]

EOI
	exit 1
fi

target=${1:-unit}	;# Run only unit tests by default
[[ $# > 0 ]] && shift


function install_test_dependencies()
{
	# We use the "--ignore-installed" (-I) option to ensure that we install
	# local copies of any extra packages we need. This will stop us seeing 
	# "Requirement already satisfied" because pip has found the requested
	# package somewhere else in the module search path (sys.path).

	pip install pytest pytest-cov pytest-mock behave wheel behave2cucumber --ignore-installed
}
function install_program_dependencies()
{
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

	# NOTE:
	# The following use of "sitecustomize.py" doesn't work; because we 
	# still need to use the "base" Python installation for the Python
	# standard library (which includes, for example, the "re" package).
        # (See my additional comments in "sitecustomize.py").
	#cp ./utils/sitecustomize.py "$site_packages_dir_fullpath/"

	export PYTHONPATH=$site_packages_dir_fullpath
}


# Create local python virtual environment to run our tests.
if [ ! -d venv ]; then
	echo "Creating a Python virtual environment in \"venv\" ..."
	command -v deactivate >/dev/null 2>&1 && deactivate
	${PYTHON} -m venv venv
	source venv/bin/activate

	update_python_syspath

	install_test_dependencies
	install_program_dependencies
fi

update_python_syspath
source venv/bin/activate


# The simplest way for our test modules (in the "tests/" directory) to be able 
# to import the packages we are testing (in the "src/" directory), is to install
# our program package ("plexusscraper") locally. We do this using 
# "pip install -e .". This creates a link ( "<package-name>.egg-link") file under 
# the Python installation's "site-packages" directory.
# NOTE: Running "pip install -e ." uses our "setup.py" file.
# The "-e" is short for "--editable" and means we can continue to edit on our
# program files locally, with needing to keep re-installing our package.
if ! pip show plexusscraper >/dev/null 2>&1 ; then
	pip install -e .
fi


function run_acceptance_tests()
{
# We will use Python Behave (https://behave.readthedocs.io)
#
# Behave (https://behave.readthedocs.io) is a Gherkin-based BDD tool for Python 
# programs. Similar BDD tools for Python are Lettuce (http://pythonhosted.org/lettuce) 
# and Freshen (https://github.com/rlisagor/freshen). I've also come across pytest-bdd
# (https://pytest-bdd.readthedocs.io), but haven't tried it yet. Behave is apparently
# "...the most stable, best documented, and most feature-rich of the three" (from 
# eBook "BDD In Action" (2015).
#
# Installation:
# pip install behave
#
# Usage:
# "behave" is run from the command line.
#
	behave tests/behave/ --tags=@acceptance -f json -o reports/TESTS-behave-acceptance.json
	python -m behave2cucumber -i reports/TESTS-behave-acceptance.json -o reports/TESTS-cucumber-acceptance.json
	[ ! -s behave2cucumber.log ] && rm -f behave2cucumber.log	# Remove zero-byte output log file.
}
function run_functional_tests()
{
	behave tests/behave/ --tags=@functional -f json -o reports/TESTS-behave-functional.json
	python -m behave2cucumber -i reports/TESTS-behave-functional.json -o reports/TESTS-cucumber-functional.json
	[ ! -s behave2cucumber.log ] && rm -f behave2cucumber.log	# Remove zero-byte output log file.
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
	pytest tests/unit -vv --junit-xml=reports/TESTS-unit.xml

	# We use the Maven Ant plugin in our pom.xml to convert this xml
	# file to html. Ant junitreport only expects the xml file to
	# contain a single testsuite result; so we need to split-up this
	# file into possible multiple separate xml files, one per
	# testsuite result.
	python utils/disaggregate_testsuites.py reports/TESTS-unit.xml
#
# If you need to, you can run tests against both Python 2 and Python 3 versions,
# using Tox. See https://tox.readthedocs.io
# NOTE: webserver.py currently fails on Python 2. Due to changes in HTTPServer
#       in Python 3, we need seperate versions of webserver.py for Python 2 and 
#       Python 3. Creating these is not a problem using "2to3" - the problem is 
#	how to dynically find the correct version at runtime.
	#tox tests/unit
}


function run_code_coverage()
{
# We will use pytest-cov (https://pytest-cov.readthedocs.io)
#
# Installation:
# pip install pytest-cov
#
	pytest --cov=src --cov-report html:reports/html/coverage
}


function generate_html_reports()
{
	# Use maven "mvn" (which you need to install)
	mvn verify
}


function run_all()
{
	run_unit_tests
	run_functional_tests
	run_acceptance_tests
	run_code_coverage
	generate_html_reports
}


case $target in
"unit")
	run_unit_tests "$@"
	;;
"functional")
	run_functional_tests "$@"
	;;
"acceptance")
	run_acceptance_tests "$@"
	;;
"coverage")
	run_code_coverage "$@"
	;;
"html")
	generate_html_reports
	;;
"all")	
	run_all
	;;
esac

