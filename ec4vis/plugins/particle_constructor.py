# coding: utf-8
"""ec4vis.plugins.particle_constructor --- Particle constructor from HDF5Data.
"""
import wx, wx.aui

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


class ParticlesSpec(PipelineSpec):
    pass

class SpeciesTableSpec(PipelineSpec):
    pass

class WorldSizeSpec(PipelineSpec):
    pass

class ParticleConstructorNode(PipelineNode):
    """
    """
    INPUT_SPEC = [Hdf5DataSpec]
    OUTPUT_SPEC = [ParticlesSpec, SpeciesTableSpec, WorldSizeSpec]
    def __init__(self, *args, **kwargs):
        """Initializer.
        """
        self._hdf5_data = None
        PipelineNode.__init__(self, *args, **kwargs)

    @log_call
    def internal_update(self):
        """Reset cached particles
        """
        self._hdf5_data = None

    @property
    def hdf5_data(self):
        """Property getter for hdf5_data.
        """
        if self._hdf5_data is None:
            self._hdf5_data = self.parent.request_data(Hdf5DataSpec)
        return self._hdf5_data

    @property
    def data_section(self):
        """Property getter for hdf5_data:/data section.
        """
        if self.hdf5_data is None:
            return None
        return self.hdf5_data.get('/data', None)
        
        
    @property
    def particles(self):
        """Property getter for particles
        """
        if self.data_section is None:
            return None
        data_keys = self.data_section.keys()
        if bool(data_keys)==False:
            return None
        particles_section = self.data_section.values()[0].get('particles', None)
        if particles_section is None:
            return None
        return dict(
            (id, dict(species_id=spid, position=pos))
            for id, spid, pos in particles_section.value)

    @property
    def species_table(self):
        """Property getter for species table.
        """
        if self.hdf5_data is None:
            return None
        species_section = self.hdf5_data.get('/species', None)
        if species_section is None:
            return None
        return dict(
            (id, dict(name=name, radius=radius, D=D))
            for id, name, radius, D in species_section.value)

    @property
    def world_size(self):
        """Property getter for world size.
        """
        if self.data_section is None:
            return None
        attrs = self.data_section.attrs
        if bool(attrs)==False:
            return None
        return attrs.get('world_size', None)

    def request_data(spec, **kwargs):
        """Provides data for children.
        """
        if spec is ParticlesSpec:
            return self.particles
        elif spec is SpeciesTableSpec:
            return self.species_table
        elif spec is WorldSizeSpec:
            return self.world_size


register_pipeline_node(ParticleConstructorNode)
