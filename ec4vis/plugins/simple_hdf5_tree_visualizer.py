# coding: utf-8
"""ec4vis.plugins.simple_hdf5_loader --- Simple HDF5 data loader plugin.
"""
from urlparse import urlparse
from h5py import File

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call, warning
from ec4vis.pipeline import PipelineNode, PipelineSpec, UriSpec, register_pipeline_node




if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
