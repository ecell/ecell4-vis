# coding: utf-8
"""ec4vis.visualizer -- visualizer class.
"""

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, info, log_call, DEBUG
from ec4vis.pipeline import PipelineNode


class VisualizerNode(PipelineNode):
    """Abstract superclass for visualizer node.
    """
    INPUT_SPEC = []
    OUTPUT_SPEC = []
    # pass


# load built-in visualizer classes
import ec4vis.visualizer.vtk3d


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
