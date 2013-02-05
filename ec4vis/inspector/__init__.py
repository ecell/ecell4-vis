# coding: utf-8
"""ec4vis.inspector -- Inspector driver superclass
"""

class Inspector(object):
    """Abstract interface declaration for inspectors.
    """
    def update(self):
        """Called on any changes on target object.

        Subclass should override this method to reflect target changes over the inspector.
        """
        return NotImplemented


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
