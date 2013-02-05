# coding: utf-8
"""
Demonstrative plugin.

This plugin regisiters DemoVisualizer class.

"""
import vtk
from ec4vis.visual import ActorsVisual, MappedActorsVisual, StaticActorsVisual
from ec4vis.visualizer import register, Visualizer


class DemoConeVisual(StaticActorsVisual):
    """Static visual of a Cone source.
    """

    def _create_actors(self):
        """Creates demo cone actors.
        """
        cone = vtk.vtkConeSource()
        cone.SetResolution(8)
        coneMapper = vtk.vtkPolyDataMapper()
        coneMapper.SetInput(cone.GetOutput())
        coneActor = vtk.vtkActor()
        coneActor.SetMapper(coneMapper)
        self._actors['ConeActor'] = coneActor


class DemoUpdatingConeVisual(DemoConeVisual):
    """DemoConeVisual with update.
    """
    import random
    def update(self, data=None):
        if not self._actors:
            return
        cone = self._actors['ConeActor']
        prop = cone.GetProperty()
        camera = self._renderer.GetActiveCamera()
        if data is None:
            dop = camera.GetDirectionOfProjection()
        else:
            dop = data
        prop.SetColor(dop)


class DemoVisualizer(Visualizer):
    def initialize(self):
        self.visuals = {'Cone': DemoUpdatingConeVisual(self.renderer)}
        Visualizer.initialize(self)

    def process_source(self, source):
        import binascii, numpy
        shex = '%08x' %(binascii.crc32(source))
        rgb = numpy.array([abs(int(h, 16)/255.0) for h in shex[:2], shex[2:4], shex[4:6]])
        self.data_objects.append(
            [str(len(self.data_objects)), 'DemoType', source[:20], source, rgb])

        
# register to VISUALIZER_CLASSES registry.
register(DemoVisualizer)


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
            visualizer = DemoVisualizer(self, self.renderer)
            visualizer.initialize()
            visualizer.show()
            self.SetTopWindow(frame)
            return True

    app = VisualizerDemoApp(0)
    app.MainLoop()

    
