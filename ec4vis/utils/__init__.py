# coding: utf-8
"""Various utilities.
"""
import os

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])
import ec4vis

PACKAGE_PATH = os.path.dirname(os.path.abspath(ec4vis.__file__))
RESOURCES_PATH = os.path.join(PACKAGE_PATH, 'resources')



