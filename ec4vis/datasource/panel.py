# coding: utf-8
"""ec4vis.datasource.panel --- Datasource panel in visualizer application.
"""
import wx, wx.aui, wx.lib.newevent

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call, warning
from ec4vis.utils.wx_ import AuiNotebookPlus
from ec4vis.datasource.page import DatasourceChangedEvent, EVT_DATASOURCE_CHANGED


class DatasourceNotebook(AuiNotebookPlus):
    """Notebook in a datasource panel.
    """
    def __init__(self, *args, **kwargs):
        # this should be popped before superclass initializer.
        self.datasource = kwargs.pop('datasource')
        default_style = (wx.aui.AUI_NB_TOP|wx.aui.AUI_NB_TAB_MOVE|
                         wx.aui.AUI_NB_SCROLL_BUTTONS|wx.aui.AUI_NB_CLOSE_BUTTON)
        kwargs['style'] = default_style|kwargs.get('style', 0)
        AuiNotebookPlus.__init__(self, *args, **kwargs)

    def create_page(self, page_class, page_name, datasource=None, **kwargs):
        kwargs['datasource'] = self.datasource
        return AuiNotebookPlus.create_page(self, page_class, page_name, **kwargs)


class DatasourcePanel(wx.Panel):
    """Datasource panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        self.datasource = kwargs.pop('datasource')
        wx.Panel.__init__(self, *args, **kwargs)
        self.notebook = DatasourceNotebook(self, datasource=self.datasource)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnNotebookPageChanged)
        self.Bind(wx.aui.EVT_AUINOTEBOOK_PAGE_CHANGED, self.OnNotebookPageChanged)
        # layout sutff
        sizer = wx.BoxSizer()
        sizer.Add(self.notebook, 1, wx.EXPAND|wx.ALL, 0)
        self.SetSizer(sizer)

    def finalize(self):
        """Finalizer.
        """
        # placeholder atm

    def OnNotebookPageChanged(self, event):
        """Event handler called on notebook change.
        """
        # look for currently selected page
        if self.notebook.selected_page:
            self.notebook.selected_page.update_datasource()
        else:
            # if no page is left
            self.datasource.uri = None
        debug('datasource.uri set to %s' %self.datasource.uri)
        wx.PostEvent(self, DatasourceChangedEvent())


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
            from ec4vis.datasource import Datasource
            from ec4vis.plugins.filesystem_datasource_page import FilesystemDatasourcePage
            frame = wx.Frame(None, -1, u'DatasourcePanel Demo')
            datasource = Datasource()
            datasource_panel = DatasourcePanel(frame, -1, datasource=datasource)
            fs1_id, fs1_page = datasource_panel.notebook.create_page(FilesystemDatasourcePage, 'Filesystem1')
            fs2_id, fs2_page = datasource_panel.notebook.create_page(FilesystemDatasourcePage, 'Filesystem2')
            fs1_page.root_path = ec4vis_test_root
            fs2_page.root_path = ec4vis_test_root
            sizer = wx.BoxSizer()
            sizer.Add(datasource_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.datasource_panel = datasource_panel
            self.Bind(EVT_DATASOURCE_CHANGED, self.OnDatasourceChanged)
            self.SetTopWindow(frame)
            return True

        def OnDatasourceChanged(self, event):
            """Demo handler for DatasourceChagedEvent.
            """
            page = self.datasource_panel.notebook.selected_page
            message = '<Datasource set to None>'
            if page and page.datasource:
                message = page.datasource.uri
            wx.MessageBox(message,  'Datasource panel changed', wx.OK)

    app = App(0)
    app.MainLoop()
