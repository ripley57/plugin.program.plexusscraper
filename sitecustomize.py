# NOTE: This script is not actually being used. Leaving it here for 
#	education purposes for the time-being.
#
# Wow, what's the reason for this file?
#
# This content is from a "sitecustomize.py" file, that I created inside the 
#  "site-packages" directory of a new Python virtual env I named "venv", e.g. 
# /home/jcdc/demo/venv/lib/python3.6/site-packages/sitecustomize.py
#
# To trigger this code, I assigned the "site-packages" location to PYTHONPATH, 
# like this, inside a bash script I have for launching my python tests:
#	site_packages_dir=$(find . -type d -name site-packages)
#	site_packages_dir_fullpath=$(cd "$site_packages_dir" && pwd)
#	export PYTHONPATH=$site_packages_dir_fullpath
# (To see why this triggers the code, see https://pymotw.com/2/site/)
#
# Now for the explanation...
#
# I noticed that when I created a new Python virtual env, whilst already inside a
# different activate virtual env, my Python module search path (sys.path) was
# not limited to only directories under my new virtual env! 
#
# I had also earlier noticed that I needed to use "pip --ignore-installed" to 
# force a local install of any external packages that Python found in some other 
# directory outside of my virtual env! That fix looked like it had worked (it 
# certainly no longer displayed the message "Requirement already satisfied").
# However, the "site-packages" directory of my new virtual env was still empty, 
# and my python application, which I expected to fail because it couldn't find
# some dependent modules, was still mysteriously working!
#
# This led me to investigate why pip was not installing new external packages in
# the new virtual env's "site-packages" directory. (Note: when I create what I hope
# is a completely independent virtual env, I expect it to contain any external
# modules that I install, using "pip install <name> --ignore-installed").
# The cause turned out to be the contents of sys.path, hence the purpose of this 
# python script. This script resets sys.path. I've read mixed things about whether
# this is a valid thing to do or not, but hey ho.
#
# Now for the bad news...
#
# While this script does indeed work, and limits my sys.path to "." and the
# "site-packages" directory of my new virtual env, the end result is that we
# can no longer find modules from the Python standard library, e.g. "re" !!
# This is because...from https://www.python.org/dev/peps/pep-0405/:
# "[a virtual env] ...shares the standard library with the base installed Python"
#
# Hence, the best you can do for your new virtual env is to ensure that "." is
# on the front of the path, followed by the virtual env's "site-packages" 
# directory. This will ensure that your program finds any local modules first,
# and then searches next in it's own "site-packages" directory. This also ensures
# that any "pip install"ed packages are installed into the local "site-packages" 
# directory. But, remember that you still need the "base" Python installation, in 
# order find the standard library.
#
# THEREFORE MY RECOMMENDATION IS THAT, WHEN YOU NEED TO DETERMINE EXACTLY WHAT 
# EXTERNAL (I.E. NON-STANDARD LIBRARY) PACKAGES YOUR PROGRAM NEEDS, YOU SHOULD 
# ALWAYS USE A CLEAN/EMPTY PYTHON "BASE" INSTALL, THEN FROM THERE "ACTIVATE" 
# INTO YOUR NEW VIRTUAL ENV.

import sys
print("*** BEFORE: sys.path=", sys.path)
final_list = {'.', '/files/08_Github/plugin.program.plexusscraper/venv/lib/python3.6/site-packages'}
list_copy = sys.path[:]
for p in list_copy:
	if p not in final_list:
		sys.path.remove(p)
sys.path.insert(0, '.')
print("*** AFTER: sys.path=", sys.path)

