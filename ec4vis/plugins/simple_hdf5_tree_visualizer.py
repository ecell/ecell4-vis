# coding: utf-8
"""ec4vis.plugins.simple_hdf5_loader --- Simple HDF5 data loader plugin.
"""
import wx
from wx.grid import Grid
from urlparse import urlparse

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.inspector.page import InspectorPage, register_inspector_page
from ec4vis.logger import debug, log_call, warning
from ec4vis.pipeline import PipelineNode, PipelineSpec, UriSpec, register_pipeline_node
from ec4vis.pipeline.specs import Hdf5DataSpec
from ec4vis.utils.wx_ import TreeCtrlPlus
from ec4vis.visualizer.page import VisualizerPage, register_visualizer_page


class SimpleHdf5TreeVisualizerNode(PipelineNode):
    """Node representing a simple hdf5 tree visualizer.
    """
    INPUT_SPEC = [Hdf5DataSpec]
    OUTPUT_SPEC = []
    def __init__(self, *args, **kwargs):
        PipelineNode.__init__(self, *args, **kwargs)
        self.node_cursor = None

    def internal_update(self):
        self.node_cursor = None
        debug('%s' %self.hdf5_data)

    @property
    @log_call
    def hdf5_data(self):
        if self.parent:
            return self.parent.request_data(Hdf5DataSpec)
        debug('No parent.')
            
register_pipeline_node(SimpleHdf5TreeVisualizerNode)


class Hdf5TreeCtrl(TreeCtrlPlus):
    """Tree ctrl for simple hdf5 tree visualizer.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        style = kwargs.pop('style', 0)|wx.TR_NO_BUTTONS|wx.TR_HAS_BUTTONS|wx.SUNKEN_BORDER
        kwargs['style'] = style
        self.selection_callback = kwargs.pop('selection_callback', None)
        TreeCtrlPlus.__init__(self, *args, **kwargs)
        self._hdf5_file = None

    def get_hdf5_file(self):
        """Property getter.
        """
        return self._hdf5_file

    @log_call
    def set_hdf5_file(self, hdf5_file):
        """Property setter; rebuilds tree on file change.
        """
        debug('Deleting tree')
        self.DeleteAllItems()
        if hdf5_file:
            debug('Valid hdf5 file at %x' % id(hdf5_file))
            node_name = "%s:: %s" %(
                hdf5_file.__class__.__name__,
                hdf5_file.name)
            root_id = self.AddRoot(node_name)
            self.SetPyData(root_id, hdf5_file)
            if hasattr(hdf5_file, 'items') and hdf5_file.items():
                self.SetItemHasChildren(root_id, True)
        self._hdf5_file = hdf5_file

    hdf5_file = property(get_hdf5_file, set_hdf5_file)

    def OnItemExpanding(self, event):
        """Event handler on item expanding.
        """
        item_id = event.GetItem()
        # retribe bound data to derive children.
        item_data = self.GetPyData(item_id)
        # add children
        for name, node in item_data.items():
            node_name = "%s:: %s" %(node.__class__.__name__, name)
            child_id = self.AppendItem(item_id, node_name)
            self.SetPyData(child_id, node)
            if hasattr(node, 'items') and node.items():
                self.SetItemHasChildren(child_id, True)

    def OnItemCollapsed(self, event):
        """Event handler on item collapsed.
        """
        item_id = event.GetItem()
        self.DeleteChildren(item_id)

    def OnSelChanged(self, event):
        """Event handler on item selected.
        """
        item_id = event.GetItem()
        if item_id and item_id.IsOk():
            node = self.GetPyData(item_id)
            node_path = node.name
            # update cursor of (page's) target node
            if self.selection_callback:
                self.selection_callback(node_path)


class SimpleHdf5TreeVisualizer(VisualizerPage):
    """Simple HDF5 tree visualizer.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        VisualizerPage.__init__(self, *args, **kwargs)
        tree = Hdf5TreeCtrl(self, -1, selection_callback=self.on_tree_select)
        self.sizer.Add(tree, 1, wx.ALL|wx.EXPAND, 5)
        self.tree = tree
        
    def update(self):
        """Observer update handler.
        """
        if not self.tree.hdf5_file==self.target.hdf5_data:
            self.tree.hdf5_file = self.target.hdf5_data

    def on_tree_select(self, node_path):
        """Callback from tree on selection change.
        """
        debug('node cursor set to  %s' %node_path)
        self.target.node_cursor = node_path
        self.target.status_changed()
            
