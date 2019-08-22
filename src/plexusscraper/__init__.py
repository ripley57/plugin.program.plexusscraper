import sys

ver = sys.version
if ver.startswith('3'):
	sys.path.append("extras_python3")
else:
	sys.path.append("extras_python2")
