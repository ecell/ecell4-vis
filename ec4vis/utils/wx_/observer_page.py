# coding: utf-8
"""ec4vis.utils.wx_.observer_page --- 
"""
import wx, wx.aui

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call
from ec4vis.pipeline import Observer


class ObserverPage(wx.Panel, Observer):
    """Abstract superclass for observer pages
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        # this should be before superclass initializer.
        target = kwargs.pop('target')
        self._sizer = None # this should be before parent's __init__
        Observer.__init__(self, target) # this will bind self.target
        wx.Panel.__init__(self, *args, **kwargs)

    @property
    def sizer(self):
        """Lazy sizer property.
        """
        if self._sizer is None:
            self._sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self._sizer)
        return self._sizer

    @log_call
    def finalize(self):
        """Finalizer.
        """
        self.unbind_target()


if __name__=='__main__':
    # TBD
    pass
