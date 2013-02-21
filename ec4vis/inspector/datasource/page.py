# coding: utf-8
"""ec4vis.inspector.page --- Built-in datasource (pipeline root node) inspector.
"""
import wx, wx.aui

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call
from ec4vis.inspector.page import InspectorPage, register_inspector_page


class DatasourceInspectorPage(InspectorPage):
    """Datasource inspector page.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        InspectorPage.__init__(self, *args, **kwargs)
        label = wx.StaticText(self, -1, 'URI')
        text = wx.TextCtrl(self, -1, '', style=wx.TE_READONLY)
        self.uri_text = text
        h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        h_sizer.Add(label, 0, wx.EXPAND|wx.ALL, 0)
        h_sizer.Add(text, 1, wx.EXPAND|wx.ALL, 0)
        # self.sizer comes from parent.
        self.sizer.Add(h_sizer, 0, wx.EXPAND|wx.ALL, 10)

    def update(self):
        """Update UI.
        """
        if (self.target and hasattr(self.target, 'datasource')
            and self.target.datasource.uri):
            self.uri_text.SetValue(self.target.datasource.uri)
        else:
            self.uri_text.SetValue('')
        

register_inspector_page('RootPipelineNode', DatasourceInspectorPage)
    

if __name__=='__main__':
    # TBD
    pass

