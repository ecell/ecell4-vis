# coding: utf-8

import h5py

from ec4vis.visualizer import register, Visualizer

from settings import ParticleSettings
from visual import *


class ParticleVisualizer(Visualizer):
    """Particle visualizer.
    """
    def initialize(self):
        ren = self.renderer
        settings = ParticleSettings()
        self.particle_settings = settings
        # configure camera
        camera = ren.GetActiveCamera()
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
        ren.SetBackground(settings.image_background_color)
        # configure lighting
        light_kit = vtk.vtkLightKit()
        light_kit.SetKeyLightIntensity(settings.light_intensity)
        light_kit.AddLightsToRenderer(ren)
        self.visuals['Species legend'] = SpeciesLegend(ren, settings=settings)
        self.visuals['Time legend'] = TimeLegend(ren, settings=settings)
        self.visuals['Wireframe'] = WireFrameCube(ren, settings=settings)
        self.visuals['Axes'] = Axes(ren, settings=settings)
        # self.visuals['Planes'] = Planes(ren, settings=settings)
        self.visuals['BlurryParticlesVolume'] = BlurryParticlesVolume(ren, settings=settings)
        Visualizer.initialize(self)

    def process_source(self, uri):
        # XXX quick hack XXX
        file_scheme_prefix = 'file://'
        if uri.startswith(file_scheme_prefix):
            uri = uri[len(file_scheme_prefix):]
        infile = h5py.File(uri)
        # due to legacy data persistency, it's quite dirty :( 
        world_size = infile.values()[0].attrs[u'world_size']
        self.visuals['BlurryParticlesVolume'].world_size = world_size
        self.visuals['Wireframe'].world_size = world_size
        self.visuals['Axes'].world_size = world_size
        data_id = infile.values()[0].keys()[0]
        data_name = str(infile.values()[0].values()[0].attrs[u't'])
        particles = infile.values()[0].values()[0].values()[0]
        data = {}
        scaling = self.particle_settings.scaling
        for pid, sid, pos in particles:
            # this is hack for performance...
            import vtk
            points = data.setdefault(sid, vtk.vtkPoints())
            points.InsertNextPoint(pos*scaling/world_size)
        self.data_objects.append(
            [data_id, 'Particle', data_name, data])

register(ParticleVisualizer)


if __name__=='__main__':
    """Demonstrative app.
    """
    import wx
    import vtk
    from ec4vis.render_window import RenderWindowPanel

    class VisualizerDemoApp(wx.App):
        """Demonstrative application.
        """
        def OnInit(self):
            frame = wx.Frame(None, -1, u'RenderWindowPanel demo',
                             size=(400, 400))
            render_window_panel = RenderWindowPanel(frame, -1)
            self.renderer = render_window_panel.renderer
            sizer = wx.BoxSizer(wx.VERTICAL)
            sizer.Add(render_window_panel, 1, wx.ALL|wx.EXPAND, 5)
            frame.SetSizer(sizer)
            frame.Layout()
            frame.Show(True)
            visualizer = ParticleVisualizer(self, self.renderer)
            visualizer.initialize()
            visualizer.show()
            self.SetTopWindow(frame)
            return True

    app = VisualizerDemoApp(0)
    app.MainLoop()
