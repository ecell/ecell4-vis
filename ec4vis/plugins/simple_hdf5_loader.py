# coding: utf-8
"""ec4vis.plugins.simple_hdf5_loader --- Simple HDF5 data loader plugin.
"""
import os.path
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
from ec4vis.pipeline import PipelineNode, PipelineSpec, UpdateEvent, UriSpec, register_pipeline_node


class Hdf5FileSpec(PipelineSpec):
    pass


class SimpleHdf5LoaderNode(PipelineNode):
    """Simple Hdf5 loader.

    >>> this_filepath = os.path.abspath(__file__)
    >>> ec4vis_parent = this_filepath[:this_filepath.rindex(os.sep+'ec4vis')]
    >>> ec4vis_test_root = os.path.join(ec4vis_parent, 'tests', 'data', 'hdf5')
    >>> test_filename = os.path.join(ec4vis_test_root, 'particle', 'dimer_particle_0005.hdf5')
    >>> from ec4vis.datasource import Datasource
    >>> from ec4vis.pipeline import RootPipelineNode
    >>> root_node = RootPipelineNode(datasource=Datasource(uri=test_filename))
    >>> hdf5_node = SimpleHdf5LoaderNode()
    >>> hdf5_node.connect(root_node)
    >>> hdf5_node.request_data(Hdf5FileSpec)
    <HDF5 file "dimer_particle_0005.hdf5" (mode r+)>
    
    """
    INPUT_SPEC = [UriSpec]
    OUTPUT_SPEC = [Hdf5FileSpec]
    def __init__(self, *args, **kwargs):
        self._hdf5_data = None
        PipelineNode.__init__(self, *args, **kwargs)

    def handle_downward_event(self, pipeline_event):
        if isinstance(pipeline_event, UpdateEvent):
            self.status_changed()

    @log_call
    def internal_update(self):
        """Reset cached hdf5 data.
        """
        self._hdf5_data = None

    @property
    def hdf5_data(self):
        """Property getter for hdf5_data
        """
        # examine cache
        if self._hdf5_data:
            pass
        else: # self._hdf5_data is None
            uri = self.parent.request_data(UriSpec)
            if uri is None:
                return
            debug('hdf5 data uri=%s' % uri)
            try:
                parsed = urlparse(uri)
                fullpath = parsed.netloc+parsed.path
                if os.path.exists(fullpath):
                    self._hdf5_data = File(fullpath)
            except IOError, e:
                warning('Failed to open %s: %s', fullpath, str(e))
                pass
        # self._hdf5_data is left None if something wrong in loading data.
        return self._hdf5_data

    @log_call
    def request_data(self, spec, **kwargs):
        """Provides particle data.
        """
        if spec is Hdf5FileSpec:
            data = self.hdf5_data
            return self.hdf5_data # this may be None if datasource is not valid.
        return None
            

register_pipeline_node(SimpleHdf5LoaderNode)


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
