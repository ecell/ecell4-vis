# coding: utf-8
"""filesystem_datasource --- plugin for filesystem based Datasource.
"""
import os, glob

# try loading submodules
try:
    import page
except ImportError:
    pass


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
