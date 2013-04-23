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
    INPUT_SPEC = [ParticleSpaceSpec]
    OUTPUT_SPEC = []

    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        self._simple_visuals = []
        PipelineNode.__init__(self, *args, **kwargs)

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
            print self.particle_space
            cmap = self.create_color_map(len(self.particle_space.species))
            for i, sid in enumerate(self.particle_space.species):
                particles = self.particle_space.list_particles(sid)
                points = vtk.vtkPoints()
                radius = 0.0
                for pid, particle in particles:
                    points.InsertNextPoint(numpy.asarray(particle.position) / 3e-6)
                    radius = max(particle.radius / 3e-6, radius)

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

class ParticleSpaceVisualizer(Vtk3dVisualizerPage):

    def __init__(self, *args, **kwargs):
        Vtk3dVisualizerPage.__init__(self, *args, **kwargs)

        self.simple_visual = SimpleVisual(renderer=self.renderer, name='simple')

    @log_call
    def update(self):
        self.simple_visual.update(
            dict(particle_space = self.target.parent.particle_space))
        self.simple_visual.enable()
        self.render()

register_visualizer_page('ParticleSpaceVisualizerNode', ParticleSpaceVisualizer)

