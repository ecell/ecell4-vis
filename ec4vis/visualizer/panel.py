# coding: utf-8
"""ec4vis.visualizer.panel --- visualizer panel
"""
import wx, wx.aui

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug
from ec4vis.utils.wx_ import AuiNotebookPlus
from ec4vis.visualizer.vtk3d.page import Vtk3dVisualizerPage


class VisualizerNotebook(AuiNotebookPlus):
    """Notebook in a visualizer panel.
    """
    def __init__(self, *args, **kwargs):
        style = wx.aui.AUI_NB_TOP|wx.aui.AUI_NB_TAB_MOVE
        style |= kwargs.pop('style', 0)
        kwargs['style'] = style
        AuiNotebookPlus.__init__(self, *args, **kwargs)


class VisualizerPanel(wx.Panel):
    """Visualizer panel.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        notebook = VisualizerNotebook(self)
        vtk3d_page = Vtk3dVisualizerPage(notebook, -1)
        notebook.AddPage(vtk3d_page, 'VTK 3D')
        # layout sutff
        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(sizer)
        # bindings
        self.notebook = notebook

    def finalize(self):
        """Finalize panel.
        """
        self.notebook.finalize()

        


if __name__=='__main__':

    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'VisualizerPanel Demo', size=(-1, 600))
            visualizer_panel = VisualizerPanel(frame, -1)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(visualizer_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
