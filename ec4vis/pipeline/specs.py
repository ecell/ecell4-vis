# coding: utf-8
"""ec4vis.pipeline.specs --- Built-in DataSpec definitions.
"""
# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.pipeline import PipelineSpec


class Hdf5DataSpec(PipelineSpec):
    """Specifies HDF5 data.
    """
    pass

class NumberOfItemsSpec(PipelineSpec):
    """Specifies number of items.
    """
    pass
