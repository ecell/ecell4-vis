# coding: utf-8
"""pipeline_panel.py --- Workspace panel in visualizer application.
"""
import wx
from wx.lib.mixins import treemixin

from utils_wx import TreeCtrlPlus
from pipeline import Pipeline, PipelineItem


class PipelineTree(TreeCtrlPlus):
    """TreeCtrl for workspace.
    """    
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        style = kwargs.pop('style', 0)|wx.TR_NO_BUTTONS
        pipeline = kwargs.pop('pipeline', None)
        kwargs['style'] = style
        wx.TreeCtrl.__init__(self, *args, **kwargs)
        # root/toplevel nodes
        self.root_item_id = None # will provided in rebuild_root()
        self.pipeline = pipeline # will invoke rebuild_root()

    def set_pipeline(self, pipeline):
        """Bind model to the tree.
        """
        self._pipeline = pipeline
        self.rebuild_root()

    def get_pipeline(self):
        return self._pipeline

    pipeline = property(get_pipeline, set_pipeline)

    def rebuild_root(self):
        """Rebuild tree from the toplevel.
        """
        self.DeleteAllItems()
        root_item_id = self.AddRoot("<<Data>>")
        root_object = None
        if self.pipeline:
            root_object = self.pipeline.root
        self.root_item_id = root_item_id
        self.SetPyData(root_item_id, root_object)
        self.rebuild_tree(root_item_id)

    def rebuild_tree(self, item_id):
        """Rebuild subtree beneath the given item_id.
        """
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
        tree_ctrl = PipelineTree(self, -1, style=wx.SUNKEN_BORDER)
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


if __name__=='__main__':

    pipeline = Pipeline()
    filter1 = PipelineItem('Filter 1')
    filter2 = PipelineItem('Filter 2')
    filter3 = PipelineItem('Filter 3')
    renderer1 = PipelineItem('Renderer 1')
    renderer2 = PipelineItem('Renderer 2')
    renderer3 = PipelineItem('Renderer 3')
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
