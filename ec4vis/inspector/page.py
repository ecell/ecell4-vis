# coding: utf-8
"""ec4vis.inspector.page --- Inspector page in visualizer application.
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

# inspector page registry
INSPECTOR_PAGE_REGISTRY = {}


def register_inspector_page(node_class_name, page_class):
    """Register new page class to registry.
    """
    INSPECTOR_PAGE_REGISTRY[node_class_name] = page_class
    debug('Registered inspector %s for pipeline node type %s' %(page_class.__name__, node_class_name))


class InspectorPage(ObserverPage):
    """Abstract superclass for pages in a inspector notebook.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        # this should be before superclass initializer.
        ObserverPage.__init__(self, *args, **kwargs)


# load built-in inspectors
import ec4vis.inspector.datasource


if __name__=='__main__':
    # TBD
    pass
