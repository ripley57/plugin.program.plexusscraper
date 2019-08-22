#!/usr/bin/env bash
#
# Run unit and/or acceptance tests.
#

if [[ "$1" = --help ]]
then
	cat <<EOI

usage:
	run_tests [--help|unit|acceptance|all]

Any additional arguments will be passed on, e.g. to skip pytests marked as "slow":

	run_tests unit -m "not slow"

EOI
	exit 1
fi

target=${1:-unit}	;# Run unit tests by default
shift


# In order for our test modules (in the "tests/" directory) to be able to
# import the packages we are testing (in the "src/" directory), we can use
# "pip install -e ." to install a "<package-name>.egg-link" file under 
# our Python installation. Instead of installing copies of a package, this
# creates a link back to the files in this directory. This works because
# we have a "setup.py" file in this directory. The "-e" option also means
# we can make changes to the files and re-test without having to re-install.
if ! pip show plexusscraper >/dev/null 2>&1 ; then
	pip install -e .
fi


function run_acceptance_tests()
{
# Acceptance tests using Python Behave (https://behave.readthedocs.io/en/latest/)
#
# The "--junit" option generates JUnit-compatible test reports, for use with
# reporting tools such as Thucydides.
#
# The "-w" option is a shorthand for "--tags=@wip". 
# This can we used to only run specific features/scenarios. See:
# https://behave.readthedocs.io/en/latest/tutorial.html?highlight=tags#controlling-things-with-tags
#behave -w test/features
#
behave tests/features/ --junit "$@"
}


function run_unit_tests()
{
# Unit tests, executed using the pytest framework (https://docs.pytest.org/)
#
# The pytest framework can run regular tests written for the "unittest"
# standard library. pytest provides additional features, plus it produces 
# a much nicer output than using "python -m unittest".
#
pytest tests/unit -vv "$@"
}


function run_all_tests()
{
run_unit_tests
run_acceptance_tests
}


case $target in
"acceptance")
	run_acceptance_tests "$@"
	;;
"unit")
	run_unit_tests "$@"
	;;
"all")	
	run_all_tests 
	;;
esac

