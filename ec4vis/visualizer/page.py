# coding: utf-8
"""ec4vis.visuaizer.page --- Visualizer panel in visualizer application.
"""
import wx, wx.aui

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug
from ec4vis.visualizer import Visualizer


class VisualizerPage(wx.Panel):
    """Abstract superclass for pages in a visualizer notebook.
    """
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        visualizer_class = self.get_visualizer_class()
        self.visualizer = visualizer_class()

    def get_visualizer_class(self):
        """Returns visualizer class. Subclass should override.
        """
        return Visualizer

    def finalize(self):
        """Finalize visualizer page (and its visualizer).
        """
        if self.visualizer:
            self.visualizer.finalize()
        debug('finalized %s' %(self.__class__.__name__))


if __name__=='__main__':
    # TBD
    pass
