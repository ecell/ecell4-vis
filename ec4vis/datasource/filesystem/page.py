# coding: utf-8
"""ec4vis.datasource.filesystem.page --- Notebook page for filesyste-based datasource.
"""
import os.path

import wx, wx.aui
from wx.lib.filebrowsebutton import DirBrowseButton

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.datasource.filesystem import FilesystemDatasource
from ec4vis.datasource.page import DatasourcePage
from ec4vis.datasource.filesystem.tree import FilesystemTree


class FilesystemDatasourcePage(DatasourcePage):
    """Notebook page for filesystem based datasource.
    """
    def __init__(self, *args, **kwargs):
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
            wx.EVT_TREE_SEL_CHANGED, self.on_tree_sel_changed)
        # layout stuff
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(dir_browse_button, 0, wx.ALL|wx.EXPAND, 0)
        sizer.Add(tree_ctrl, 1, wx.ALL|wx.EXPAND, 0)
        self.SetSizer(sizer)
        self.Layout()

    def get_datasource_class(self):
        """Always returns FilesystemDatasource.
        """
        return FilesystemDatasource

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

    def dir_browse_callback(self, evt):
        """Handler for dir_browse_button's changeCallback.
        """
        tree_ctrl = getattr(self, 'tree_ctrl', None)
        if tree_ctrl:
            self.tree_ctrl.root_path = evt.GetString()
        # reset dataset (to file_path=None)
        self.datasource.file_path = None
        self.datasource_changed()

    def on_tree_sel_changed(self, evt):
        """Handler called on selection changed in tree ctrl.
        """
        selected_id = self.tree_ctrl.GetSelection()
        if isinstance(selected_id, wx.TreeItemId) and selected_id.IsOk():
            file_path = self.tree_ctrl.get_node_path(selected_id)
            self.datasource.path = os.path.abspath(file_path)
        else:
            self.datasource.path = ''
        self.datasource_changed()
        

if __name__=='__main__':
    
    this_filepath = os.path.abspath(__file__)
    ec4vis_parent = this_filepath[:this_filepath.rindex(os.sep+'ec4vis')]
    ec4vis_test_root = os.path.join(ec4vis_parent, 'tests', 'data', 'fs', 'root')
    
    from ec4vis.datasource.panel import DatasourcePanel

    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'DatasourcePanel Demo')
            fs_ds_page = FilesystemDatasourcePage(frame, -1)
            fs_ds_page.root_path = ec4vis_test_root
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(fs_ds_page, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.frame = frame
            self.SetTopWindow(frame)
            return True

        def on_datasource_changed(self, page):
            wx.MessageBox(
                page.datasource.uri, 'Datasource changed', wx.OK)

    app = App(0)
    app.MainLoop()
