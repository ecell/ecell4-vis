# coding: utf-8
"""ec4vis.datasource.filesystem --- Filesystem based Datasource.
"""
import os, glob

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug
from ec4vis.datasource import Datasource


class FilesystemDatasource(Datasource):
    """Filesystem-based datasource.
    """

    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        Datasource.__init__(self, *args, **kwargs)
        # the content of _path should be empty string (uninitialized) or
        # an absolute path.
        self._path = ''

    def get_path(self):
        """Property getter for path.
        """
        return self._path

    def set_path(self, path):
        """Property setter for path.
        """
        self._path = path

    path = property(get_path, set_path)

    def get_uri(self):
        """Getter for _file_path.
        """
        return 'file://%s' %self.path


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
