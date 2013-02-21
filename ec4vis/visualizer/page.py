# coding: utf-8
"""ec4vis.visuaizer.page --- Visualizer panel in visualizer application.
"""
import wx, wx.aui

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call
from ec4vis.utils.wx_.observer_page import ObserverPage

# visualizer page registry
VISUALIZER_PAGE_REGISTRY = {}


def register_visualizer_page(node_class_name, page_class):
    """Registers new page class to registry.
    """
    VISUALIZER_PAGE_REGISTRY[node_class_name] = page_class
    debug('Registered visualizer %s for pipeline node type %s' %(page_class.__name__, node_class_name))


class VisualizerPage(ObserverPage):
    """Abstract superclass for pages in a visualizer notebook.
    """
    def __init__(self, *args, **kwargs):
        ObserverPage.__init__(self, *args, **kwargs)


# load built-in visualizer page classes
import ec4vis.visualizer.vtk3d.page



if __name__=='__main__':
    # TBD
    pass
