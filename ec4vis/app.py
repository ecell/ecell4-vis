# coding: utf-8
"""ec4vis.app -- Visualizer Application.
"""
from os import getcwd, getenv

import wx

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, info, logger, DEBUG, log_call

from ec4vis.browser import BrowserFrame
from ec4vis.datasource import Datasource
from ec4vis.datasource.page import DATASOURCE_PAGE_REGISTRY, EVT_DATASOURCE_CHANGED
from ec4vis.datasource.add_dialog import AddDatasourceDialog
from ec4vis.inspector.page import INSPECTOR_PAGE_REGISTRY
from ec4vis.inspector.datasource.page import DatasourceInspectorPage
from ec4vis.pipeline import PipelineTree, UpdateEvent, PIPELINE_NODE_REGISTRY
from ec4vis.pipeline.add_dialog import AddPipelineNodeDialog
from ec4vis.plugins import PluginLoader
from ec4vis.registry import Registry
from ec4vis.visualizer.page import VISUALIZER_PAGE_REGISTRY
from ec4vis.version import VERSION


# Application-wide variables
APP_TITLE_NAME = 'E-Cell 4 Data Browser Version %d.%d.%d' %VERSION


class BrowserApp(wx.App):
    """Application object for browser. 
    """
    def __init__(self, *args, **kwargs):
        
        # application status
        self.registry = Registry(kwargs.pop('registry_home', None), create=True)
        # create datasource
        self.datasource = Datasource()
        # create pipeline
        self.pipeline = PipelineTree(datasource=self.datasource)
        # let super's __init__ call OnInit()
        wx.App.__init__(self, *args, **kwargs)

    # wx built-in Event handlers
    def OnInit(self):
        """Integrated initialization hook.
        """
        # initialize UI stuff
        self.init_ui()
        # initialize plugins
        info('Loading plugins...')
        self.init_plugins()
        self.post_init_setup()
        return True

    def OnExit(self):
        """Integrated finalization hook.
        """
        debug('BrowserApp.OnExit')
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
        """Initializes UI.
        """
        # browser
        self.init_browser()
        # menu
        self.init_menu()
        # pipeline panel
        self.init_pipeline_panel()
        # datasource panel
        self.init_datasource_panel()
        # inspector panel
        self.init_inspector_panel()
        # visualizer panel
        self.init_visualizer_panel()
        # assign and show top window
        self.SetTopWindow(self.browser)
        self.browser.Show(True)

    def init_browser(self):
        """Initializes browser frame.
        """
        browser = BrowserFrame(None, -1, APP_TITLE_NAME, size=(1000, 600), pipeline=self.pipeline)
        # bidings
        self.browser = browser

    def init_pipeline_panel(self):
        """Initializes pipeline panel.
        """
        pipeline_panel = self.browser.pipeline_panel
        pipeline_tree_ctrl = pipeline_panel.tree_ctrl
        pipeline_tree_menu = pipeline_tree_ctrl.tree_menu
        add_node_menu_id = pipeline_tree_menu.add_node_menu_id
        delete_node_menu_id = pipeline_tree_menu.delete_node_menu_id
        show_inspector_menu_id = pipeline_tree_menu.show_inspector_menu_id
        show_visualizer_menu_id = pipeline_tree_menu.show_visualizer_menu_id
        # bind pipeline
        pipeline_tree_ctrl.pipeline = self.pipeline
        # event bindings
        pipeline_tree_ctrl.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnPipelineTreeSelChanged)
        pipeline_tree_ctrl.Bind(wx.EVT_TREE_ITEM_MENU, self.OnPipelineTreeItemMenu)
        pipeline_tree_ctrl.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnPipelineShowObserversMenu)
        pipeline_tree_ctrl.Bind(wx.EVT_MENU, self.OnPipelineAddNodeMenu, add_node_menu_id)
        pipeline_tree_ctrl.Bind(wx.EVT_MENU, self.OnPipelineDeleteNodeMenu, delete_node_menu_id)
        pipeline_tree_ctrl.Bind(wx.EVT_MENU, self.OnPipelineShowInspectorMenu, show_inspector_menu_id)
        pipeline_tree_ctrl.Bind(wx.EVT_MENU, self.OnPipelineShowVisualizerMenu, show_visualizer_menu_id)
        # outlet bindings
        self.pipeline_panel = pipeline_panel
        self.pipeline_tree_ctrl = pipeline_tree_ctrl
        self.pipeline_tree_menu = pipeline_tree_menu
        # make sure that root node is selected.
        pipeline_tree_ctrl.Unselect()

    def init_datasource_panel(self):
        """Initializes datasource panel.
        """
        datasource_panel = self.browser.datasource_panel
        # event bindings
        self.Bind(EVT_DATASOURCE_CHANGED, self.OnDatasourceChanged)
        # outlet bindings
        self.datasource_panel = datasource_panel

    def init_inspector_panel(self):
        """Initializes inspector panel.
        """
        inspector_panel = self.browser.inspector_panel
        # add datasource inspector
        inspector_notebook = inspector_panel.notebook
        root_node = self.pipeline.root
        # event bindings
        # outlet bindings
        self.inspector_panel = inspector_panel
        self.inspector_notebook = inspector_notebook

    def init_visualizer_panel(self):
        """Initializes visualizer panel.
        """
        visualizer_panel = self.browser.visualizer_panel
        visualizer_notebook = visualizer_panel.notebook
        # event bindings
        # outlet bindings
        self.visualizer_panel = visualizer_panel
        self.visualizer_notebook = visualizer_notebook
        
    def init_menu(self):
        """Initializes application menu.
        """
        browser = self.browser
        menu_bar = browser.menu_bar
        # menu event bindings
        def bind_menu(label_attr, handler):
            """Util to bind menu events"""
            browser.Bind(wx.EVT_MENU, handler, getattr(menu_bar, label_attr))
        bind_menu('app_quit', self.OnAppQuitMenu)
        bind_menu('app_about', self.OnAppAboutMenu)
        bind_menu('datasource_add', self.OnDatasourceAddMenu)
        bind_menu('datasource_remove', self.OnDatasourceRemoveMenu)
        bind_menu('pipeline_add_node', self.OnPipelineAddNodeMenu)
        # outlet bindings
        self.menu_bar = menu_bar

    def post_init_setup(self):
        """The last phase of initialization.
        """
        # load datasources
        ds_registry = self.registry.load_section('datasources')
        for label_name, ds_name, ds_info in ds_registry.get('pages', []):
            page_class = DATASOURCE_PAGE_REGISTRY.get(ds_name, None)
            if page_class is None:
                wx.MessageBox('Page Type not found: %s' %ds_name, 'Error')
            idx, page = self.datasource_panel.notebook.create_page(page_class, label_name)
            page.restore(ds_info)
        # load pipeline
        pl_registry = self.registry.load_section('pipeline')
        tree_info = pl_registry.get('tree', None)
        if tree_info:
            self.pipeline.restore(tree_info)
            self.pipeline_tree_ctrl.rebuild_root()
            self.pipeline_tree_ctrl.ExpandAll()

    def finalize(self):
        """Finalizer.
        """
        # finalize visualizers
        debug('finalized %s' %(self.__class__.__name__))
        # close registry
        self.registry.close()

    # In-app convenient properties

    @property
    def current_datasource_page(self):
        """Returns currently selected Datasource Page.
        """
        return self.datasource_panel.notebook.selected_page

    @property
    def current_visualizer_page(self):
        """Returns currently selected Visualzier Page.
        """
        return None

    @property
    def current_visualizer(self):
        """Returns Visualizer for selected Visualzier Page.
        """
        if self.current_visualizer_page:
            return self.current_visualizer_page.visualizer
        return None

    @property
    def current_pipeline_node_info(self):
        """Returns a tuple of tree item id and node object for for currently selected Pipeline Node.
        """
        selected_tree_item_id = self.pipeline_tree_ctrl.selected_tree_item_id
        if selected_tree_item_id:
            return (selected_tree_item_id, self.pipeline_tree_ctrl.GetPyData(selected_tree_item_id))
        # otherwise
        return (None, None)
    
    @property
    def current_inspector_page(self):
        """Returns currently selected Inspector Page.
        """
        return None
    
    @property
    def current_inspector(self):
        """Returns Inspector for currently selected Inspector Page.
        """
        if self.current_inspector_page:
            return self.current_inspector_page.inspector
        return None

    def OnBrowserClosing(self, event):
        """Hook from browser on closing.
        """
        # save datasource panel.
        ds_registry = self.registry.load_section('datasources')
        ds_notebook = self.datasource_panel.notebook
        ds_pages_info = []
        for page_index in range(ds_notebook.GetPageCount()):
            page = ds_notebook.GetPage(page_index)
            label = ds_notebook.GetPageText(page_index)
            for name, cls in DATASOURCE_PAGE_REGISTRY.items():
                if cls==page.__class__:
                    ds_pages_info.append((label, name, page.save()))
            debug('saving page %s' % [label, name, page.save()])
        ds_registry['pages'] = ds_pages_info

        # save pipeline
        pl_registry = self.registry.load_section('pipeline')
        pl_registry['tree'] = self.pipeline.save()

        # self.registry.sync()

    def OnDatasourceRemoveMenu(self, event):
        """Called on 'Datasource' -> 'Remove' menu.
        """
        selected_page_index = self.datasource_panel.notebook.destroy_selected_page()
        if selected_page_index is wx.NOT_FOUND:
            wx.MessageBox('Select any datasource page first.', 'Invalid operation')

    def OnDatasourceAddMenu(self, event):
        """Called on 'Datasource'->'Add...' menu.
        """
        debug('Available datasource page types: %s' %DATASOURCE_PAGE_REGISTRY.keys())
        dlg = AddDatasourceDialog(self.browser, choices=sorted(DATASOURCE_PAGE_REGISTRY.keys()))
        if dlg.ShowModal()==wx.ID_OK:
            label_name = dlg.label_name
            page_class = DATASOURCE_PAGE_REGISTRY.get(dlg.datasource_name, None)
            debug('Got %s as %s' %(page_class.__name__, label_name))
            if page_class is None:
                wx.MessageBox('Page Type not found: %s' %dlg.datasource_name, 'Error')
            # load new dialog page
            self.datasource_panel.notebook.create_page(page_class, label_name)
        dlg.Destroy()

    def check_pipeline_node_selected(self):
        """Show alert if no pipeline node is selected, returning True. Otherwise False.
        """
        selected_tree_item_id, selected_node = self.current_pipeline_node_info
        debug('current_pipeline_node is %s' %selected_node)
        if selected_node is None:
            wx.MessageBox('No node is selected.', 'Invalid operation.')
        return  selected_tree_item_id, selected_node

    def OnPipelineAddNodeMenu(self, event):
        """Called on 'Pipeline'->'Add Node...' menu.
        """
        # If current pipeline node is set to None, do nothing and return.
        parent_tree_item_id, parent_node = self.check_pipeline_node_selected()
        if parent_node is None:
            return
        # else --
        # check spec for parent_node
        node_class_choices = [
            node_name
            for node_name, node_class
            in PIPELINE_NODE_REGISTRY.items()
            if set(node_class.class_input_spec()).issubset(parent_node.output_spec)]
        dlg = AddPipelineNodeDialog(self.browser, choices=node_class_choices)
        new_node = None
        if dlg.ShowModal()==wx.ID_OK:
            label_name = dlg.label_name
            node_class = PIPELINE_NODE_REGISTRY.get(dlg.node_name, None)
            if node_class is None:
                wx.MessageBox('Node Type not found: %s' %dlg.node_name, 'Error')
                return
            # create new node and connect to parent
            new_node = node_class(name=label_name)
            new_node.connect(parent_node)
            # rebuild tree
            self.pipeline_tree_ctrl.rebuild_tree(parent_tree_item_id)
            self.pipeline_tree_ctrl.Expand(parent_tree_item_id)
        dlg.Destroy()

    def OnPipelineDeleteNodeMenu(self, event):
        """Called on 'Pipeline'->'Delete Node...' menu.
        """
        # If current pipeline node is set to None, do nothing and return.
        selected_tree_item_id, selected_node = self.check_pipeline_node_selected()
        if selected_node is None:
            return
        elif selected_tree_item_id==self.pipeline_tree_ctrl.GetRootItem():
            wx.MessageBox('Cannot delete root node.', 'Invalid operation')
            return
        # here, selected_node is proved to have some parent.
        selected_pipeline_node = self.pipeline_tree_ctrl.GetPyData(selected_tree_item_id)
        # else -
        debug('current_pipeline_node is %s' %selected_node)
        # destroy selected node
        # phase 1: collect target data
        targets_to_be_destroyed = self.pipeline_tree_ctrl.get_subtree_data(selected_tree_item_id)
        # phase 2: destroy inspectors/visualizers bound to those targets
        debug('Destroying targets: %s' %targets_to_be_destroyed)
        for target in targets_to_be_destroyed:
            self.inspector_notebook.destroy_page_for_target(target)
            self.visualizer_notebook.destroy_page_for_target(target)
        # phase 3: cull pipeline subtree
        selected_pipeline_node.disconnect()
        # phase 4: rebuild tree
        self.pipeline_tree_ctrl.rebuild_parent(selected_tree_item_id)
        # phase 5: delete pipeline node
        del selected_pipeline_node

    def OnPipelineShowInspectorMenu(self, event):
        """Called on 'Pipeline'->'Show Inspector...' menu.
        """
        # If current pipeline node is set to None, do nothing and return.
        selected_tree_id, selected_node = self.check_pipeline_node_selected()
        if selected_node is None:
            return
        # else -- 
        debug('current_pipeline_node is %s' %selected_node)
        # If there are already corresponding inspector, just focus it.
        inspector_page_index, inspector_page_instance = self.inspector_notebook.find_page_for_target(selected_node)
        if inspector_page_index is None:
            debug('No page exists, trying')
            # find PipelineNode class and (try to) load new inspector page.
            pipeline_node_type_name = selected_node.__class__.__name__
            debug('\n'.join(str((k, v)) for k, v in INSPECTOR_PAGE_REGISTRY.items()))
            inspector_page_class = INSPECTOR_PAGE_REGISTRY.get(pipeline_node_type_name, None)
            if inspector_page_class is None:
                wx.MessageBox('Node type %s does not have inspector.' %(pipeline_node_type_name),
                              'Invalid operation.')
                return
            debug('inspector page class: %s' %(inspector_page_class))
            # else
            inspector_page_index, inspector_page_instance = self.inspector_notebook.create_page(
                inspector_page_class, selected_node.name, target=selected_node)
            # force update
            inspector_page_instance.update()
        self.inspector_notebook.SetSelection(inspector_page_index)

    def OnPipelineShowVisualizerMenu(self, event):
        """Called on 'Pipeline'->'Show visualizer...' menu.
        """
        # TBD: this is almost same with OnPipelineShowInspectorMenu.
        # If current pipeline node is set to None, do nothing and return.
        selected_tree_id, selected_node = self.check_pipeline_node_selected()
        if selected_node is None:
            return
        # else -- 
        debug('current_pipeline_node is %s' %selected_node)
        # If there are already corresponding visualizer, just focus it.
        visualizer_page_index, visualizer_page_instance = self.visualizer_notebook.find_page_for_target(selected_node)
        if visualizer_page_index is None:
            debug('No page exists, trying')
            # find PipelineNode class and (try to) load new visualizer page.
            pipeline_node_type_name = selected_node.__class__.__name__
            debug('\n'.join(str((k, v)) for k, v in VISUALIZER_PAGE_REGISTRY.items()))
            visualizer_page_class = VISUALIZER_PAGE_REGISTRY.get(pipeline_node_type_name, None)
            if visualizer_page_class is None:
                wx.MessageBox('Node type %s does not have inspector.' %(pipeline_node_type_name),
                              'Invalid operation.')
                return
            debug('inspector page class: %s' %(visualizer_page_class))
            # else
            visualizer_page_index, visualizer_page_instance = self.visualizer_notebook.create_page(
                visualizer_page_class, selected_node.name, target=selected_node)
            # force update
            visualizer_page_instance.update()
        self.visualizer_notebook.SetSelection(visualizer_page_index)

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

    def OnDatasourceChanged(self, event):
        """Hook on datasource change.
        """
        debug('datasource.uri=%s' %self.datasource.uri)
        pevent = UpdateEvent(None)
        self.pipeline.propagate(pevent)

    def OnPipelineTreeSelChanged(self, event):
        """Called on selection change on pipeline tree item.
        """
        # If current pipeline node is set to None, do nothing and return.
        selected_tree_item_id, selected_node = self.check_pipeline_node_selected()
        if selected_node is None:
            return
        node_type_name = selected_node.__class__.__name__
        self.pipeline_tree_ctrl.tree_menu.enable_show_inspector(
            node_type_name in INSPECTOR_PAGE_REGISTRY.keys())
        self.pipeline_tree_ctrl.tree_menu.enable_show_visualizer(
            node_type_name in VISUALIZER_PAGE_REGISTRY.keys())

    def OnPipelineTreeItemMenu(self, event):
        """Called on right-click on a pipeline tree item.
        """
        self.pipeline_tree_ctrl.popup_tree_menu()

    def OnPipelineShowObserversMenu(self, event):
        selected_tree_id, selected_node = self.check_pipeline_node_selected()
        if selected_node is None:
            return
        # If there are already corresponding inspector, just focus it.
        inspector_page_index, inspector_page_instance = self.inspector_notebook.find_page_for_target(selected_node)
        if inspector_page_index is None:
            pipeline_node_type_name = selected_node.__class__.__name__
            inspector_page_class = INSPECTOR_PAGE_REGISTRY.get(pipeline_node_type_name, None)
            if inspector_page_class is not None:
                self.OnPipelineShowInspectorMenu(event)
            visualizer_page_class = VISUALIZER_PAGE_REGISTRY.get(pipeline_node_type_name, None)
            if visualizer_page_class is not None:
                self.OnPipelineShowVisualizerMenu(event)


if __name__=='__main__':
    app = BrowserApp(0)
    debug('Running MainLoop()')
    app.MainLoop()
    debug('Exit.')
