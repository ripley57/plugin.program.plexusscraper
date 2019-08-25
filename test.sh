#!/usr/bin/env bash
#
# Run unit and/or acceptance tests.
#
set -e
set +x

PYTHON=python3	

if [[ "$1" = --help ]]
then
	cat <<EOI

usage:
	./test.sh [--help|unit|acceptance|functional|all|coverage]

Any additional arguments will be passed on, e.g. to skip pytests marked as "slow":

	./test.sh unit -m "not slow"

EOI
	exit 1
fi

target=${1:-unit}	;# Run unit tests by default
[[ $# > 0 ]] && shift


function install_test_dependencies()
{
	pip install pytest pytest-mock behave --ignore-installed
}

function install_program_dependencies()
{
	pip install bs4 requests click xmltodict --ignore-installed
}

function update_python_syspath()
{
	# BY setting PYTHONPATH, this valuegets added to front of sys.path
	# (See https://pymotw.com/2/site/)
	# This ensures that "pip install" installs packages to our local
	# "site-packages" directory.
	site_packages_dir=$(find ./venv -type d -name site-packages)
	site_packages_dir_fullpath=$(cd "$site_packages_dir" && pwd)
	# The following use of "sitecustomize.py" doesn't work, because we 
	# still need to use the "base" Python installation for the Python
	# standard library (including, for example, the "re" package).
        # (See my further comments in "sitecustomize.py").
	#cp ./sitecustomize.py "$site_packages_dir_fullpath/"
	export PYTHONPATH=$site_packages_dir_fullpath
}

# Create local virtual environment.
if [ ! -d venv ]; then
	echo "Creating a Python virtual environment in \"venv\" ..."
	command -v deactivate >/dev/null 2>&1 && deactivate
	${PYTHON} -m venv venv
	source venv/bin/activate

	update_python_syspath

	# NOTE: We use the "--ignore-installed" (-I) option to ensure that we install
	# local copies of any extra packages we need. This will stop us seeing instances
	# of "Requirement already satisfied" because pip finds the requested package
	# somewhere else in the sys.path.
	install_test_dependencies
	install_program_dependencies
fi

update_python_syspath
source venv/bin/activate


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
# This can we used to only run specific acceptance/scenarios. See:
# https://behave.readthedocs.io/en/latest/tutorial.html?highlight=tags#controlling-things-with-tags
#behave -w test/acceptance
#
behave tests/behave/ --tags=@acceptance --junit "$@"
}


function run_functional_tests()
{
behave tests/behave/ --tags=@functional --junit "$@"
}


function run_unit_tests()
{
# Unit tests, executed using the pytest framework (https://docs.pytest.org/)
#
# The pytest framework can run regular tests written for the "unittest"
# standard library. pytest provides additional features, plus it produces 
# a much nicer output than using "python -m unittest".
#
# Options passed:
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
#
#pytest tests/unit -q "$@"
pytest tests/unit -vv "$@"
#
# Run tests against both Python 2 and Python 3 versions using Tox.
# See https://tox.readthedocs.io
# TODO: webserver.py currently fails on Python 2. Due to changes in HTTPServer
#       in Python 3, we need seperate versions of webserver.py for Python 2 and 
#       Python 3. Creating these is not a problem using - the problem is how to
#       dynically find the correct version at runtime.
#tox tests/unit "$@" 
}


function run_code_coverage()
{
# We will use coverage.py, via the installation of pytest-cov, which allows
# us to run coverage it via pytest:
#	pip install pytest-cov
#
# See:
# 	https://coverage.readthedocs.io
#	https://pytest-cov.readthedocs.io
# 
pytest --cov=src --cov-report=html
}


function run_all_tests()
{
run_unit_tests
run_functional_tests
run_acceptance_tests
}


case $target in
"acceptance")
	run_acceptance_tests "$@"
	;;
"unit")
	run_unit_tests "$@"
	;;
"functional")
	run_functional_tests "$@"
	;;
"coverage")
	run_code_coverage "$@"
	;;
"all")	
	run_all_tests 
	;;
esac

