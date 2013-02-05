# coding: utf-8
"""datasource.py --- Datasource abstraction
"""

class Datasource(object):
    """Abstract superclass for datasources.

    Datasource bridges between visualizer and underlying data resource,
    such as files in a filesystem, records in a RDBMS table, live stream
    from a remote server. Datasource always provides URI in any forms.

    - Datasource has a state (current filepath, cursor in a database, etc.)
    - Datasource provides a URI of interest.

    >>> d = Datasource()
    >>> d.uri # yields None
    >>> d.uri = 'file:///foo/bar/baz/'
    >>> d.uri
    'file:///foo/bar/baz/'
    
    """
    def __init__(self, uri=None):
        """Initializer.
        """
        self._uri = uri

    def get_uri(self):
        return self._uri

    def set_uri(self, uri):
        self._uri = uri

    uri = property(get_uri, set_uri)


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)

