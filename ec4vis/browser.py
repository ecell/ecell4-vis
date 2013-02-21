# coding: utf-8
"""ec4vis.browser -- Browser window in visualizer application
"""

import wx
import wx.aui

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, info, logger, DEBUG, log_call
from ec4vis.console.panel import ConsolePanel
from ec4vis.datasource.panel import DatasourcePanel
from ec4vis.inspector.panel import InspectorPanel
from ec4vis.pipeline.panel import PipelinePanel
from ec4vis.visualizer.panel import VisualizerPanel
from ec4vis.menu_bar import AppMenuBar
        

def pane_info(caption):
    """Utility to create common pane info.
    """
    return (wx.aui.AuiPaneInfo()
            .Name(caption.lower())
            .Caption(caption)
            .CloseButton(False)
            .Floatable(False))


class BrowserFrame(wx.Frame):
    """Browser window.

    Window layout:
    
    +------------+------------+-----------+
    |            |            |           |
    | (LEFT)     |            |           |
    | Datasource |            |           |
    | Panel      |            |           |
    |            | (CENTER)   | (RIGHT)   |
    +------------+ Visualizer | Inspector |
    |            | Panel      | Panel     |
    | (LEFT)     |            |           |
    | Pipeline   |            |           |
    | Panel      |            |           |
    |            |            |           |
    +-------------------------------------+
    |       (BOTTOM) Console Panel        |
    +-------------------------------------+
    
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        # this should be before superclass initializer.
        pipeline = kwargs.pop('pipeline')
        wx.Frame.__init__(self, *args, **kwargs)
        datasource = pipeline.root.datasource
        # datasource panel
        datasource_panel = DatasourcePanel(self, -1, datasource=datasource)
        # pipeline panel
        pipeline_panel = PipelinePanel(self, -1)
        # visualizer panel
        visualizer_panel = VisualizerPanel(self, -1)
        # inspector panel
        inspector_panel = InspectorPanel(self, -1)
        # console panel
        console_panel = ConsolePanel(self, -1)
        # menu
        menu_bar = AppMenuBar(self)
        # aui manager
        aui_manager = wx.aui.AuiManager()
        aui_manager.SetManagedWindow(self)
        for panel, name, bestsize, layout in [
            (pipeline_panel, 'Pipeline', (300, -1), 'Left'),
            (datasource_panel, 'Datasource', None, 'Left'),
            (console_panel, 'Console', (-1, 100), 'Bottom'),
            (visualizer_panel, 'Visualizer', None, 'Center'),
            (inspector_panel, 'Inspector', (300, -1), 'Right')]:
            pinfo = pane_info(name)
            if bestsize:
                pinfo = pinfo.BestSize(bestsize)
            if layout:
                pinfo = getattr(pinfo, layout)()
            aui_manager.AddPane(panel, pinfo)
        aui_manager.Update()
        # bindings
        self.menu_bar = menu_bar
        self.datasource_panel = datasource_panel
        self.pipeline_panel = pipeline_panel
        self.visualizer_panel = visualizer_panel
        self.inspector_panel = inspector_panel
        self.console_panel = console_panel
        self.aui_manager = aui_manager
        # event bindings
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def finalize(self):
        """Finalizer.
        """
        for subwidget in [self.menu_bar,
                          self.datasource_panel,
                          self.pipeline_panel,
                          self.visualizer_panel,
                          self.inspector_panel,
                          self.console_panel]:
            subwidget.finalize()
        self.aui_manager.UnInit()
        del self.aui_manager
        
    def OnClose(self, evt):
        """Make sure to destroy aui_manager, otherwise it crashes.
        """
        app = wx.GetApp()
        closing_hook = getattr(app, 'OnBrowserClosing')
        if closing_hook:
            closing_hook(evt)
        self.finalize()
        self.Destroy()


if __name__=='__main__':

    this_filepath = os.path.abspath(__file__)
    ec4vis_parent = this_filepath[:this_filepath.rindex(os.sep+'ec4vis')]
    ec4vis_test_root = os.path.join(ec4vis_parent, 'tests', 'data', 'fs', 'root')

    from ec4vis.datasource import Datasource
    from ec4vis.pipeline import PipelineTree
    
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            datasource = Datasource()
            pipeline = PipelineTree(datasource=datasource)
            frame = BrowserFrame(None, -1, u'Browser Frame Demo', size=(1200, 800), pipeline=pipeline)
            frame.Show(True)
            
            # frame.aui_manager.Upodate()
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
