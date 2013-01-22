# coding: utf-8
"""file_group.py --- represents a group of file (in a directory).
"""
from glob import glob
from os.path import exists

from workspace import WorkspaceEntity


class FileGroup(WorkspaceEntity):
    """Represents a group of file (in a directory).

    >>> fg = FileGroup()
    >>> fg.label
    u'FileGroup'
    >>> fg.directory # returns None
    >>> fg.props
    {'directory': None}
    >>> fg.is_valid
    False
    >>> from os.path import abspath, dirname
    >>> fg.directory = dirname(abspath('.')) # this directory should exist
    >>> fg.is_valid
    True
    
    """
    def __init__(self, label='FileGroup', **props):
        """Initializer.
        """
        WorkspaceEntity.__init__(self, label, **props)
        self.props.setdefault('directory', None)

    def _get_directory(self):
        return self.props['directory']

    def _set_directory(self, directory):
        self.props['directory'] = directory

    directory = property(_get_directory, _set_directory)
    
    def do_is_valid(self):
        return (bool(self.directory) and exists(self.directory))

    def list_files(self):
        return glob(self.directory)


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
