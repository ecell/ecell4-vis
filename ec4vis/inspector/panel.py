# coding: utf-8
"""ec4vis.inspector.panel --- Inspector panel in visualizer application.
"""
import wx

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug
from ec4vis.utils.wx_ import AuiNotebookPlus


class InspectorNotebook(AuiNotebookPlus):
    """Notebook in a inspector panel.
    """
    def __init__(self, *args, **kwargs):
        default_style = (wx.aui.AUI_NB_TOP|wx.aui.AUI_NB_TAB_MOVE|
                         wx.aui.AUI_NB_SCROLL_BUTTONS)
        kwargs['style'] = default_style|kwargs.get('style', 0)
        AuiNotebookPlus.__init__(self, *args, **kwargs)
    

class InspectorPanel(wx.Panel):
    """Inspector panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        notebook = InspectorNotebook(self)
        # layout stuff
        sizer = wx.BoxSizer()
        sizer.Add(notebook, 1, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(sizer)
        # bindings
        self.notebook = notebook
        
    def finalize(self):
        """Finalizer.
        """
        # placeholder atm


if __name__=='__main__':

    from ec4vis.inspector.page import InspectorPage
    
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Inspector Panel Demo')
            inspector_panel = InspectorPanel(frame, -1)
            notebook = inspector_panel.notebook
            page = InspectorPage(notebook)
            notebook.AddPage(page, 'Demo inspector')
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(inspector_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True
    app = App(0)
    app.MainLoop()
