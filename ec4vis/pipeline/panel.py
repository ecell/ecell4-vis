# coding: utf-8
"""ec4vis.pipeline.panel --- Workspace panel in visualizer application.
"""
import wx
from wx.lib.mixins import treemixin

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call
from ec4vis.utils.wx_ import TreeCtrlPlus
from ec4vis.pipeline import PipelineTree, PipelineNode


class PipelineTreeItemMenu(wx.Menu):
    """Context menu shown on pipeline tree item.
    """
    def __init__(self):
        wx.Menu.__init__(self)
        # populate menu items
        add_node_menu_id = self.Append(-1, "Add...")
        delete_node_menu_id = self.Append(-1, "Delete")
        show_inspector_menu_id = self.Append(-1, "Show Inspector")
        show_visualizer_menu_id = self.Append(-1, "Show Visualizer")
        self.add_node_menu_id = add_node_menu_id
        self.delete_node_menu_id = delete_node_menu_id
        self.show_inspector_menu_id = show_inspector_menu_id
        self.show_visualizer_menu_id = show_visualizer_menu_id

    def enable_show_inspector(self, enabled):
        """Enable/disables 'Show Inspector' menu.
        """
        self.Enable(self.show_inspector_menu_id.GetId(), enabled)
                
    def enable_show_visualizer(self, enabled):
        """Enable/disables 'Show Visualizer' menu.
        """
        self.Enable(self.show_visualizer_menu_id.GetId(), enabled)
        

class PipelineTreeCtrl(TreeCtrlPlus):
    """TreeCtrl for workspace.
    """    
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        style = kwargs.pop('style', 0)|wx.TR_NO_BUTTONS
        kwargs['style'] = style
        wx.TreeCtrl.__init__(self, *args, **kwargs)
        # tree item menu
        self.tree_menu = PipelineTreeItemMenu()
        # initial pipeline set to None
        self._pilepline = None

    @log_call
    def get_subtree_data(self, tree_item_id):
        """Recursively collects target data from subtree of given tree_item_id.
        """
        current_node = self.GetPyData(tree_item_id)
        return current_node.descendants

    def set_pipeline(self, pipeline):
        """Bind model to the tree.
        """
        debug('PipelineTreeCtrl::set_pipeline() setting pilepline at %d' %(id(pipeline)))
        self._pipeline = pipeline
        self.rebuild_root()

    def get_pipeline(self):
        return self._pipeline

    pipeline = property(get_pipeline, set_pipeline)

    @property
    def selected_tree_item_id(self):
        """Returns tree item currently selected.
        """
        selected_item_id = self.GetSelection()
        if selected_item_id and selected_item_id.IsOk():
            return selected_item_id
        # else
        return None

    @property
    def selected_pipeline_node(self):
        """Returns PipelineNode for currently selected tree item.
        """
        data = None
        if self.selected_tree_item_id:
            data = self.GetPyData(self.selected_tree_item_id)
        return data

    def rebuild_root(self):
        """Rebuild tree from the toplevel.
        """
        debug('PipelineTreeCtrl::rebuild_root()')
        self.DeleteAllItems()
        root_item_id = self.AddRoot("<<DataSource>>")
        root_object = None
        if self.pipeline:
            root_object = self.pipeline.root
        self.SetPyData(root_item_id, root_object)
        self.rebuild_tree(root_item_id)
        debug('rebuild_root() succellfully.')

    def rebuild_tree(self, item_id):
        """Rebuild subtree beneath the given item_id.
        """
        # delete children beneath.
        self.DeleteChildren(item_id)
        debug('PipelineTreeCtrl::rebuild_tree() building under item #%s' %item_id)
        node_data = self.GetPyData(item_id)
        if node_data is None:
            return
        for child in node_data.children:
            child_id = self.AppendItem(item_id, '%s::%s' %(child.class_name, child.name))
            self.SetPyData(child_id, child)
            self.rebuild_tree(child_id)

    def rebuild_parent(self, item_id):
        """Rebuild parent tree of given item_id.
        """
        self.rebuild_tree(self.GetItemParent(item_id))

    def popup_tree_menu(self):
        self.PopupMenu(self.tree_menu)



class PipelinePanel(wx.Panel):
    """Data panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        # workspace tree control
        tree_ctrl = PipelineTreeCtrl(self, -1, style=wx.SUNKEN_BORDER)
        # name bindings
        self.tree_ctrl = tree_ctrl
        # sizer
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(tree_ctrl, 1, wx.ALL|wx.EXPAND, 0)
        root_sizer.SetMinSize((200, -1))
        self.SetSize((200, 600))
        self.SetSizer(root_sizer)
        self.Layout()

    def finalize(self):
        """Finalizer.
        """
        # placeholder atm


if __name__=='__main__':

    pipeline = PipelineTree()
    filter1 = PipelineNode('Filter 1')
    filter2 = PipelineNode('Filter 2')
    filter3 = PipelineNode('Filter 3')
    renderer1 = PipelineNode('Renderer 1')
    renderer2 = PipelineNode('Renderer 2')
    renderer3 = PipelineNode('Renderer 3')
    filter1.connect(pipeline.root)
    filter2.connect(filter1)
    filter3.connect(filter2)
    renderer1.connect(filter1)
    renderer2.connect(filter2)
    renderer3.connect(filter3)
    
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Pipeline Panel Demo')
            pipeline_panel = PipelinePanel(frame, -1)
            tree = pipeline_panel.tree_ctrl
            tree.pipeline = pipeline
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(pipeline_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

    app = App(0)
    app.MainLoop()
