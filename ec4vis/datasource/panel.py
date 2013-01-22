# coding: utf-8
"""ec4vis.datasource.panel --- Datasource panel in visualizer application.
"""
import wx, wx.aui

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug
from ec4vis.datasource.filesystem.page import FilesystemDatasourcePage
from ec4vis.utils.wx_ import AuiNotebookPlus


class DatasourceNotebook(AuiNotebookPlus):
    """Notebook in a datasource panel.
    """
    def __init__(self, *args, **kwargs):
        default_style = (wx.aui.AUI_NB_TOP|wx.aui.AUI_NB_TAB_MOVE|
                         wx.aui.AUI_NB_SCROLL_BUTTONS)
        kwargs['style'] = default_style|kwargs.get('style', 0)
        AuiNotebookPlus.__init__(self, *args, **kwargs)


class DatasourcePanel(wx.Panel):
    """Datasource panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        notebook = DatasourceNotebook(self)
        fs_page = FilesystemDatasourcePage(notebook, -1)
        notebook.AddPage(fs_page, 'Filesystem')
        # layout sutff
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
    
    this_filepath = os.path.abspath(__file__)
    ec4vis_parent = this_filepath[:this_filepath.rindex(os.sep+'ec4vis')]
    ec4vis_test_root = os.path.join(ec4vis_parent, 'tests', 'data', 'fs', 'root')
    
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'DatasourcePanel Demo')
            datasource_panel = DatasourcePanel(frame, -1)
            fs_page = datasource_panel.notebook.find_page('Filesystem')
            if fs_page:
                fs_page.root_path = ec4vis_test_root
            sizer = wx.BoxSizer()
            sizer.Add(datasource_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

        def on_datasource_changed(self, page):
            wx.MessageBox(
                page.datasource.uri, 'Datasource changed', wx.OK)

    app = App(0)
    app.MainLoop()
