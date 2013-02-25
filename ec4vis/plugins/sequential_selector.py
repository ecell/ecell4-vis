# coding: utf-8
"""ec4vis.plugins.sequential_selector --- sequential data selector plugin.
"""
import wx
from wx.grid import Grid
from urlparse import urlparse
from h5py import File

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.inspector.page import InspectorPage, register_inspector_page
from ec4vis.logger import debug, log_call, warning
from ec4vis.pipeline import PipelineNode, PipelineSpec, UriSpec, UpdateEvent, register_pipeline_node
from ec4vis.pipeline.specs import Hdf5DataSpec, NumberOfItemsSpec


class SequentialHdf5SelectorNode(PipelineNode):
    """Node representing a selector of HDF5 data sequence.
    """
    INPUT_SPEC = [Hdf5DataSpec, NumberOfItemsSpec]
    OUTPUT_SPEC = [Hdf5DataSpec]

    def __init__(self, *args, **kwargs):
        self.index_cursor = 0
        PipelineNode.__init__(self, *args, **kwargs)

    def save(self):
        return dict(index_cursor=self.index_cursor)

    def restore(self, info):
        if isinstance(info, dict):
            self.index_cursor = info.get('index_cursor', 0)

    def internal_update(self):
        """Reset index cursor.
        """
        if self.index_cursor not in range(-self.n_data, self.n_data):
            self.index_cursor = 0

    @property
    def n_data(self):
        n = self.parent.request_data(NumberOfItemsSpec)
        if n is None:
            n = 0
        return n

    @property
    @log_call
    def selected_data(self):
        if self.index_cursor in range(-self.n_data, self.n_data):
            debug("retriving data at index=%s" %self.index_cursor)
            return self.parent.request_data(Hdf5DataSpec, index=self.index_cursor)
        else:
            warning('Index cursor is set to wrong value.')
        return None

    def request_data(self, spec, **kwargs):
        if spec is Hdf5DataSpec:
            return self.selected_data
        return None


register_pipeline_node(SequentialHdf5SelectorNode)


class SequentialHdf5SelectorInspector(InspectorPage):
    """Sequential hdf5 selector inspector.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        InspectorPage.__init__(self, *args, **kwargs)
        n_data_label = wx.StaticText(self, -1, 'Number of data')
        n_data = wx.TextCtrl(self, -1, "%s" %self.target.n_data, style=wx.TE_READONLY)
        cursor_label = wx.StaticText(self, -1, 'Current Index')
        cursor_spin = wx.SpinCtrl(self, -1, min=0, max=self.target.n_data, initial=self.target.index_cursor)
        self.Bind(wx.EVT_SPINCTRL, self.OnCursorSpin)
        data_label = wx.StaticText(self, -1, 'Selected data')
        data_text = wx.TextCtrl(self, -1, "%s" %self.target.selected_data, style=wx.TE_READONLY)
        self.sizer.Add(n_data_label, 0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(n_data, 0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(cursor_label, 0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(cursor_spin, 0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(data_label, 0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(data_text, 0, wx.ALL|wx.EXPAND, 5)
        self.n_data = n_data
        self.cursor_spin = cursor_spin
        self.data_text = data_text

    @log_call
    def OnCursorSpin(self, event):
        if self.target:
            self.target.index_cursor = self.cursor_spin.GetValue()
        self.target.propagate_down(UpdateEvent(None))

    def update(self):
        self.n_data.SetValue("%s" %self.target.n_data)
        self.cursor_spin.SetRange(0, self.target.n_data)
        self.cursor_spin.SetValue(self.target.index_cursor)
        self.data_text.SetValue("%s" %self.target.selected_data)


register_inspector_page('SequentialHdf5SelectorNode', SequentialHdf5SelectorInspector)


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
