"""Minimal setup file for plexusscraper project."""

from setuptools import setup, find_packages

setup(
    name='plexusscraper',
    version='0.0.1',
    license='proprietary', 
    description='Plexus Scraper Project',

    author='not specified',
    author_email='not specified',
    url='not specified',

    packages=find_packages(where='src'),
    package_dir={'': 'src'},

    install_requires=[],
    tests_require=[],
    extras_require={},

    entry_points={},
)
