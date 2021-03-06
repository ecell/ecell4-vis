# coding: utf-8
"""ec4vis.datasource.page --- Datasource page in visualizer application.
"""
import wx, wx.aui, wx.lib.newevent

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call
from ec4vis.datasource import Datasource

# Datasource change event
DatasourceChangedEvent, EVT_DATASOURCE_CHANGED = wx.lib.newevent.NewEvent()


# datasource page registry
DATASOURCE_PAGE_REGISTRY = {}

def register_datasource_page(page_class, name=None):
    """Registers new page class to registry.
    """
    if bool(name)==False:
        name = page_class.__name__
    DATASOURCE_PAGE_REGISTRY[name] = page_class
    debug('Registered datasource %s as %s' %(page_class.__name__, name))


class DatasourcePage(wx.Panel):
    """Abstract superclass for pages in a datasource notebook.
    """
    def __init__(self, *args, **kwargs):
        # this should be popped before superclass initializer.
        self.datasource = kwargs.pop('datasource')
        wx.Panel.__init__(self, *args, **kwargs)

    def finalize(self):
        """Finalizer.
        """
        # do nothing atm.

    def update_datasource(self):
        """Update datasource according to UI status. Subclass should override.
        """
        return NotImplemented

    def datasource_changed(self):
        """Posts DatasourceChangedEvent().

        Whenever you made any changes on underlying datasource, call this method.
        """
        wx.PostEvent(self, DatasourceChangedEvent())

    def save(self):
        """Save states. Subclass may override.
        """
        return None

    def restore(self, info):
        """Restore states. Subclass may override.
        """
        return


if __name__=='__main__':
    # TBD
    pass
