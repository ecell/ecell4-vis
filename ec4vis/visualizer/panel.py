# coding: utf-8
"""ec4vis.visualizer.panel --- visualizer panel
"""
import wx, wx.aui

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call
from ec4vis.utils.wx_ import AuiNotebookPlusWithTargetBindingPage


class VisualizerNotebook(AuiNotebookPlusWithTargetBindingPage):
    """Notebook in a visualizer panel.
    """
    def __init__(self, *args, **kwargs):
        style = wx.aui.AUI_NB_TOP|wx.aui.AUI_NB_TAB_MOVE|wx.aui.AUI_NB_CLOSE_BUTTON
        style |= kwargs.pop('style', 0)
        kwargs['style'] = style
        AuiNotebookPlusWithTargetBindingPage.__init__(self, *args, **kwargs)


class VisualizerPanel(wx.Panel):
    """Visualizer panel.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        notebook = VisualizerNotebook(self)
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

    from ec4vis.visualizer.vtk3d import Vtk3dVisualizerNode
    from ec4vis.visualizer.vtk3d.page import Vtk3dVisualizerPage

    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'VisualizerPanel Demo', size=(-1, 600))
            visualizer_panel = VisualizerPanel(frame, -1)
            notebook = visualizer_panel.notebook
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(visualizer_panel, 1, wx.ALL|wx.EXPAND, 5)
            visualizer_node = Vtk3dVisualizerNode()
            notebook.create_page(Vtk3dVisualizerPage, 'VTK 3D', target=visualizer_node)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

    app = App(0)
    app.MainLoop()
