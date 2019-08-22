"""Helper functions for debugging.

   JeremyC 28-05-2018
"""

import xbmcgui

def debug(str1, str2):
    # Display pop-up dialog.
    # Note: I do not see a way to increase the dialog size, or reduce the
    #       text size, so instead we convert our string to display into a
    #       multi-line string. Then we can at least see all of it!
    str_multiline = ""
    count = 0
    for c in str2:
        str_multiline = str_multiline + c
        count = count + 1
        if (count % 50 == 0):
            str_multiline = str_multiline + "\n"

        xbmcgui.Dialog().ok(str1, str_multiline)

        # We will also log to /storage/.kodi/temp/kodi.log
        print("JCDC: str1=" + str1 + ", str2=" + str2)

