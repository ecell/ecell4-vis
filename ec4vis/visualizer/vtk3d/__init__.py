# coding: utf-8

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug
from ec4vis.visualizer import Visualizer


class Vtk3dVisualizer(Visualizer):
    """Visualizer class for VTK3D rendering view.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        Visualizer.__init__(self, *args, **kwargs)
        self.render_window = None

    def set_render_window(self, render_window):
        """Set render window object.
        """
        debug('Vtk3dVisualizer::set_render_window() object at %s'
              %id(render_window))
        self.render_window = render_window


if __name__=='__main__':
    # TBD test stuff.
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
    
