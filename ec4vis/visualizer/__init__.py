# coding: utf-8
"""ec4vis.visualizer -- visualizer class.
"""

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, info, logger, DEBUG
from ec4vis.pipeline import PipelineNode


class VisualizerNode(PipelineNode):
    """Abstract superclass for visualizer node.
    """
    def __init__(self, *args, **kwargs):
        render_window = kwargs.pop('render_window', None)
        PipelineNode.__init__(self, *args, **kwargs)
        self._render_window = render_window

    def get_render_window(self):
        return self._render_window

    def set_render_window(self, render_window):
        self._render_window = render_window

    render_window = property(get_render_window, set_render_window)


# initialize built-in visualizer classes
import ec4vis.visualizer.vtk3d


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
