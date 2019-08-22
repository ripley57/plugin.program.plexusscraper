"""Plexus Scraper Project"""

from .plexushistoryfile import ( 
    PlexusHistoryFile,
)

from .testing.utils.webserver import (
    WebServer,
)

__version__ = '0.0.1'


# We might need this at some point, to distribute any package
# dependencies, rather than polluting the Kodi Python packages.
#import sys
#ver = sys.version
#if ver.startswith('3'):
#	sys.path.append("extras_python3")
#else:
#	sys.path.append("extras_python2")

