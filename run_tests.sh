# Introduction to Python Behave:
# https://semaphoreci.com/community/tutorials/getting-started-with-behavior-testing-in-python-with-behave
#
# Python Behave docs:
# https://behave.readthedocs.io/en/latest/
#
# NOTE:
# A useful behave option is "--junit" option, which generates JUnit-compatible
# test reports in the "reports" directory. This makes it easy to incorporate Behave 
# tests into your build process using a continuous integration server, and also allows 
# for more sophisticated reporting with Thucydides.

behave test/features/

# Note "-w" is a shorthand for "--tags=@wip", and seems to be the best option when working
# on a new feature/scenario and you don't want to run/see the other features/scenarios. See:
# https://behave.readthedocs.io/en/latest/tutorial.html?highlight=tags#controlling-things-with-tags
#`behave -w test/features

# Filtering to only see the one feature I'm working on, using this, doesn't seem to
# work very well. Sure the other feature(s) are being run, but I still see a lot of
# 'noise' from them in the output.
#behave --tags=wip test/features/

