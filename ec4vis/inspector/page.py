# coding: utf-8
"""ec4vis.inspector.page --- Inspector page in visualizer application.
"""
import wx, wx.aui

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug
from ec4vis.inspector import Inspector


class InspectorPage(wx.Panel):
    """Abstract superclass for pages in a inspector notebook.
    """
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        inspector_class = self.get_inspector_class()
        self.inspector = inspector_class()

    def get_inspector_class(self):
        """Returns inspector class. Subclass should override.
        """
        return Inspector


if __name__=='__main__':
    # TBD
    pass
