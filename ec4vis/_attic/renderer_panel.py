# coding: utf-8
"""renderer_panel.py -- Panel to wrap wxVTKRenderWindowInteractor.
"""

import numpy
import vtk
import wx

from wxVTKRenderWindowInteractor import wxVTKRenderWindowInteractor


class RendererPanel(wx.Panel):
    """A panel containing wxVTKRenderWindowInteractor.

    Attributes:
    render_window --- wxVTKRenderWindowInteractor instance.
    aspect_ratio --- aspect ratio of render_window. (w, h)-tuple.

    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        # extract aspect ratio, defaulting 4:3.
        self._aspect_ratio = kwargs.pop('aspect_ratio', (4, 3))
        super(RendererPanel, self).__init__(*args, **kwargs)
        render_window = wxVTKRenderWindowInteractor(self, -1)
        # binding
        self.render_window = render_window
        # events
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.setup_renderer()
        settings = kwargs.get('settings', None)
        if settings:
            self.configure_renderer(settings)

    def _get_aspect_ratio(self):
        return self._aspect_ratio

    def _set_aspect_ratio(self, aspect_ratio):
        self._aspect_ratio = aspect_ratio
        self.force_aspect_ratio(*self.GetSize())

    aspect_ratio = property(_get_aspect_ratio, _set_aspect_ratio)

    def configure_renderer(self, settings):
        """Configure rendering environment.
        """
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

    def setup_renderer(self):
        """Set up vtk renderers.
        """
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
        
    def OnSize(self, event):
        """Resize handler.
        """
        self.force_aspect_ratio(*event.GetSize())


if __name__=='__main__':
    # Run a demo application.
    class DemoApp(wx.App):
        """Demonstrative application.
        """
        ASPECT_RATIOS = [(4, 3), (16, 8)]
        def OnRadioSelect(self, event):
            aspect_ratio = self.ASPECT_RATIOS[event.GetInt()]
            self.render_window_panel.aspect_ratio = aspect_ratio

        def OnInit(self):
            frame = wx.Frame(None, -1, u'RendererPanel demo',
                             size=(400, 400))
            aspect_radio = wx.RadioBox(
                frame, -1,
                choices=['%s:%s' %ar for ar in self.ASPECT_RATIOS])
            renderer_panel = RendererPanel(frame, -1)
            frame.Bind(wx.EVT_RADIOBOX, self.OnRadioSelect)
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(aspect_radio, 0, wx.ALL|wx.EXPAND, 5)
            sizer.Add(renderer_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            self.SetTopWindow(frame)
            renderer = renderer_panel.renderer
            # stuff to be rendererd
            source = vtk.vtkConeSource()
            source.SetResolution(8)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInput(source.GetOutput())
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)
            renderer.AddActor(actor)
            return True

    app = DemoApp(0)
    app.MainLoop()
