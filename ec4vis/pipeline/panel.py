# coding: utf-8
"""ec4vis.pipeline.panel --- Workspace panel in visualizer application.
"""
import wx
from wx.lib.mixins import treemixin

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug
from ec4vis.utils.wx_ import TreeCtrlPlus
from ec4vis.pipeline import PipelineTree, PipelineNode


class PipelineTreeCtrl(TreeCtrlPlus):
    """TreeCtrl for workspace.
    """    
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        style = kwargs.pop('style', 0)|wx.TR_NO_BUTTONS
        kwargs['style'] = style
        wx.TreeCtrl.__init__(self, *args, **kwargs)
        # initial pipeline set to None
        self._pilepline = None
        # root/toplevel nodes
        self.root_item_id = None # will provided in rebuild_root()

    def set_pipeline(self, pipeline):
        """Bind model to the tree.
        """
        debug('PipelineTreeCtrl::set_pipeline() setting pilepline at %d' %(id(pipeline)))
        self._pipeline = pipeline
        self.rebuild_root()

    def get_pipeline(self):
        return self._pipeline

    pipeline = property(get_pipeline, set_pipeline)

    def rebuild_root(self):
        """Rebuild tree from the toplevel.
        """
        debug('PipelineTreeCtrl::rebuild_root()')
        self.DeleteAllItems()
        root_item_id = self.AddRoot("<<DataSource>>")
        root_object = None
        if self.pipeline:
            root_object = self.pipeline.root
        self.root_item_id = root_item_id
        self.SetPyData(root_item_id, root_object)
        self.rebuild_tree(root_item_id)
        debug('rebuild_root() succellfully.')

    def rebuild_tree(self, item_id):
        """Rebuild subtree beneath the given item_id.
        """
        debug('PipelineTreeCtrl::rebuild_tree() building under item #%s' %item_id)
        node_data = self.GetPyData(item_id)
        if node_data is None:
            return
        for child in node_data.children:
            child_id = self.AppendItem(item_id, '%s::%s' %(child.class_name, child.name))
            self.SetPyData(child_id, child)
            self.rebuild_tree(child_id)


class PipelinePanel(wx.Panel):
    """Data panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        # workspace tree control
        tree_ctrl = PipelineTreeCtrl(self, -1, style=wx.SUNKEN_BORDER)
        # buttons
        add_button = wx.Button(self, -1, '+')
        del_button = wx.Button(self, -1, '-')
        # name bindings
        self.tree_ctrl = tree_ctrl
        # sizer
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        button_sizer.Add(add_button, 0, wx.ALL, 0)
        button_sizer.Add(del_button, 0, wx.ALL, 0)
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(tree_ctrl, 1, wx.ALL|wx.EXPAND, 0)
        root_sizer.Add(button_sizer, 0, wx.ALL, 5)
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
