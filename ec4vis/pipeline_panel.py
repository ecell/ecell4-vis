# coding: utf-8
"""pipeline_panel.py --- Workspace panel in visualizer application.
"""
import wx
from wx.lib.mixins import treemixin


class PipelineTreeModel(object):
    """Pipeline tree model.
    """
    def __init__(self, *args, **kwargs):
        self.items = []
        self.itemCounter = 0
        super(PipelineTreeModel, self).__init__(*args, **kwargs)

    def GetItem(self, indices):
        text, children = 'Hidden root', self.items
        for index in indices:
            text, children = children[index]
        return text, children

    def GetText(self, indices):
        return self.GetItem(indices)[0]

    def GetChildren(self, indices):
        return self.GetItem(indices)[1]

    def GetChildrenCount(self, indices):
        return len(self.GetChildren(indices))

    def SetChildrenCount(self, indices, count):
        children = self.GetChildren(indices)
        while len(children) > count:
            children.pop()
        while len(children) < count:
            children.append(('item %d'%self.itemCounter, []))
            self.itemCounter += 1

    def MoveItem(self, itemToMoveIndex, newParentIndex):
        itemToMove = self.GetItem(itemToMoveIndex)
        newParentChildren = self.GetChildren(newParentIndex)
        newParentChildren.append(itemToMove)
        oldParentChildren = self.GetChildren(itemToMoveIndex[:-1])
        oldParentChildren.remove(itemToMove)


class PipelineTreeMixin(treemixin.VirtualTree, treemixin.DragAndDrop, 
                    treemixin.ExpansionState):
    """Tree Mixin.
    """
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('treemodel')
        self.log = kwargs.pop('log')
        super(PipelineTreeMixin, self).__init__(*args, **kwargs)
        self.CreateImageList()

    def CreateImageList(self):
        size = (16, 16)
        self.imageList = wx.ImageList(*size)
        for art in wx.ART_FOLDER, wx.ART_FILE_OPEN, wx.ART_NORMAL_FILE:
            self.imageList.Add(wx.ArtProvider.GetBitmap(art, wx.ART_OTHER, 
                                                        size))
        self.AssignImageList(self.imageList)

    def OnGetItemText(self, indices):
        return self.model.GetText(indices)

    def OnGetChildrenCount(self, indices):
        return self.model.GetChildrenCount(indices)

    def OnGetItemFont(self, indices):
        # Show how to change the item font. Here we use a small font for
        # items that have children and the default font otherwise.
        if self.model.GetChildrenCount(indices) > 0:
            return wx.SMALL_FONT
        else:
            return super(DemoTreeMixin, self).OnGetItemFont(indices)

    def OnGetItemTextColour(self, indices):
        # Show how to change the item text colour. In this case second level
        # items are coloured red and third level items are blue. All other
        # items have the default text colour.
        if len(indices) % 2 == 0:
            return wx.RED
        elif len(indices) % 3 == 0:
            return wx.BLUE
        else:
            return super(DemoTreeMixin, self).OnGetItemTextColour(indices)

    def OnGetItemBackgroundColour(self, indices):
        # Show how to change the item background colour. In this case the
        # background colour of each third item is green.
        if indices[-1] == 2:
            return wx.GREEN
        else: 
            return super(DemoTreeMixin, 
                         self).OnGetItemBackgroundColour(indices)

    def OnGetItemImage(self, indices, which):
        # Return the right icon depending on whether the item has children.
        if which in [wx.TreeItemIcon_Normal, wx.TreeItemIcon_Selected]:
            if self.model.GetChildrenCount(indices):
                return 0
            else:
                return 2
        else:
            return 1

    def OnDrop(self, dropTarget, dragItem):
        dropIndex = self.GetIndexOfItem(dropTarget)
        dropText = self.model.GetText(dropIndex)
        dragIndex = self.GetIndexOfItem(dragItem)
        dragText = self.model.GetText(dragIndex)
        """self.log.write('drop %s %s on %s %s'%(dragText, dragIndex,
            dropText, dropIndex))"""
        self.model.MoveItem(dragIndex, dropIndex)
        self.GetParent().RefreshItems()


class PipelineTree(PipelineTreeMixin, wx.TreeCtrl):
    """TreeCtrl for workspace.
    """
    
    def __init__(self, *args, **kwargs):
        wx.TreeCtrl.__init__(self, *args, **kwargs)
        root_node = self.AddRoot("WorkSpace")
        # root/toplevel nodes
        self.root_node = root_node
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
        

class PipelinePanel(wx.Panel):
    """Data panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        # workspace tree control
        tree_ctrl = PipelineTree(
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
            frame = wx.Frame(None, -1, u'Pipeline Panel Demo')
            pipeline_panel = PipelinePanel(frame, -1)
            tree = pipeline_panel.tree_ctrl
            tree.model = DummyModel()
            tree.refresh()
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(pipeline_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

    app = App(0)
    app.MainLoop()
