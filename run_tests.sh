#!/usr/bin/env bash
#
# Description:
#	Run tests
#
# Usage:
#	Run acceptance tests:
#		./run_tests [acceptance]
#
#	Run unit tests:
#		./run_tests unit
target=${1:-acceptance}		;# By default run acceptance tests


function acceptance_tests()
{
# Acceptance tests.
#
# Introduction to Python Behave:
# https://semaphoreci.com/community/tutorials/getting-started-with-behavior-testing-in-python-with-behave
# Python Behave docs:
# https://behave.readthedocs.io/en/latest/
#
# NOTE:
# A useful behave option is "--junit" option, which generates JUnit-compatible
# test reports in the "reports" directory. This makes it easy to incorporate Behave 
# tests into your build process using a continuous integration server, and also allows 
# for more sophisticated reporting with Thucydides.
#
# Note "-w" is a shorthand for "--tags=@wip", and seems to be the best option when working
# on a new feature/scenario and you don't want to run/see the other features/scenarios. See:
# https://behave.readthedocs.io/en/latest/tutorial.html?highlight=tags#controlling-things-with-tags
#behave -w test/features
#
# Filtering to only see the one feature I'm working on, using this, doesn't seem to
# work very well. Sure the other feature(s) are being run, but I still see a lot of
# 'noise' from them in the output.
#behave --tags=wip test/features/
#
# Run acceptance tests.
behave test/features/ --junit
}


function unit_tests()
{
# Unit tests.
#
# TODO: 
# * Consider using pytest instead of the standard unittest module.
# * Create separate integration tests.
#
# Run unit tests using unittest
# See https://docs.python.org/2/library/unittest.html
#python3 -m unittest plexusscraper/test_*.py
#
# Run unit tests using pytest
# See https://docs.pytest.org/
pytest plexusscraper -v
}


case $target in
"acceptance")
	acceptance_tests
	;;
"unit")
	unit_tests
	;;
"all")	
	unit_tests
	acceptance_tests
	;;
esac

