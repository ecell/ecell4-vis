# coding: utf-8
"""ec4vis.visuaizer.page --- Visualizer panel in visualizer application.
"""
import wx, wx.aui

# this stuff enables module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call


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


class VisualizerPage(wx.Panel):
    """Abstract superclass for pages in a visualizer notebook.
    """
    def __init__(self, *args, **kwargs):
        target = kwargs.pop('target')
        wx.Panel.__init__(self, *args, **kwargs)
        self.target = target

    @log_call
    def finalize(self):
        """Finalize visualizer page (and its visualizer).
        """
        if self.target and hasattr(self.target, 'finalize'):
            self.target.finalize()
        debug('finalized target %s' %(self.target.__class__.__name__))


if __name__=='__main__':
    # TBD
    pass
