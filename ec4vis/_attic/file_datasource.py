# coding: utf-8
"""file_datasource.py -- Filesystem based datasource.
"""
from logging import debug
from os import getcwd

import wx

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.browser import BrowserFrame
from ec4vis.plugins import PluginLoader
from ec4vis.version import VERSION


class FileDatasourcePanel(wx.Panel):
    """Data panel for browser.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        wx.Panel.__init__(self, *args, **kwargs)
        # datasource tree control
        tree_ctrl = DatasourceTree(
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
        

