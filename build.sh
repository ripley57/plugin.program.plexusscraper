#!/usr/bin/env bash
#
# Build different package types.
#
# Useful:
#	https://python-packaging.readthedocs.io/en/latest/

if [[ "$1" = --help ]]
then
	cat <<EOI

usage:
	./build.sh [--help|local|dist|zip|kodi]

where:
	local	-	Install locally.
	dist	-	Package as a .whl and .tar.gz files.
	zip	-	Package the CLI tool as a self-executing zip.
	kodi	-	Package ready to deploy to Kodi.

EOI
	exit 1
fi

target=${1:-dist}
[[ $# > 0 ]] && shift


function local_install()
{
	# The -e (--editable) option to pip installs the modules as links under
	# the Python site-packages directory that points back to this directory.
	# This means we can continue to work on the modules here, and not have 
	# to keep re-installing them.
	pip install -e .
}


function build_dist()
{
	# Package the modules as .whl and .tar.gz files. 
	python setup.py sdist bdist_wheel
}


function build_zip()
{
	# Python can package a program in a self-executiving zip, similar to
	# a self-executing jar file in Java. This is a handy way to package
	# the plexusscraper CLI tool, together with any dependencies.

	echo "TO BE IMPLEMENTED!" >&2 
	exit 1
}


function build_kodi()
{
	# Create the file structure for the plexusscraper Kodi plugin.

	echo "TO BE IMPLEMENTED!" >&2 
	exit 1
}


case $target in
"local")
	local_install "$@"
	;;
"dist")
	build_dist "$@"
	;;
"zip")
	build_zip "$@"
	;;
"kodi")
	build_kodi "$@"
	;;
esac

