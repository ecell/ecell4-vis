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
    
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """

    @property
    def uri(self):
        """Returns URI of the datasource. Subclass must override this.
        """
        return self.get_uri()

    def get_uri(self):
        return NotImplemented


if __name__=='__main__':
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)

