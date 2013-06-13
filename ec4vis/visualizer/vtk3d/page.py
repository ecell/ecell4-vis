# coding: utf-8
"""ec4vis.visuaizer.vtk3d.page --- Visualizer panel in visualizer application.
"""
import numpy
import vtk
import wx, wx.aui

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, info, log_call
from ec4vis.visualizer.page import VisualizerPage
from ec4vis.visualizer.vtk3d import Vtk3dVisualizerNode
from ec4vis.visualizer.vtk3d.render_window import RenderWindowMixin
from ec4vis.visualizer.vtk3d.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor


class Vtk3dVisualizerPage(VisualizerPage, RenderWindowMixin):
    """Abstract superclass for pages in a visualizer notebook.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        aspect_ratio = kwargs.pop('aspect_ratio', (4, 3))
        VisualizerPage.__init__(self, *args, **kwargs)
        RenderWindowMixin.__init__(self, aspect_ratio=aspect_ratio)
        # XXX dirty! XXX Inject RenderEvent callback 
        self.render_window._Iren.AddObserver('RenderEvent', self.ObserverRenderEventHandler)
        # bind default renderer
        default_renderer = getattr(self.target, 'renderer')
        if default_renderer:
            self.add_renderer(default_renderer)
            self.render_window.Enable(True)

    def ObserverRenderEventHandler(self, observer, event, fromobj=None):
        self.target.status_changed(exclude_observers=[self])

    def finalize(self):
        """Finalize page, visualizer
        """
        RenderWindowMixin.finalize(self)
        VisualizerPage.finalize(self)

        
        
if __name__=='__main__':

    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'DatasourcePanel Demo')
            # Node provides vtkRenderer.
            visualizer_node = Vtk3dVisualizerNode()
            # Panel provides wxVtkRenderWindowInteractor.
            visualizer_panel = Vtk3dVisualizerPage(frame, -1, target=visualizer_node)
            sizer = wx.BoxSizer()
            sizer.Add(visualizer_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            # configure renderer.
            renderer = visualizer_node.renderer
            source = vtk.vtkConeSource()
            source.SetResolution(64)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(source.GetOutput())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            renderer.AddActor(actor)
            # add renderer to the window.
            visualizer_panel.add_renderer(renderer)
            return True

    app = App(0)
    app.MainLoop()
