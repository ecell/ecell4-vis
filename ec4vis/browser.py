# coding: utf-8
"""browser.py -- Browser window in visualizer application
"""
from logging import debug

import wx
import wx.aui
from ec4vis import *

from renderer_panel import RendererPanel
from workspace_panel import WorkspacePanel
from pipeline_panel import PipelinePanel
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
        # pipeline panel
        pipeline_panel = PipelinePanel(self, -1)
        # renderer panel
        renderer_panel = RendererPanel(self, -1)
        # inspector panel
        inspector_panel = InspectorPanel(self, -1)
        # menu
        menu_bar = AppMenuBar(self)
        # aui manager
        aui_manager = wx.aui.AuiManager()
        aui_manager.SetManagedWindow(self)
        aui_manager.AddPane(pipeline_panel,
                            wx.aui.AuiPaneInfo()
                            .Name('pipeline')
                            .Caption('Pipeline')
                            .BestSize((200, -1))
                            .Left())
        aui_manager.AddPane(workspace_panel,
                            wx.aui.AuiPaneInfo()
                            .Name('workspace')
                            .Caption('Workspace')
                            .Left())
        aui_manager.AddPane(wx.Panel(self, -1),
                            wx.aui.AuiPaneInfo()
                            .Name('console')
                            .Caption('Console')
                            .BestSize((-1, 100))
                            .Bottom())
        aui_manager.AddPane(renderer_panel,
                            wx.aui.AuiPaneInfo()
                            .Name('vtk window')
                            .Caption('Particles preview')
                            .Center())
        aui_manager.AddPane(inspector_panel,
                            wx.aui.AuiPaneInfo()
                            .Name('inspector')
                            .Caption('Inspector')
                            .BestSize((200, -1))
                            .Right())
        aui_manager.Update()
        # bindings
        self.aui_manager = aui_manager
        self.workspace_panel = workspace_panel
        self.renderer_panel = renderer_panel
        # self.inspector_panel = inspector_panel
        self.menu_bar = menu_bar

    def OnClose(self, evt):
        self.aui_manager.UnInit()
        del self.aui_manager
        self.Destroy()


if __name__=='__main__':
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = BrowserFrame(None, -1, u'Browser Frame Demo')
            frame.Show(True)
            # frame.aui_manager.Upodate()
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
