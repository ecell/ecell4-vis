# coding: utf-8
"""ec4vis.plugins.simple_hdf5_loader_inspector --- Inspector for Simple HDF5 data loader plugin.
"""
from urlparse import urlparse
from h5py import File
import wx, wx.aui

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call, warning
from ec4vis.pipeline import PipelineNode, PipelineSpec, UriSpec, register_pipeline_node
from ec4vis.inspector.page import InspectorPage, register_inspector_page


class SimpleHdf5LoaderInspector(InspectorPage):
    """Inspector page for SimpleHdf5Loader.
    """
    PROP_NAMES = ['filename', 'mode', 'driver', 'libver', 'userblock_size',
                  'name', 'id', 'ref', 'attrs']
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        InspectorPage.__init__(self, *args, **kwargs)
        widgets = []
        # create inspector fields for common h5py.File attributes.
        for prop_name in self.PROP_NAMES:
            label = wx.StaticText(self, -1, prop_name.capitalize())
            text_ctrl = wx.TextCtrl(self, -1, '', style=wx.TE_READONLY)
            setattr(self, prop_name, text_ctrl)
            widgets.extend([
                (label, 0, wx.ALL|wx.EXPAND),
                (text_ctrl, 1, wx.ALL|wx.EXPAND)])
        # pack in FlexGridSizer.
        fx_sizer = wx.FlexGridSizer(cols=2, vgap=5, hgap=5)
        fx_sizer.AddMany(widgets)
        fx_sizer.AddGrowableCol(1)
        self.sizer.Add(fx_sizer, 1, wx.EXPAND|wx.ALL, 10)

    @log_call
    def update(self):
        """Update UI.
        """
        if self.target and hasattr(self.target, 'hdf5_data'):
            hdf5_data = self.target.hdf5_data
            debug('hdf5_data at %s' %(hdf5_data))
            if hdf5_data:
                # glob attributes from the hdf5 data.
                for prop_name in self.PROP_NAMES:
                    widget = getattr(self, prop_name, None)
                    prop_value = getattr(hdf5_data, prop_name, None)
                    if widget and prop_value:
                        widget.SetValue(str(prop_value))
                return
        # else fallback
        debug('**** not found: %s, %s' %(self.target, self.target.hdf5_data))
        for prop_name in self.PROP_NAMES:
            widget = getattr(self, prop_name, None)
            if widget:
                widget.SetValue('')


register_inspector_page('SimpleHdf5LoaderNode', SimpleHdf5LoaderInspector)


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
