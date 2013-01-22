# coding: utf-8
"""ec4vis.visualizer -- visualizer class.
"""

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, info, logger, DEBUG


class Visualizer(object):
    """Abstract superclass for visualizer.
    """
    def finalize(self):
        """Finalize visualizer. Subclass may *extend* this.
        """
        debug('finalized %s' %(self.__class__.__name__))
