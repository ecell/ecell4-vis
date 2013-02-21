# coding: utf-8
"""ec4vis.plugins.hdf5_bundle_loader --- HDF5 bundle loader plugin.
"""
import glob, os.path
from urlparse import urlparse
from h5py import File
import wx, wx.aui

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.inspector.page import InspectorPage, register_inspector_page
from ec4vis.logger import debug, log_call, warning
from ec4vis.pipeline import PipelineNode, UpdateEvent, UriSpec, register_pipeline_node
from ec4vis.pipeline.specs import Hdf5DataSpec, NumberOfItemsSpec


class FileBundle(object):

    def __init__(self, path, glob_pattern='*', sorter=sorted):
        self._path = path
        self.glob_pattern = glob_pattern
        self._cache = None
        self.sorter = sorter

    def get_path(self):
        return self._path

    def set_path(self, path):
        self._cache = None
        self._path = path

    path = property(get_path, set_path)

    @property
    def is_ok(self):
        return os.path.exists(self.path)

    @property
    def cache(self):
        if self._cache is None:
            if os.path.isdir(self.path):
                path_list = glob.glob(
                    os.path.join(self.path, self.glob_pattern))
                if self.sorter:
                    path_list = self.sorter(path_list)
                self._cache = path_list
            else:
                self._cache = [self.path]
        return self._cache

    @property
    def n_files(self):
        return len(self.cache)
                
    def get_path_at(self, index):
        if self.is_ok:
            return self.cache.get(index, None)
        return None
        

class Hdf5BundleLoaderNode(PipelineNode):
    """Bundled Hdf5 loader.    
    """
    INPUT_SPEC = [UriSpec]
    OUTPUT_SPEC = [Hdf5DataSpec, NumberOfItemsSpec]
    
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        self._bundle = None
        self._cache = None
        self.glob_pattern = '*'
        PipelineNode.__init__(self, *args, **kwargs)

    @log_call
    def internal_update(self):
        """Reset bundle and cached hdf5 data.
        """
        self._bundle = None
        self._cache = None

    @property
    def bundle(self):
        if self._bundle is None:
            uri = self.parent.request_data(UriSpec)
            parsed = urlparse(uri)
            fullpath = parsed.netloc+parsed.path
            self._bundle = FileBundle(fullpath, self.glob_pattern)
        return self._bundle

    @property
    def cache(self):
        if self._cache is None:
            self._cache = {}
        return self._cache

    @log_call
    def request_data(self, spec, **kwargs):
        """Provides particle data.
        """
        if spec==NumberOfItemsSpec:
            return self.bundle.n_files
        if spec==Hdf5DataSpec:
            index = kwargs.get('index', 0)
            data = self.cache.get(index, None)
            if data is None:
                path = self.bundle.get_path_at(index)
                if not(path is None):
                    data = File(path)
                    self.cache[index] = data
            return data
        return None


register_pipeline_node(Hdf5BundleLoaderNode)


class Hdf5BundleLoaderInspector(InspectorPage):
    """Sequential hdf5 selector inspector.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        InspectorPage.__init__(self, *args, **kwargs)
        glob_pattern_label = wx.StaticText(self, -1, 'Glob pattern')
        glob_pattern = wx.TextCtrl(self, -1, "%s" %self.target.glob_pattern)
        self.Bind(wx.EVT_TEXT, self.OnGlobPatternText, glob_pattern)
        self.sizer.Add(glob_pattern_label, 0, wx.ALL|wx.EXPAND, 5)
        self.sizer.Add(glob_pattern, 0, wx.ALL|wx.EXPAND, 5)
        self.glob_pattern = glob_pattern

    @log_call
    def OnGlobPatternText(self, event):
        pattern = self.glob_pattern.GetValue()
        if pattern:
            self.target.glob_pattern = pattern
            self.target.internal_update()
            for child in self.target.children:
                child.propagate_down(UpdateEvent(None))
            
    def update(self):
        self.glob_pattern.SetValue("%s" %self.target.glob_pattern)


register_inspector_page('Hdf5BundleLoaderNode', Hdf5BundleLoaderInspector)


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
