# coding: utf-8
"""ec4vis.datasource.page --- Datasource page in visualizer application.
"""
import wx, wx.aui

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug
from ec4vis.datasource import Datasource


class DatasourcePage(wx.Panel):
    """Abstract superclass for pages in a datasource notebook.
    """
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        datasource_class = self.get_datasource_class()
        self.datasource = datasource_class()

    def get_datasource_class(self):
        """Returns datasource class. Subclass should override.
        """
        return Datasource

    def datasource_changed(self):
        """A hook to notify any datasource changes to app.
        """
        debug('DatasorucePage::datasource_changed()')
        app = wx.GetApp()
        handler = getattr(app, 'on_datasource_changed', None)
        if handler:
            debug('calling App::on_datasource_changed...')
            handler(self)
        else:
            debug('no handlers, skipped.')


if __name__=='__main__':
    # TBD
    pass
