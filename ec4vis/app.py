# coding: utf-8
"""ec4vis.app -- Visualizer Application.
"""
from os import getcwd

import wx

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, info, logger, DEBUG

from ec4vis.browser import BrowserFrame
from ec4vis.inspector.datasource.page import DatasourceInspectorPage
from ec4vis.pipeline import PipelineTree, UpdateEvent
from ec4vis.plugins import PluginLoader
from ec4vis.version import VERSION


# Application-wide variables
APP_TITLE_NAME = 'E-Cell 4 Data Browser Version %d.%d.%d' %VERSION


class BrowserApp(wx.App):
    """Application object for browser.
    """
    def __init__(self, *args, **kwargs):
        
        # application status
        self.visualizer = None # current visualizer
        self.settings = kwargs.pop('settings', None)
        # create pipeline
        self.pipeline = PipelineTree()
        wx.App.__init__(self, *args, **kwargs)

    def OnInit(self):
        """Integrated initialization hook.
        """
        # initialize UI stuff
        debug('Initializing GUI...') # this won't appear on Console.
        self.init_ui()
        # initialize plugins
        info('Loading plugins...')
        self.init_plugins()
        return True

    def OnExit(self):
        """Integrated finalization hook.
        """
        self.finalize()
        return

    def init_plugins(self):
        """Initialize plugins
        """
        # load plugins
        plugin_loader = PluginLoader()
        for i, (modpath, status) in enumerate(plugin_loader.load_iterative()):
            message = '%s ... %s' %(modpath, 'OK' if status else 'FAILED')
            debug(message)

    def init_ui(self):
        """Initialize UI.
        """
        # browser
        browser = BrowserFrame(None, -1, APP_TITLE_NAME, size=(1000, 600))
        pipeline_panel = browser.pipeline_panel
        pipeline_tree_ctrl = pipeline_panel.tree_ctrl
        # set pipeline to tree
        pipeline_tree_ctrl.pipeline = self.pipeline
        # add datasource inspector.
        inspector_notebook = browser.inspector_panel.notebook
        ds_inspector_page = DatasourceInspectorPage(inspector_notebook, -1)
        ds_inspector_page.target = self.pipeline.root
        def ds_update_handler(node, event):
            ds_inspector_page.update()
        self.pipeline.root.downward_event_handlers.setdefault(UpdateEvent, []).append(ds_update_handler)
        inspector_notebook.AddPage(ds_inspector_page, 'Datasource')
        # outlet bindings
        self.browser = browser
        self.menu_bar = browser.menu_bar
        self.pipeline_panel = browser.pipeline_panel
        # menu event bindings
        def bind_menu(label_attr, handler):
            """Util to bind menu events"""
            self.Bind(wx.EVT_MENU, handler, getattr(self.menu_bar, label_attr))
        bind_menu('app_quit', self.OnAppQuitMenu)
        bind_menu('app_about', self.OnAppAboutMenu)
        # assign and show top window
        self.SetTopWindow(browser)
        self.browser.Show(True)
        debug('init_ui(): browser initialized.')

    def finalize(self):
        """Finalizer.
        """
        # just a placeholder atm.
        # finalize visualizers
        debug('finalized %s' %(self.__class__.__name__))

    def OnAppAboutMenu(self, event):
        """Called on 'App'->'About' menu.
        """
        debug('App::OnAppAboutMenu.')
        dlg = wx.MessageDialog(self.browser, APP_TITLE_NAME,
                               'About this application...', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnAppQuitMenu(self, event):
        """Called on 'App'->'Quit' menu.
        """
        debug('App::OnAppQuitMenu.')
        self.ExitMainLoop()

    def on_datasource_changed(self, page):
        """Hook on datasource change.
        """
        self.pipeline.root.datasource = page.datasource
        debug('on_datasource_changed, uri=%s' %(page.datasource.uri))
        pevent = UpdateEvent(None)
        self.pipeline.propagate(pevent)


if __name__=='__main__':
    app = BrowserApp(0)
    app.MainLoop()