register_visualizer_page('SimpleHdf5TreeVisualizerNode', SimpleHdf5TreeVisualizer)


class SimpleHdf5TreeInspector(InspectorPage):
    """Simple HDF5 tree inspector.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        InspectorPage.__init__(self, *args, **kwargs)
        # path text.
        path_label = wx.StaticText(self, -1, 'Path')
        path_text = wx.TextCtrl(self, -1, style=wx.TE_READONLY)
        # attributes grid.
        attr_label = wx.StaticText(self, -1, 'Attributes')
        attr_grid = Grid(self, -1, size=(-1, 100))
        attr_grid.CreateGrid(0, 2)
        attr_grid.SetColLabelValue(0, 'Key')
        attr_grid.SetColLabelValue(1, 'Value')
        attr_grid.EnableEditing(False)
        # values (for datasets) grid.
        vals_label = wx.StaticText(self, -1, 'Values')
        vals_grid = Grid(self, -1)
        vals_grid.CreateGrid(0, 0)
        vals_grid.EnableEditing(False)
        self.sizer.Add(path_label, 0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(path_text, 0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(attr_label, 0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(attr_grid, 0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(vals_label, 0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(vals_grid, 1, wx.ALL|wx.EXPAND, 5)
        self.path_text = path_text
        self.attr_grid = attr_grid
        self.vals_grid = vals_grid
        
    def update(self):
        """Observer update handler.
        """
        # reset values (delete existing rows for grids)
        self.path_text.SetValue('')
        self.attr_grid.SetRowLabelSize(0) # HideRowLabels()
        if self.attr_grid.GetNumberRows():
            self.attr_grid.DeleteRows(0, self.attr_grid.GetNumberRows())
        self.vals_grid.SetRowLabelSize(0) # HideRowLabels()
        if self.vals_grid.GetNumberRows():
            self.vals_grid.DeleteRows(0, self.vals_grid.GetNumberRows())
        if self.vals_grid.GetNumberCols():
            self.vals_grid.DeleteCols(0, self.vals_grid.GetNumberCols())
        # check for current node cursor of target.
        current_path = self.target.node_cursor
        hdf5_data = self.target.hdf5_data
        if (current_path is None) or (hdf5_data is None):
            return
        # current_path and hdf5_data is valid, let's inspect it.
        self.path_text.SetValue(current_path)
        node = hdf5_data.get(current_path)
        # for node having attrs, populate attrs grid.
        if hasattr(node, 'attrs'):
            n_attrs = len(node.attrs.items())
            grid = self.attr_grid
            grid.InsertRows(0, n_attrs)
            for row_idx, (key, value) in enumerate(node.attrs.items()):
                grid.SetCellValue(row_idx, 0, key)
                grid.SetCellValue(row_idx, 1, "%s" %value)
        # for node having value (implies dataset), populate values grid.
        if hasattr(node, 'value'):
            grid = self.vals_grid
            labels = node.dtype.names
            n_labels = len(labels)
            grid.InsertCols(0, n_labels)
            grid.InsertRows(0, node.len())
            for i, label in enumerate(labels):
                grid.SetColLabelValue(i, label)
            for row_idx, row_data in enumerate(node.value):
                for col_idx in range(n_labels):
                    grid.SetCellValue(row_idx, col_idx, "%s" %row_data[col_idx])
            
register_inspector_page('SimpleHdf5TreeVisualizerNode', SimpleHdf5TreeInspector)


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
