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
from ec4vis.inspector import Inspector


# inspector page registry
INSPECTOR_PAGE_REGISTRY = {}

@log_call
def register_inspector_page(node_class_name, page_class):
    """Register new page class to registry.
    """
    INSPECTOR_PAGE_REGISTRY[node_class_name] = page_class
    debug('registered inspector %s for pipeline node type %s' %(page_class, node_class_name))
    

class InspectorPage(wx.Panel, Inspector):
    """Abstract superclass for pages in a inspector notebook.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        # this should be before superclass initializer.
        target = kwargs.pop('target')
        wx.Panel.__init__(self, *args, **kwargs)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)
        self.target = target
        if self.target:
            self.target.add_observer(self)
            debug('added %s to %s\'s ovservers.' %(self, target))

    @log_call
    def update(self):
        """Update UI to reflect target status. Subclass should override.
        """
        pass

    @log_call
    def finalize(self):
        """Finalizer.
        """
        if self.target:
            self.target.remove_observer(self)



if __name__=='__main__':
    # TBD
    pass
