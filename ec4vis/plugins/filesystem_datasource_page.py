# coding: utf-8
"""ec4vis.datasource.filesystem.tree --- Tree for filesyste-based datasource.
"""
import re
import os # required for os.getcwd in FilesystemTree
import glob
import wx, wx.aui
from wx.lib.filebrowsebutton import DirBrowseButton

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.utils.wx_ import ImageListWrapper, TreeCtrlPlus
from ec4vis.logger import debug, log_call
from ec4vis.datasource.page import DatasourcePage, register_datasource_page


class FileNodeProfilerAbstract(object):
    """
    Abstract class for file node profiler.

    The file node profiler accepts file path and examines if given
    path points valid data file, data bundle, directory or otherwise.
    
    """
    def __init__(self, path):
        """Initializer.
        """
        self.path = path

    def is_data_file(self):
        """Returns if the path points to a valid data file.

        Subclass should override this, must return boolean.
        """
        return NotImplemented

    def is_data_bundle(self):
        """Returns if the path points to a valid data bundle.

        Subclass should override this, must return boolean.
        """
        return NotImplemented

    def is_directory(self):
        """Returns if the path points to a (non-bundle) directory.

        Subclass should override this, must return boolean.
        """
        return NotImplemented


class DefaultFileNodeProfiler(FileNodeProfilerAbstract):
    """Default profiler implementation.

    This profiler recognizes *.h5, *.hdf5 files as data files,
    directories containing *.h5 and *.hdf5 files as data bundles.
    """
    ext_names = ['.h5', '.hdf5', '.csv']

    DIRECTORY_ITEM = 0
    DATA_BUNDLE_ITEM = 1
    DATA_FILE_ITEM = 2
    DATA_SET_ITEM = 3

    def is_data_file(self):
        if os.path.exists(self.path) and (not os.path.isdir(self.path)):
            body, ext = os.path.splitext(self.path)
            if ext.lower() in DefaultFileNodeProfiler.ext_names:
                return True
        # else
        return False

    def is_data_bundle(self):
        """Returns if the path points to a valid data bundle.

        Subclass should override this.
        """
        if os.path.exists(self.path) and os.path.isdir(self.path):
            for name in os.listdir(self.path):
                body, ext = os.path.splitext(name)
                if ext.lower() in DefaultFileNodeProfiler.ext_names:
                    return True
        # else
        return False

    def is_directory(self):
        """Returns if the path points to a (non-bundle) directory.

        Subclass should override this.
        """
        if os.path.exists(self.path) and os.path.isdir(self.path):
            if not self.is_data_bundle():
                return True
        # else
        return False
    

