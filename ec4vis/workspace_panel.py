# coding: utf-8
"""workspace_panel.py --- Workspace panel in visualizer application.
"""
import glob, os, os.path
import wx
from wx.lib import filebrowsebutton

icons_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'resources', 'icons')



class Ec4DirectoryScanner(object):

    def is_directory(self, path):
        """Determines if path 'should be treated as' directory.
        """
        if self.is_data_bundle(path):
            return False
        if os.path.isdir(path):
            return True

    def is_data_bundle(self, path):
        """Determines if path is a data (or data bundle)
        """
        # actual algorithm is TBD
        pass


class WorkspaceTree(wx.TreeCtrl):
        
    BINDINGS = (
        ('BEGIN_DRAG', 'OnBeginDrag'),
        ('BEGIN_RDRAG', 'OnBeginRDrag'),
        ('END_DRAG', 'OnEndDrag'),
        ('BEGIN_LABEL_EDIT', 'OnBeginLabelEdit'),
        ('END_LABEL_EDIT', 'OnEndLabelEdit'),
        ('DELETE_ITEM', 'OnDeleteItem'),
        ('GET_INFO', 'OnGetInfo'),
        ('SET_INFO', 'OnSetInfo'),
        ('ITEM_ACTIVATED', 'OnItemActivated'),
        ('ITEM_COLLAPSED', 'OnItemCollapsed'),
        ('ITEM_COLLAPSING', 'OnItemCollapsing'),
        ('ITEM_EXPANDED', 'OnItemExpanded'),
        ('ITEM_EXPANDING', 'OnItemExpanding'),
        ('ITEM_RIGHT_CLICK', 'OnItemRightClick'),
        ('ITEM_MIDDLE_CLICK', 'OnItemMiddleClick'),
        ('SEL_CHANGED', 'OnSelChanged'),
        ('SEL_CHANGING', 'OnSelChanging'),
        ('KEY_DOWN', 'OnKeyDown'),
        ('ITEM_GETTOOLTIP', 'OnItemGetToolTip'),
        ('ITEM_MENU', 'OnItemMenu'),
        ('STATE_IMAGE_CLICK', 'OnStateImageClick'),
        )    


    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.TreeCtrl.__init__(self, *args, **kwargs)
        image_size = (16, 16)
        self.image_list = wx.ImageList(*image_size)
        """
        self.folder_image_id = self.image_list.Add(
            wx.ArtProvider_GetBitmap(wx.ART_FOLDER, wx.ART_OTHER, image_size))
        self.file_image_id = self.image_list.Add(
            wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, image_size))
            """
        self.folder_image_id = self.image_list.Add(
            wx.Image(os.path.join(icons_path, 'folder_open.png'),
                     wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.file_image_id = self.image_list.Add(
            wx.Image(os.path.join(icons_path, 'document_default.png'),
                     wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.bundle_image_id = self.image_list.Add(
            wx.Image(os.path.join(icons_path, 'draw_layer.png'),
                     wx.BITMAP_TYPE_PNG).ConvertToBitmap())
        self.SetImageList(self.image_list)
        self._root_path = os.getcwd()

        for evt_name, handler_name in self.BINDINGS:
            macro = getattr(wx, 'EVT_TREE_'+evt_name)
            handler = getattr(self, handler_name)
            self.Bind(macro, handler, self)
        self.rebuild_root()

    def get_root_path(self):
        """Getter for root_path
        """
        return self._root_path

    def set_root_path(self, root_path):
        """Setter for root_path
        """
        self._root_path = root_path
        self.rebuild_root()

    root_path = property(get_root_path, set_root_path)

    def rebuild_root(self):
        """Rebuild tree from root.
        """
        root_item_id = self.GetRootItem()
        if root_item_id and root_item_id.IsOk():
            if self.GetItemText(root_item_id)!=self._root_path:
                self.DeleteAllItems()
                self.AddRoot(self._root_path)
        else:
            self.AddRoot(self._root_path)
        root_item_id = self.GetRootItem()
        self.SetItemHasChildren(root_item_id, os.path.isdir(self._root_path))
        self.SetItemImage(root_item_id, self.folder_image_id, wx.TreeItemIcon_Normal)
        self.SetItemImage(root_item_id, self.folder_image_id, wx.TreeItemIcon_Expanded)
        if self.ItemHasChildren(root_item_id) and self.IsExpanded(root_item_id):
            self.rebuild_tree(root_item_id)

    def get_node_path(self, item_id):
        """Resolve path of the node (with recursion).
        """
        parent_id = self.GetItemParent(item_id)
        if parent_id:
            parent_node_path = self.get_node_path(parent_id)
            return os.path.join(parent_node_path, self.GetItemText(item_id))
        else:
            return self.GetItemText(item_id)

    def rebuild_tree(self, item_id):
        """Rebuilds a subtree.
        """
        node_path = self.get_node_path(item_id)
        node_names = os.listdir(node_path)
        child_id, cookie = self.GetFirstChild(item_id)
        id_to_delete = []
        # phase 1: update children, marking candidates for deletion
        while child_id:
            child_text = self.GetItemText(child_id)
            if child_text not in node_names:
                # mark nonexistent children to delete
                id_to_delete.append(child_id)
            else:
                node_names.remove(child_text)
                child_path = os.path.join(node_path, child_text)
                if os.path.isdir(child_path):
                    image_id = self.folder_image_id
                    if glob.glob(os.path.join(node_path, '*.h5')):
                        image_id = self.bundle_image_id
                    self.SetItemImage(
                        child_id, self.image_id, wx.TreeItemIcon_Normal)
                    self.SetItemHasChildren(child_id, True)
                    if self.IsExpanded(child_id):
                        self.rebuild_tree(child_id)
                else:
                    self.SetItemImage(child_id, self.file_image_id, wx.TreeItemIcon_Normal)
                    self.SetItemHasChildren(child_id, False)
            child_id, cookie = self.GetNextChild(child_id, cookie)
        # phase 2: delete nonexistent nodes
        for del_id in id_to_delete:
            self.Delete(del_id)
        # phase 3: populate newly introduced nodes
        for node_name in node_names:
            child_path = os.path.join(node_path, node_name)
            child_id = self.AppendItem(item_id, node_name)
            is_dir = os.path.isdir(child_path)
            self.SetItemHasChildren(child_id, is_dir)
            if is_dir:
                image_id = self.folder_image_id
                if glob.glob(os.path.join(node_path, '*.h5')):
                    image_id = self.bundle_image_id
                self.SetItemImage(child_id, image_id, wx.TreeItemIcon_Normal)
                self.SetItemImage(child_id, image_id, wx.TreeItemIcon_Expanded)
            else:
                image_id = self.file_image_id
                self.SetItemImage(child_id, image_id, wx.TreeItemIcon_Normal)
        return

    def OnBeginDrag(self, evt):
        """Handler called on begin item dragging.
        """
        pass # do nothing atm

    def OnBeginRDrag(self, evt):
        """Handler called on begin item dragging with right button.
        """
        pass # do nothing atm

    def OnEndDrag(self, evt):
        """Handler called on end item dragging.
        """
        pass # do nothing atm

    def OnBeginLabelEdit(self, evt):
        """Handler called on begin editing label on an item.
        """
        pass # do nothing atm

    def OnEndLabelEdit(self, evt):
        """Handler called on end editing label on an item.
        """
        pass # do nothing atm

    def OnDeleteItem(self, evt):
        """Handler called on deleting item.
        """
        pass # do nothing atm

    def OnGetInfo(self, evt):
        """Handler called on getting node info.
        """
        pass # do nothing atm

    def OnSetInfo(self, evt):
        """Handler called on getting node info.
        """
        pass # do nothing atm

    def OnItemActivated(self, evt):
        """Handler called on activating item.
        """
        pass # do nothing atm

    def OnItemCollapsed(self, evt):
        """Handler called on an item has collapsed.
        """
        item_id = evt.GetItem()
        self.DeleteChildren(item_id)

    def OnItemCollapsing(self, evt):
        """Handler called on collapsing an item.
        """
        pass # do nothing atm

    def OnItemExpanded(self, evt):
        """Handler called on an item has expanded.
        """
        pass # do nothing atm
        
    def OnItemExpanding(self, evt):
        """Handler called on expanding item.
        """
        item_id = evt.GetItem()
        self.rebuild_tree(item_id)

    def OnItemRightClick(self, evt):
        """Handler called on right-clicking item.
        """
        pass # do nothing atm

    def OnItemMiddleClick(self, evt):
        """Handler called on middle-clicking item.
        """
        pass # do nothing atm

    def OnSelChanged(self, evt):
        """Handler called on user has changed item selection.
        """
        pass # do nothing atm

    def OnSelChanging(self, evt):
        """Handler called on changing selection.
        """
        pass # do nothing atm

    def OnKeyDown(self, evt):
        """Handler called on key down.
        """
        pass # do nothing atm

    def OnItemGetToolTip(self, evt):
        """Handler called on getting tooltip
        """
        pass # do nothing atm

    def OnItemMenu(self, evt):
        """Handler called on requiring context menu.
        """
        pass # do nothing atm

    def OnStateImageClick(self, evt):
        """Handler called on clicing state image.
        """
        pass # do nothing atm

        

class WorkspacePanel(wx.Panel):
    """Data panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        # workspace tree control
        tree_ctrl = WorkspaceTree(
            self, -1, style=wx.SUNKEN_BORDER|wx.TR_HAS_BUTTONS)
        self.tree_ctrl = tree_ctrl
        # root_directory browse button
        directory_browse_button = filebrowsebutton.DirBrowseButton(
            self, -1, changeCallback=self.directory_browse_callback,
            labelText='Data Root:', 
            )
        directory_browse_button.SetValue(tree_ctrl.root_path)
        # name bindings
        self.directory_browse_button = directory_browse_button
        # sizer
        root_sizer = wx.BoxSizer(wx.VERTICAL)
        root_sizer.Add(directory_browse_button, 0, wx.ALL|wx.EXPAND, 0)
        root_sizer.Add(tree_ctrl, 1, wx.ALL|wx.EXPAND, 0)
        root_sizer.SetMinSize((200, -1))
        self.SetSize((200, 600))
        self.SetSizer(root_sizer)
        self.Layout()

    def directory_browse_callback(self, evt):
        self.tree_ctrl.root_path = evt.GetString()
        


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
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(workspace_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True

    app = App(0)
    app.MainLoop()
