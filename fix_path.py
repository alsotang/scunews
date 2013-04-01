import os
import sys

isAppend = False


def init():
    if not isAppend:
        global isAppend
        isAppend = True
        sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