class FilesystemTree(TreeCtrlPlus):

    def __init__(self, *args, **kwargs):
        kwargs['style'] = wx.SUNKEN_BORDER|wx.TR_HAS_BUTTONS|kwargs.get('style', 0)
        root_path = kwargs.pop('root_path', os.getcwd())
        file_node_profiler = kwargs.pop('file_node_profiler', DefaultFileNodeProfiler)
        TreeCtrlPlus.__init__(self, *args, **kwargs)
        image_list_wrapper = ImageListWrapper('icons/mono16/data')
        # bindings
        self._root_path = root_path
        self.file_node_profiler = file_node_profiler
        self.image_list_wrapper = image_list_wrapper
        self.SetImageList(self.image_list_wrapper.image_list)
        self.build_root()

    def get_root_path(self):
        """Property getter for root path.
        """
        return self._root_path

    def set_root_path(self, path):
        """Property setter for root path.
        
        It rebuilds tree's root immediately.
        It is developer's responsibility to specify valid directory path.
        """
        self._root_path = path
        self.build_root()

    root_path = property(get_root_path, set_root_path)

    def get_parent_node_path(self, item_id):
        parent_id = self.GetItemParent(item_id)
        # node_name = self.GetItemText(item_id)
        item_data = self.GetItemData(item_id).GetData()
        node_name = item_data['text']
        if parent_id:
            parent_node_path = self.get_node_path(parent_id)
            if item_data['type'] == self.file_node_profiler.DATA_SET_ITEM:
                return parent_node_path
            else:
                return os.path.join(parent_node_path, node_name)
        return node_name

    def get_node_path(self, item_id):
        """Resolve path of the node.
        """
        parent_id = self.GetItemParent(item_id)
        node_name = self.GetItemText(item_id)
        # node_name = self.GetItemData(item_id).GetData()['text']
        if parent_id:
            parent_node_path = self.get_parent_node_path(parent_id)
            return os.path.join(parent_node_path, node_name)
        return node_name

    def setup_folder_item(self, item_id, item_text):
        """Setup given tree item as a folder.
        """
        close_image_id = self.image_list_wrapper['folder_close']
        open_image_id = self.image_list_wrapper['folder_open']
        self.SetItemHasChildren(item_id, True)
        self.SetItemImage(item_id, close_image_id, wx.TreeItemIcon_Normal)
        self.SetItemImage(item_id, open_image_id, wx.TreeItemIcon_Expanded)
        item_data = wx.TreeItemData()
        item_data.SetData(
            {'text': item_text, 'type': self.file_node_profiler.DIRECTORY_ITEM})
        self.SetItemData(item_id, item_data)

    def setup_data_file_item(self, item_id, item_text):
        """Setup given tree item as a data file.
        """
        data_image_id = self.image_list_wrapper['document_default']
        self.SetItemHasChildren(item_id, False)
        self.SetItemImage(item_id, data_image_id, wx.TreeItemIcon_Normal)
        item_data = wx.TreeItemData()
        item_data.SetData(
            {'text': item_text, 'type': self.file_node_profiler.DATA_FILE_ITEM})
        self.SetItemData(item_id, item_data)

    def setup_data_set_item(self, item_id, item_text):
        """Setup given tree item as a data set.
        """
        data_image_id = self.image_list_wrapper['document_create']
        # self.SetItemHasChildren(item_id, False)
        # self.SetItemImage(item_id, data_image_id, wx.TreeItemIcon_Normal)
        self.SetItemHasChildren(item_id, True)
        self.SetItemImage(item_id, data_image_id, wx.TreeItemIcon_Normal)
        self.SetItemImage(item_id, data_image_id, wx.TreeItemIcon_Expanded)
        item_data = wx.TreeItemData()
        item_data.SetData(
            {'text': item_text, 'type': self.file_node_profiler.DATA_SET_ITEM})
        self.SetItemData(item_id, item_data)

    def setup_data_bundle_item(self, item_id, item_text):
        """Setup given tree item as a data bundle.
        """
        bundle_image_id = self.image_list_wrapper['draw_layer']
        self.SetItemHasChildren(item_id, True)
        self.SetItemImage(item_id, bundle_image_id, wx.TreeItemIcon_Normal)
        self.SetItemImage(item_id, bundle_image_id, wx.TreeItemIcon_Expanded)
        item_data = wx.TreeItemData()
        item_data.SetData(
            {'text': item_text, 'type': self.file_node_profiler.DATA_BUNDLE_ITEM})
        self.SetItemData(item_id, item_data)

    def build_root(self):
        """Build root directory.
        """
        self.DeleteAllItems()
        root_item_id = self.AddRoot(self.root_path)
        self.setup_folder_item(root_item_id, self.root_path)
        self.SetItemHasChildren(root_item_id, os.path.isdir(self.root_path))
        # Root node should always expand initially.
        self.Expand(root_item_id)
            
    def build_tree(self, item_id):
        """Build a subtree for given item.
        """
        # If node has already some children, delete it first.
        if self.GetChildrenCount(item_id):
            self.DeleteChildren(item_id)

        node_path = self.get_node_path(item_id)
        node_dir_path = self.get_parent_node_path(item_id)
        node_type = self.GetItemData(item_id).GetData()['type']

        if os.path.isdir(node_path):
            if os.path.exists(node_path) == False:
                raise ValueError('node_path %s does not exist.' % node_path)
            subnode_names = os.listdir(node_path)
        else:
            tmp = glob.glob(node_path)
            if len(tmp) == 0:
                return # discard silently
            else:
                subnode_names = [os.path.basename(fname) for fname in tmp]
        # if os.path.exists(node_path)==False:
        #     raise ValueError('node_path %s does not exist.' %node_path)
        # if os.path.isdir(node_path)==False:
        #     return # discard silently
        # subnode_names = os.listdir(node_path)
        subnode_names.sort()

        data_sets = {}
        for subnode_name in subnode_names:
            # child_path = os.path.join(node_path, subnode_name)
            child_path = os.path.join(node_dir_path, subnode_name)
            node_profiler = self.file_node_profiler(child_path)
            item_data = wx.TreeItemData()
            if node_profiler.is_directory():
                child_id = self.AppendItem(item_id, subnode_name)
                self.setup_folder_item(child_id, subnode_name)
            elif node_profiler.is_data_bundle():
                child_id = self.AppendItem(item_id, subnode_name)
                self.setup_data_bundle_item(child_id, subnode_name)
            elif node_profiler.is_data_file():
                # child_id = self.AppendItem(item_id, subnode_name)
                # self.setup_data_file_item(child_id)

                rexp = re.compile('(.+)\.\d+(\.csv)$')
                mobj = rexp.match(subnode_name)
                if (node_type != self.file_node_profiler.DATA_SET_ITEM
                    and mobj is not None):
                    set_name = mobj.group(1)
                    if set_name in data_sets.keys():
                        data_sets[set_name].append(subnode_name)
                    else:
                        data_sets[set_name] = [subnode_name]
                        item_text = '%s.*.csv' % set_name
                        child_id = self.AppendItem(item_id, item_text)
                        self.setup_data_set_item(child_id, item_text)
                else:
                    child_id = self.AppendItem(item_id, subnode_name)
                    self.setup_data_file_item(child_id, subnode_name)
            else:
                pass # ignores unmatched items.

    def OnItemCollapsed(self, evt):
        """Collapsing directory will remove all children from the tree.
        """
        item_id = evt.GetItem()
        self.DeleteChildren(item_id)
        # TBD: If the selected item is of any deleting children...?

    def OnItemExpanding(self, evt):
        """Expanding tree will insert children to the tree.
        """
        item_id = evt.GetItem()
        self.build_tree(item_id)


