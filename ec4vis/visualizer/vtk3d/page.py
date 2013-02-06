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
from ec4vis.visualizer.vtk3d.wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor


class Vtk3dVisualizerPage(VisualizerPage):
    """Abstract superclass for pages in a visualizer notebook.
    """
    def __init__(self, *args, **kwargs):
        settings = kwargs.pop('settings', None)
        VisualizerPage.__init__(self, *args, **kwargs)
        self._aspect_ratio = [4, 3]
        render_window = wxVTKRenderWindowInteractor(self, -1)
        self.target.render_window = render_window
        # bindings
        self.render_window = render_window
        # event bindings
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.setup_renderer()
        if settings:
            self.configure_renderer(settings)

    @log_call
    def finalize(self):
        """Finalize page, visualizer
        """
        VisualizerPage.finalize(self)

    def _get_aspect_ratio(self):
        return self._aspect_ratio

    @log_call
    def _set_aspect_ratio(self, aspect_ratio):
        self._aspect_ratio = aspect_ratio
        debug('forcing aspect ratio as %s' %aspect_ratio)
        self.force_aspect_ratio(*self.GetSize())

    aspect_ratio = property(_get_aspect_ratio, _set_aspect_ratio)

    @log_call
    def configure_renderer(self, settings):
        """Configure rendering environment.
        """
        debug('Vtk3dVisualizerPage::configure_renderer()')
        renderer = self.renderer
        # configure camera
        camera = renderer.GetActiveCamera()
        camera.SetFocalPoint(
            numpy.array(settings.camera_focal_point)*settings.scaling)
        camera.SetPosition(
            numpy.array(settings.camera_base_position)*settings.scaling)
        camera.Azimuth(settings.camera_azimuth)
        camera.Elevation(settings.camera_elevation)
        camera.SetViewAngle(settings.camera_view_angle)
        camera.SetParallelProjection(settings.camera_parallel_projection)
        camera.Zoom(settings.camera_zoom)
        # configure background
        renderer.SetBackground(settings.image_background_color)
        # configure lighting
        light_kit = vtk.vtkLightKit()
        light_kit.SetKeyLightIntensity(settings.light_intensity)
        light_kit.AddLightsToRenderer(renderer)

    @log_call
    def setup_renderer(self):
        """Set up vtk renderers.
        """
        debug('Vtk3dVisualizerPage::setup_renderer()')
        # Enable rendering
        self.render_window.Enable(1)
        # Hook exit event.
        self.render_window.AddObserver(
            'ExitEvent', lambda o,e,f=self: f.Close())
        # create renderer
        renderer = vtk.vtkRenderer()
        renderer.SetViewport(0.0, 0.0, 1.0, 1.0)
        # Register renderer
        self.render_window.GetRenderWindow().AddRenderer(renderer)
        self.renderer = renderer

    @log_call
    def force_aspect_ratio(self, width, height):
        """
        Force size of render_window to follow aspect ratio.

        Arguments:
        width --- preferred width of the window.
        height --- preferred height of the window.
        
        """
        aw, ah = self.aspect_ratio
        width = int(min(width, height*aw/float(ah)))
        height = int(min(height, width*ah/float(aw)))
        self.render_window.SetSize((width, height))

    @log_call
    def OnSize(self, event):
        """Resize handler.
        """
        self.force_aspect_ratio(*event.GetSize())

    @log_call
    def render(self):
        """Do real rendering action.
        """
        self.render_window.Render()

    @log_call
    def update(self):
        """Updates content of the rendering window.
        """
        self.render()
        
        
if __name__=='__main__':

    class App(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            """Initializer.
            """
            frame = wx.Frame(None, -1, u'DatasourcePanel Demo')
            visualizer_node = Vtk3dVisualizerNode()
            visualizer_panel = Vtk3dVisualizerPage(frame, -1, target=visualizer_node)
            sizer = wx.BoxSizer()
            sizer.Add(visualizer_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            renderer = visualizer_panel.renderer
            source = vtk.vtkConeSource()
            source.SetResolution(64)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(source.GetOutput())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            renderer.AddActor(actor)
            return True

    app = App(0)
    app.MainLoop()
