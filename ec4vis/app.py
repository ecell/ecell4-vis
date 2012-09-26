# coding: utf-8
"""app.py -- Visualizer Application implementation by Yasushi Masuda (ymasuda@accense.com)
"""
from logging import debug
from os import getcwd

import wx

from ec4vis.browser import BrowserFrame
from ec4vis.plugins import PluginLoader
from ec4vis.settings import settings
from ec4vis.visualizer import VISUALIZER_CLASSES, VisualizerEventResponder

VERSION = (0, 0, 1)
APP_TITLE_NAME = 'E-Cell 4 Data Browser Version %d.%d.%d' %VERSION


class BrowserApp(wx.App, VisualizerEventResponder):
    """Application object for browser.
    """
    def __init__(self, *args, **kwargs):
        
        # application status
        self.visualizer = None # current visualizer
        self.settings = kwargs.pop('settings', None)
        wx.App.__init__(self, *args, **kwargs)

    def OnInit(self):
        """Integrated initialization hook.
        """
        # initialize plugins
        self.init_plugins()
        # initialize UI stuff
        self.init_ui()
        self.render_window.Render()
        return True

    def init_plugins(self):
        """Initialize plugins
        """
        # load plugins
        plugin_loader = PluginLoader()
        for i, (modpath, status) in enumerate(plugin_loader.load_iterative()):
            message = '%s ... %s' %(modpath, 'OK' if status else 'FAILED')
            # pass

    def init_ui(self):
        """Initialize UI.
        """
        # browser
        browser = BrowserFrame(None, -1, APP_TITLE_NAME, size=(1000, 600))
        workspace_panel = browser.workspace_panel
        renderer_panel = browser.renderer_panel
        render_window = renderer_panel.render_window
        # inspector_panel = browser.inspector_panel # TBD

        # outlet bindings
        self.browser = browser
        self.workspace_panel = workspace_panel
        self.workspace_tree = workspace_panel.tree_ctrl
        self.renderer_panel = renderer_panel
        if self.settings:
            render_window_panel.configure_renderer(self.settings)
        self.render_window = render_window
        self.renderer = renderer_panel.renderer

        # self.inspector_panel = inspector_panel
        
        # # outlet configurations
        # self.sources = []
        # source_model = SourceDataViewModel(self.sources)
        # # data_model = DataDataViewModel([])
        # self.update_visualizer_buttons_status()
        # # self.source_list.AssociateModel(source_model)
        # self.update_source_remove_ui_status()
        # # self.data_list.AssociateModel(data_model)
        # self.update_data_list_buttons_status()

        # menu event bindings
        menu_bar = browser.menu_bar
        app_about = menu_bar.app_about
        app_quit = menu_bar.app_quit
        workspace_set_root = menu_bar.workspace_set_root
        #workspace_save = menu_bar.workspace_save
        #workspace_save_as = menu_bar.workspace_save_as
        #workspace_load = menu_bar.workspace_load
        #workspace_remove = menu_bar.workspace_remove
        #workspace_add_file = menu_bar.workspace_add_file
        #workspace_add_loader = menu_bar.workspace_add_loader
        #workspace_add_visualizer = menu_bar.workspace_add_visualizer
        #workspace_add_filter = menu_bar.workspace_add_filter

        # menu commands
        def menu_bind(handler, menu):
            browser.Bind(wx.EVT_MENU, handler, menu)
        menu_bind(self.OnAppAboutMenu, app_about)
        menu_bind(self.OnAppQuitMenu, app_quit)
        menu_bind(self.OnWorkspaceSetRootMenu, workspace_set_root)
        #menu_bind(self.OnWorkspaceLoadMenu, workspace_load)
        #menu_bind(self.OnWorkspaceSaveMenu, workspace_save)
        #menu_bind(self.OnWorkspaceSaveAsMenu, workspace_save_as)
        #menu_bind(self.OnWorkspaceAddFileMenu, workspace_add_file)
        #menu_bind(self.OnWorkspaceAddFileMenu, workspace_add_file)

        # renderer event binding --- this is a bad hack
        def render_window_render_observer(o, e, f=renderer_panel):
            # hasattr() is to prevent AttributeError.
            """ # This is kept for demonstration use.
            if hasattr(self, 'visualizer'):
                if self.visualizer:
                    self.visualizer.update()"""
            pass
        self.render_window.AddObserver(
            "RenderEvent", render_window_render_observer)

        # assign and show top window
        self.SetTopWindow(browser)
        self.browser.Show(True)

    def finalize(self):
        """Finalizer.
        """
        pass # just a placeholder now.

    def OnAppAboutMenu(self, event):
        """Called on 'App'->'About' menu.
        """
        dlg = wx.MessageDialog(self.browser, APP_TITLE_NAME,
                               'About this application...', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnAppQuitMenu(self, event):
        """Called on 'App'->'Quit' menu.
        """
        self.finalize()
        self.ExitMainLoop()

    def OnWorkspaceSetRootMenu(self, evt):
        """Called on 'Workspace'->'Set Root Direcotry...' menu.
        """
        # TBD: save current workspace to file.
        dlg = wx.DirDialog(
            self.browser,
            u'Choose root directory for workspace',
            style=wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST|wx.DD_CHANGE_DIR)
        ret = dlg.ShowModal()
        if ret==wx.ID_OK:
            dirname = dlg.GetPath()
            # TBD: set directory
            self.workspace_tree.set_root_directory(dirname)
            

#     def OnWorkspaceLoadMenu(self, evt):
#         """Called on 'Workspace'->'Load workspace' menu.
#         """
#         # TBD: save current workspace to file.
#         dlg = wx.FileDialog(
#             self.browser,
#             u'Choose workspace file to load',
#             style=wx.OPEN, defaultDir=getcwd())
#         ret = dlg.ShowModal()
#         if ret==wx.ID_OK:
#             filename = dlg.GetPath()
#         # TBD: saving mechanism
            
#     def OnWorkspaceSaveMenu(self, evt):
#         """Called on 'Workspace'->'Save workspace' menu.
#         """
#         # TBD: save current workspace to file.
            
#     def OnWorkspaceSaveAsMenu(self, evt):
#         """Called on 'Workspace'->'Save workspace as...' menu.
#         """
#         # TBD: save current workspace to file.
#         dlg = wx.FileDialog(
#             self.browser,
#             u'Choose workspace file to save',
#             style=wx.SAVE, defaultDir=getcwd())
#         ret = dlg.ShowModal()
#         if ret==wx.ID_OK:
#             filename = dlg.GetPath()
#         # TBD: saving mechanism
            
#     def OnWorkspaceAddFileMenu(self, evt):
#         """Called on 'Workspace'->'Add file...' menu.
#         """
#         dlg = wx.DirDialog(
#             self.browser,
#             u'Choose data directory',
#             style=wx.DD_DEFAULT_STYLE|wx.DD_DIR_MUST_EXIST|wx.DD_CHANGE_DIR)
#         ret = dlg.ShowModal()
#         if ret==wx.ID_OK:
#             dirname = dlg.GetPath()
            

    def update_visualizer_buttons_status(self):
        """Updates enable/disable status of Reset/Configure buttons.
        """
        visualizer = self.visualizer
        can_reset = not (visualizer is None)
        has_config_ui = bool(visualizer) and visualizer.has_configuration_ui
        # self.visualizer_reset_button.Enable(can_reset)
        self.visualizer_configure_button.Enable(has_config_ui)

    def update_source_remove_ui_status(self):
        """Updates enable/disable status of UIs related removing source.
        """
        if False:
            selected = self.source_list.GetSelection()
            self.source_remove_button.Enable(bool(selected))

    def update_data_list_buttons_status(self):
        """Updates enable/disable status of UIs related removing source.
        """
        data_list = self.data_list 
        model = data_list.GetModel()
        selected = data_list.GetSelection()
        # this is hack: wxPython's DVLC lacks way-to-count-rows or something.
        n_rows = 0
        selected_row = wx.NOT_FOUND
        if selected and self.visualizer:
            # this is dirty because DVLC lacks functionality to count rows.
            selected_data_id = model.GetValue(selected, 0)
            data_objects = self.visualizer.data_objects
            n_rows = len(data_objects)
            for row_id, info in enumerate(data_objects):
                if selected_data_id==info[0]:
                    selected_row = row_id
                    break
        self.data_up_button.Enable(bool(selected and selected_row>0))
        self.data_down_button.Enable(bool(selected and (0<=selected_row<(n_rows-1))))

    def do_process_sources(self):
        self.visualizer.process_sources([uri for use, uri in self.sources])
        data_objects = self.visualizer.data_objects
        data_list = self.data_list
        new_data_model = DataDataViewModel(data_objects)
        new_data_model.AfterReset()
        old_data_model = data_list.GetModel()
        data_list.AssociateModel(new_data_model)
        del old_data_model

    def OnVisualizerResetButton(self, event):
        """Handles visualizer 'Reset' button.
        """
        if self.visualizer is None:
            return
        self.visualizer.reset()
        self.do_process_sources()

    def OnVisualizerConfigureButton(self, event):
        """Handles visualizer 'Configure' button.
        """
        self.visualizer.load_configuration_ui()

    def OnSourceAddButton(self, event):
        """Called on Add source boutton.
        """
        self.add_file_source()

    def OnSourceRemoveButton(self, event):
        """Called on Add source boutton.
        """
        selected = self.source_list.GetSelection()
        if selected:
            selected_uri = self.source_list.GetModel().GetValue(selected, 1)
            popped = None
            for i, (use, uri) in enumerate(self.sources):
                if uri==selected_uri:
                    popped = self.sources.pop(i)
                    break
            if popped:
                # this is required for yielding
                self.source_list.GetModel().AfterReset()
        self.update_source_remove_ui_status()

    def OnVisualizerChoice(self, event):
        """Called on selection of visualizer_choice changed.
        """
        selected_idx = event.GetSelection()
        if selected_idx: # not 'Select Visualizer'
            key = event.GetString()
            visualizer_class = VISUALIZER_CLASSES[key]
        else:
            visualizer_class = None
        if self.visualizer.__class__==visualizer_class:
            # do nothing if visualizer class not chaged
            return
        # detach old visualizer from application
        old_visualizer, self.visualizer = self.visualizer, None
        if old_visualizer:
            old_visualizer.finalize()
            del old_visualizer
        if visualizer_class:
            # attach new visualizer to application
            new_visualizer = visualizer_class(self, self.renderer)
            new_visualizer.initialize() # implies show()
            self.visualizer = new_visualizer
            self.do_process_sources()
            self.render_window.Render()
        self.update_visualizer_buttons_status()
        
    def OnSourceListSelectionChanged(self, event):
        """Called on selection of soruce list changed.
        """
        self.update_source_remove_ui_status()

    def OnDataListSelectionChanged(self, event):
        """Called on selection of data list changed.
        """
        model = self.data_list.GetModel()
        if model is None:
            return
        selected = self.data_list.GetSelection()
        data_id = model.GetValue(selected, 0)
        if self.visualizer is None:
            return
        self.visualizer.update(data_id)
        self.render_window.Render()
        self.update_data_list_buttons_status()

    def move_current_data(self, offset):
        """Do real job for OnDataUp/DownButton.
        """
        model = self.data_list.GetModel()
        if model is None:
            return
        selected = self.data_list.GetSelection()
        if selected is None:
            return
        if self.visualizer is None:
            return
        data_id = model.GetValue(selected, 0)
        self.visualizer.move_data_ordering(data_id, offset)
        # model.ValueChanged()
        model.AfterReset() # yield
            
    def OnDataUpButton(self, event):
        """Called on data list up button.
        """
        self.move_current_data(-1)
        
    def OnDataDownButton(self, event):
        """Called on data list down button.
        """
        self.move_current_data(+1)

    # Visualizer Event Responder methods
    def get_ui_root(self):
        # just returns browser as toplevel window
        return self.browser

    def process_sources_start(self, sender, sources):
        # show data-loading dialog
        if self.data_loader_dialog is None:
            self.data_loader_dialog = wx.ProgressDialog(
                u'Loading data...',
                u'',
                maximum=len(sources),
                parent=self.browser,
            style=wx.PD_AUTO_HIDE)
    
    def process_sources_done(self, sender, sources):
        # withdraw data-loading dialog
        if self.data_loader_dialog:
            self.data_loader_dialog.Destroy()
            wx.Yield()
            self.data_loader_dialog = None

    def process_source_done(self, sender, source, error):
        # update data-loading dialog
        print error
        if self.data_loader_dialog is None:
            return
        sources = [uri for use, uri in self.sources]
        if source in sources:
            index = sources.index(source)
            message = 'Processing %s ... %s' %(source, 'OK' if (error is None) else 'FAILED')
            self.data_loader_dialog.Update(index, message)
        

if __name__=='__main__':
    app = BrowserApp(0)
    app.MainLoop()
