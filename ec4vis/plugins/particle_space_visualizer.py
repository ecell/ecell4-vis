# coding: utf-8
"""ec4vis.plugins.particle_space_visualizer --- ParticleSpace visualizer.
"""
import wx, wx.aui
import vtk
import numpy

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[: p.rindex(os.sep + 'ec4vis')])

from ec4vis.inspector.page import InspectorPage, register_inspector_page
from ec4vis.logger import debug, log_call, warning
from ec4vis.pipeline import PipelineNode, PipelineSpec, UpdateEvent, UriSpec, register_pipeline_node
from ec4vis.pipeline.specs import Hdf5DataSpec, NumberOfItemsSpec

from ec4vis.plugins.particle_csv_loader import ParticleSpaceSpec
from ec4vis.visualizer.page import register_visualizer_page
from ec4vis.visualizer.vtk3d.page import Vtk3dVisualizerPage
from ec4vis.visualizer.vtk3d.visual import ActorsVisual

class ParticleSpaceVisualizerNode(PipelineNode):
    """
    """
    INPUT_SPEC = [ParticleSpaceSpec, NumberOfItemsSpec]
    OUTPUT_SPEC = []

    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        # self._simple_visuals = []
        PipelineNode.__init__(self, *args, **kwargs)

        self.view_scale = 1e-6

    @log_call
    def fetch_particle_space(self, **kwargs):
        return self.parent.request_data(ParticleSpaceSpec, **kwargs)

    @log_call
    def internal_update(self):
        """Reset cached particles
        """
        pass

register_pipeline_node(ParticleSpaceVisualizerNode)

# def create_axes(minpos, maxpos, **params):
def create_axes(bounds, **params):
    # bounds = (minpos[0], maxpos[0], minpos[1],
    #           maxpos[1], minpos[2], maxpos[2])
    ranges = bounds

    axes = vtk.vtkCubeAxesActor2D()
    axes.SetBounds(bounds)
    axes.SetRanges(ranges)
    axes.SetLabelFormat('%g')
    # axes.SetFontFactor(1.5)
    axes.UseRangesOn()
    # axes.SetCornerOffset(0.0)

    tprop = vtk.vtkTextProperty()
    if 'color' in params.keys():
        tprop.SetColor(params['color'])
    # tprop.ShadowOn()
    axes.SetAxisTitleTextProperty(tprop)
    axes.SetAxisLabelTextProperty(tprop)

    return axes