class FilesystemDatasourcePage(DatasourcePage):
    """Notebook page for filesystem based datasource.
    """
    @log_call
    def __init__(self, *args, **kwargs):
        # this will populate self.datasource
        DatasourcePage.__init__(self, *args, **kwargs)
        tree_ctrl = FilesystemTree(self, -1)
        dir_browse_button = DirBrowseButton(
            self, -1, changeCallback=self.dir_browse_callback,
            labelText='Data Root:')
        dir_browse_button.SetValue(tree_ctrl.root_path)
        # bindings
        self.tree_ctrl = tree_ctrl
        self.dir_browse_button = dir_browse_button
        # event bindings
        self.Bind(
            wx.EVT_TREE_SEL_CHANGED, self.OnTreeSelectionChanged)
        # layout stuff
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(dir_browse_button, 0, wx.ALL|wx.EXPAND, 0)
        sizer.Add(tree_ctrl, 1, wx.ALL|wx.EXPAND, 0)
        self.SetSizer(sizer)
        self.Layout()

    def get_root_path(self):
        """Returns root path of the tree.
        """
        return self.tree_ctrl.root_path

    def set_root_path(self, root_path):
        """Set root path of the tree.
        """
        self.tree_ctrl.root_path = root_path
        self.dir_browse_button.SetValue(root_path)

    root_path = property(get_root_path, set_root_path)

    @log_call
    def dir_browse_callback(self, evt):
        """Handler for dir_browse_button's changeCallback.
        """
        tree_ctrl = getattr(self, 'tree_ctrl', None)
        if tree_ctrl:
            self.tree_ctrl.root_path = evt.GetString()
        # self.update_datasource()

    @log_call
    def OnTreeSelectionChanged(self, evt):
        """Handler called on selection changed in tree ctrl.
        """
        self.update_datasource()
    
    @log_call
    def update_datasource(self):
        """Updates datasource.
        """
        old_uri = self.datasource.uri
        prefix = 'file://'
        selected_id = self.tree_ctrl.GetSelection()
        if isinstance(selected_id, wx.TreeItemId) and selected_id.IsOk():
            file_path = self.tree_ctrl.get_node_path(selected_id)
            self.datasource.uri = prefix+file_path
        else:
            self.datasource.uri = prefix
        if not (old_uri==self.datasource.uri):
            # trigger DatasourceChangeEvent
            self.datasource_changed()

    def save(self):
        """Saves state.
        """
        return dict(root_path=self.root_path)

    def restore(self, info):
        """Restores state.
        """
        if isinstance(info, dict):
            root_path = info.get('root_path', None)
            if bool(root_path) and os.path.exists(root_path):
                self.root_path = root_path

    
# register FilesystemDatasourcePage to datasource page registry
register_datasource_page(FilesystemDatasourcePage)


if __name__=='__main__':

    this_filepath = os.path.abspath(__file__)
    ec4vis_parent = this_filepath[:this_filepath.rindex(os.sep+'ec4vis')]
    ec4vis_test_root = os.path.join(ec4vis_parent, 'tests', 'data', 'fs', 'root')
    
    from ec4vis.datasource import Datasource
    from ec4vis.datasource.panel import DatasourcePanel
    from ec4vis.datasource.page import EVT_DATASOURCE_CHANGED

    class App1(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'DatasourcePanel Demo')
            tree = FilesystemTree(frame, -1)
            tree.root_path = ec4vis_test_root
            self.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_sel_changed)
            sizer = wx.BoxSizer()
            sizer.Add(tree, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.frame = frame
            self.SetTopWindow(frame)
            return True

        def on_tree_sel_changed(self, evt):
            tree = evt.GetEventObject()
            selected_id = tree.GetSelection()
            if selected_id is not None:
                wx.MessageBox(tree.GetItemText(selected_id), 'Item selected', wx.OK)

    class App2(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'DatasourcePanel Demo')
            ds = Datasource()
            fs_ds_page = FilesystemDatasourcePage(frame, -1, datasource=ds)
            fs_ds_page.root_path = ec4vis_test_root
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(fs_ds_page, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.Bind(EVT_DATASOURCE_CHANGED, self.OnDatasourceChanged)
            self.fs_ds_page = fs_ds_page
            self.frame = frame
            self.SetTopWindow(frame)
            return True

        def OnDatasourceChanged(self, event):
            wx.MessageBox(
                self.fs_ds_page.datasource.uri, 'Datasource changed', wx.OK)

    # app = App1(0)
    app = App2(0)
    app.MainLoop()
