# conftest.py
#
# To share fixtures among multiple test files, we need to use a 
# conftest.py file somewhere centrally located for all of the tests.
#
# You can have other conftest.py files in subdirectories of the top
# tests directory. If you do, fixtures defined in these lower-level 
# conftest.py files will be available to tests in that directory and 
# subdirectories.
#
# Although conftest.py is a Python module, it should not be imported 
# by test files. Don’t import conftest from anywhere. The conftest.py 
# file gets read by pytest, and is considered a local plugin.