class SimpleVisual(ActorsVisual):

    def __init__(self, *args, **kwargs):
        ActorsVisual.__init__(self, *args, **kwargs)

        self.particle_space = None
        self.view_scale = 1e-6
        self._axes = None
        self._actors_cache = {}

    def create_color_map(self, num_types):
        cmap = [(1, 0, 0), (0, 1, 0), (0, 0, 1),
            (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]
        if num_types > len(cmap):
            cmap += [(1, 1, 1)] * (num_types - len(cmap))
        return cmap

    def _get_actors(self):
        for sid, actor in self._actors_cache.items():
            self._renderer.RemoveActor(actor)
        self._actors_cache.clear()

        if self.particle_space is not None:
            bounds = [numpy.inf, 0.0, numpy.inf, 0.0, numpy.inf, 0.0]
            cmap = self.create_color_map(len(self.particle_space.species))
            for i, sid in enumerate(self.particle_space.species):
                particles = self.particle_space.list_particles(sid)
                points = vtk.vtkPoints()
                radius = 0.0
                for pid, particle in particles:
                    points.InsertNextPoint(
                        numpy.asarray(particle.position) / self.view_scale)
                    radius = max(particle.radius / self.view_scale, radius)

                points.ComputeBounds()
                b = points.GetBounds()
                bounds = [
                    min(bounds[0], b[0]), max(bounds[1], b[1]),
                    min(bounds[2], b[2]), max(bounds[3], b[3]),
                    min(bounds[4], b[4]), max(bounds[5], b[5])]

                poly_data = vtk.vtkPolyData()
                poly_data.SetPoints(points)
                source = vtk.vtkPointSource()
                source.SetRadius(radius)
                mapper = vtk.vtkGlyph3DMapper()
                mapper.SetSourceConnection(source.GetOutputPort())
                mapper.SetInputConnection(poly_data.GetProducerPort())
                actor = vtk.vtkActor()
                actor.SetMapper(mapper)
                actor.GetProperty().SetColor(cmap[i])
                self._actors_cache[sid] = actor

            self._renderer.ResetCamera(bounds)
            if self._axes is not None:
                self._renderer.RemoveViewProp(self._axes)
            self._axes = create_axes(bounds)
            self._axes.SetCamera(self._renderer.GetActiveCamera())
            self._renderer.AddViewProp(self._axes)

        debug('actors: %s' % self._actors_cache)
        return self._actors_cache

    def update(self, data):
        self.particle_space = data['particle_space']
        self.view_scale = data['view_scale']

class ParticleSpaceVisualizer(Vtk3dVisualizerPage):

    def __init__(self, *args, **kwargs):
        Vtk3dVisualizerPage.__init__(self, *args, **kwargs)

        self.simple_visual = SimpleVisual(renderer=self.renderer, name='simple')

    @log_call
    def update(self):
        ps = self.target.fetch_particle_space()
        self.simple_visual.update(
            dict(particle_space = ps, view_scale = self.target.view_scale))
        self.simple_visual.enable()
        self.render()

register_visualizer_page('ParticleSpaceVisualizerNode', ParticleSpaceVisualizer)

class ParticleSpaceVisualizerInspector(InspectorPage):
    """Inspector page for ParticleSpaceVisualizer.
    """
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        InspectorPage.__init__(self, *args, **kwargs)

        widgets = []

        self.index_entry = wx.TextCtrl(
            self, wx.ID_ANY, "0", style=wx.TE_PROCESS_ENTER)
        self.max_index_text = wx.StaticText(self, -1, 'Index (0)')
        # self.max_num_entry.Bind(wx.EVT_TEXT_ENTER, self.max_num_entry_updated)
        widgets.extend([
            (self.max_index_text, 0, wx.ALL | wx.EXPAND),
            (self.index_entry, 1, wx.ALL | wx.EXPAND)])

        self.view_scale_entry = wx.TextCtrl(
            self, wx.ID_ANY, "1e-6", style=wx.TE_PROCESS_ENTER)
        self.view_scale_entry.Bind(wx.EVT_TEXT_ENTER, self.view_scale_entry_updated)
        widgets.extend([
            (wx.StaticText(self, -1, 'Scale :'), 0, wx.ALL | wx.EXPAND),
            (self.view_scale_entry, 1, wx.ALL | wx.EXPAND)])

        # pack in FlexGridSizer.
        fx_sizer = wx.FlexGridSizer(cols=2, vgap=9, hgap=25)
        fx_sizer.AddMany(widgets)
        fx_sizer.AddGrowableCol(1)
        self.sizer.Add(fx_sizer, 1, wx.EXPAND | wx.ALL, 10)

    @log_call
    def view_scale_entry_updated(self, event):
        raw_value = self.view_scale_entry.GetValue().strip()
        value = 0.0
        try:
            value = float(raw_value)
        except ValueError:
            value = 0.0

        if value > 0:
            self.view_scale_entry.ChangeValue(str(value))
            self.target.view_scale = value
            # self.target.internal_update()
            self.target.status_changed()
            for child in self.target.children:
                child.propagate_down(UpdateEvent(None))
        else:
            self.view_scale_entry.ChangeValue(str(self.target.view_scale))

    @log_call
    def update(self):
        """Update UI.
        """
        max_num = self.target.parent.request_data(NumberOfItemsSpec)
        self.max_index_text.SetLabel('Index (%d)' % max_num)

register_inspector_page('ParticleSpaceVisualizerNode', ParticleSpaceVisualizerInspector)
