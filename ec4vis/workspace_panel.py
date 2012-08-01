# coding: utf-8
"""workspace_panel.py --- Workspace panel in visualizer application.
"""
import wx


# WorkspaceTree uses WorkspaceModel instance as an internal data model.
# See workspace.py for details.


class WorkspaceTree(wx.TreeCtrl):
    """TreeCtrl for workspace.
    """
    
    def __init__(self, *args, **kwargs):
        wx.TreeCtrl.__init__(self, *args, **kwargs)
        root_node = self.AddRoot("WorkSpace")
        # root/toplevel nodes
        self.root_node = root_node
        self.file_node = self.AppendItem(root_node, 'Files')
        self.loader_node = self.AppendItem(root_node, 'Loaders')
        self.filter_node = self.AppendItem(root_node, 'Filters')
        self.visualizer_node = self.AppendItem(root_node, 'Vizualizers')
        self.visual_node = self.AppendItem(root_node, 'Visuals')
        self.parameter_node = self.AppendItem(root_node, 'Parameters')
        self.frame_node = self.AppendItem(root_node, 'Frames')
        self._model = None

    def set_model(self, model):
        """Bind model to the tree.
        """
        self._model = model
        self.refresh()

    def get_model(self):
        return self._model

    model = property(get_model, set_model)

    def refresh(self):
        """Refresh tree content to reflect given model.
        """
        for node_type in ['file', 'loader', 'filter', 'visualizer',
                          'visual', 'parameter', 'frame']:
            parent_node = getattr(self, node_type+'_node', None)
            node_add_handler = getattr(self, 'add_'+node_type+'_node')
            if parent_node and node_add_handler:
                self.DeleteChildren(parent_node)
                for subnode_info in getattr(self._model, node_type, []):
                    node_add_handler(subnode_info)

    def add_node(self, parent_node, node_info):
        """Common node_add handler.
        """
        node = self.AppendItem(parent_node, unicode(node_info))
        self.SetPyData(node, node_info)
        
        return node

    def add_file_node(self, node_info):
        """Adds file node to the tree.
        """
        node = self.add_node(self.file_node, node_info)
        
    def add_loader_node(self, node_info):
        """Adds loader node to the tree.
        """
        node = self.add_node(self.loader_node, node_info)
        
    def add_filter_node(self, node_info):
        """Adds filter node to the tree.
        """
        node = self.add_node(self.filter_node, node_info)
        
    def add_visualizer_node(self, node_info):
        """Adds visualizer node to the tree.
        """
        node = self.add_node(self.visualizer_node, node_info)

    def add_visual_node(self, node_info):
        """Adds visual node to the tree.
        """
        node = self.add_node(self.visual_node, node_info)
        
    def add_parameter_node(self, node_info):
        """Adds parameter node to the tree.
        """
        node = self.add_node(self.parameter_node, node_info)
    
    def add_frame_node(self, node_info):
        """Adds frame node to the tree.
        """
        node = self.add_node(self.frame_node, node_info)
        

class WorkspacePanel(wx.Panel):
    """Data panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        # workspace tree control
        tree_ctrl = WorkspaceTree(
            self, -1, style=wx.SUNKEN_BORDER|wx.TR_HAS_BUTTONS|wx.TR_HIDE_ROOT)
        # name bindings
        self.tree_ctrl = tree_ctrl
        # sizer
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(tree_ctrl, 1, wx.ALL|wx.EXPAND, 0)
        root_sizer.SetMinSize((200, -1))
        self.SetSize((200, 600))
        self.SetSizer(root_sizer)
        self.Layout()


if __name__=='__main__':
    
    class DummyNode(object):

        def __init__(self, label):
            self.label = label

        def __unicode__(self):
            return self.label

    class DummyModel(object):

        def __init__(self):
            self.file = [DummyNode('FooFile'), DummyNode('BarFile')]
            self.filter = [DummyNode('BazFilter'), DummyNode('QuxFilter')]
    
    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'Workspace Panel Demo')
            workspace_panel = WorkspacePanel(frame, -1)
            tree = workspace_panel.tree_ctrl
            tree.model = DummyModel()
            tree.refresh()
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(workspace_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

    app = App(0)
    app.MainLoop()
