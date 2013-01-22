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


class InspectorPage(wx.Panel):
    """Abstract superclass for pages in a inspector notebook.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.target = None # target object

    def update(self):
        """Update UI to reflect target status. Subclass should override.
        """
        pass

if __name__=='__main__':
    # TBD
    pass
