# coding: utf-8
"""ec4vis.plugins.particle_visualizer --- Particle visualizer.
"""
import wx, wx.aui
import vtk

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.inspector.page import InspectorPage, register_inspector_page
from ec4vis.logger import debug, log_call, warning
from ec4vis.pipeline import PipelineNode, PipelineSpec, UpdateEvent, UriSpec, register_pipeline_node
from ec4vis.pipeline.specs import Hdf5DataSpec, NumberOfItemsSpec

from ec4vis.plugins.particle_constructor import ParticlesSpec, SpeciesTableSpec, WorldSizeSpec
from ec4vis.visualizer.page import register_visualizer_page
from ec4vis.visualizer.vtk3d.page import Vtk3dVisualizerPage
from ec4vis.visualizer.vtk3d.visual import ActorsVisual


class ParticleVisualizerNode(PipelineNode):
    """
    """
    INPUT_SPEC = [ParticlesSpec, SpeciesTableSpec, WorldSizeSpec]
    OUTPUT_SPEC = []
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        self._particle_visuals = []
        PipelineNode.__init__(self, *args, **kwargs)

    @log_call
    def internal_update(self):
        """Reset cached particles
        """

        

register_pipeline_node(ParticleVisualizerNode)


class ParticlesVisual(ActorsVisual):

    def __init__(self, *args, **kwargs):
        ActorsVisual.__init__(self, *args, **kwargs)
        self.world_size = None
        self.species_table = None
        self.particles = None
        self.scaling = 1.0
        self._actors_cache = {}

    def _get_actors(self):
        for actor in self._actors_cache.values():
            self._renderer.RemoveActor(actor)
            
        if self.species_table and self.world_size and self.particles:
            for sp_id, info in self.species_table.items():
                name = info['name']
                radius = info['radius']
                D = info['D']
                points = vtk.vtkPoints()
                for p_id, p_info in self.particles.items():
                    if p_info['species_id']==sp_id:
                        points.InsertNextPoint(p_info['position']*self.scaling/self.world_size)
                poly_data = vtk.vtkPolyData()
                poly_data.SetPoints(points)
                source = vtk.vtkPointSource()
                source.SetRadius(radius*self.scaling/self.world_size)
                mapper = vtk.vtkGlyph3DMapper()
                mapper.SetSourceConnection(source.GetOutputPort())
                mapper.SetInputConnection(poly_data.GetProducerPort())
                actor = vtk.vtkActor()
                actor.SetMapper(mapper)
                self._actors_cache[sp_id] = actor
        debug('actors: %s' %self._actors_cache)
        return self._actors_cache

    def update(self, data):
        self.world_size=data['world_size']
        self.species_table=data['species_table']
        self.particles=data['particles']



class ParticleVisualizer(Vtk3dVisualizerPage):

    def __init__(self, *args, **kwargs):
        Vtk3dVisualizerPage.__init__(self, *args, **kwargs)
        self.particles_visual = ParticlesVisual(
            renderer=self.renderer,
            name='particles')

    def update(self):
        self.particles_visual.update(
            dict(world_size=self.target.parent.world_size,
                 species_table=self.target.parent.species_table,
                 particles=self.target.parent.particles))
        self.particles_visual.enable()
        self.render()

register_visualizer_page('ParticleVisualizerNode', ParticleVisualizer)

