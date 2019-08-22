""" Helper functions related to Acestreams

    JeremyC 28-05-2018
"""

import re

def is_raw_acestream(arg):
    rtn = False
    matchObj = re.match('.*acestream://', arg)
    if matchObj:
        rtn = True
    #debug("is_raw_acestream", "arg=" + arg + ", rtn=" + str(rtn))
    return rtn

