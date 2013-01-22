# coding: utf-8
"""loader.py --- represents a file laader.
"""
from workspace import WorkspaceEntity


class Loader(WorkspaceEntity):
    """Represents a file loader.
    """
    def __init__(self, label='Loader', **props):
        """Initializer.
        """
        WorkspaceEntity.__init__(self, label, **props)
        self.props.setdefault('input', None)

    def do_is_valid(self):
        return (bool(self.directory) and exists(self.directory))

    def list_files(self):
        return glob(self.directory)


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
