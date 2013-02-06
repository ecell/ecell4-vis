# coding: utf-8

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call
from ec4vis.pipeline import register_pipeline_node, PipelineSpec
from ec4vis.visualizer import VisualizerNode


class Vtk3dVisualizerNode(VisualizerNode):
    """Visualizer class for VTK3D rendering view.

    >>> node = Vtk3dVisualizerNode()
    >>> node
    <Vtk3dVisualizerNode: vtk3dvisualizernode>
    
    """
    INPUT_SPEC = []
    OUTPUT_SPEC = []
    
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        VisualizerNode.__init__(self, *args, **kwargs)


if __name__=='__main__':
    # TBD test stuff.
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
    
