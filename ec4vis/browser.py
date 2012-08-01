# coding: utf-8
"""browser.py -- Browser window in visualizer application
"""
from logging import debug

import wx
from ec4vis import *

from renderer_panel import RendererPanel
from workspace_panel import WorkspacePanel
from inspector_panel import InspectorPanel
from menu_bar import AppMenuBar
        

class BrowserFrame(wx.Frame):
    """Browser window.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Frame.__init__(self, *args, **kwargs)
        # workspace panel
        workspace_panel = WorkspacePanel(self, -1)
        # renderer panel
        renderer_panel = RendererPanel(self, -1)
        # inspector panel
        # inspector_panel = InspectorPanel(self, -1)
        # menu
        menu_bar = AppMenuBar(self)
        # bindings
        self.workspace_panel = workspace_panel
        self.renderer_panel = renderer_panel
        # self.inspector_panel = inspector_panel
        self.menu_bar = menu_bar
        # sizer
        root_sizer = wx.BoxSizer(wx.HORIZONTAL)
        root_sizer.Add(workspace_panel, 0, wx.ALL|wx.EXPAND, 0)
        root_sizer.Add(renderer_panel, 1, wx.ALL|wx.EXPAND, 0)
        # root_sizer.Add(inspector_panel, 0, wx.ALL|wx.EXPAND, 0)
        self.SetSizer(root_sizer)
        self.Layout()


if __name__=='__main__':
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = BrowserFrame(None, -1, u'Browser Frame Demo')
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
