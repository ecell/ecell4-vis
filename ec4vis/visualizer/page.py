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

@log_call
def register_visualizer_page(page_class, name=None):
    """Registers new page class to registry.
    """
    if bool(name)==False:
        name = page_class.__name__
    VISUALIZER_PAGE_REGISTRY[name] = page_class
    debug('registered visualizer %s as %s' %(name, page_class))


class VisualizerPage(ObserverPage):
    """Abstract superclass for pages in a visualizer notebook.
    """
    def __init__(self, *args, **kwargs):
        ObserverPage.__init__(self, *args, **kwargs)


if __name__=='__main__':
    # TBD
    pass
