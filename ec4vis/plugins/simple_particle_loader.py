# coding: utf-8
"""ec4vis.plugins.simple_particle_loader --- Simple Particle data loader plugin.
"""
from urlparse import urlparse

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[:p.rindex(os.sep+'ec4vis')])

from ec4vis.logger import debug, log_call
from ec4vis.pipeline import PipelineNode, PipelineSpec, UriSpec, register_pipeline_node


class ParticleDataSpec(PipelineSpec):
    pass


class SimpleParticleLoaderNode(PipelineNode):
    INPUT_SPEC = [UriSpec]
    OUTPUT_SPEC = [ParticleDataSpec]
    def __init__(self, *args, **kwargs):
        self._particle_data = None
        PipelineNode.__init__(self, *args, **kwargs)

    def internal_update(self):
        """Reset cached particle data.
        """
        self._particle_data = None

    @property
    def particle_data(self):
        """Property getter for particle_data
        """
        # examine cache
        if self._particle_data:
            pass
        else: # self._particle_data is None
            uri = self.parent.request_data(UriSpec)
            if isinstance(uri, str):
                parsed = urlparse(uri)
                fullpath = parsed.netloc+parsed.path
                if os.path.exists(fullpath):
                    pass #TBDDDDDDD
        # self._particle_data is left None if something wrong in loading data.
        return self._particle_data
        
    def request_data(self, spec):
        """Provides particle data.
        """
        if spec is ParticleDataSpec:
            return self.particle_data # this may be None if datasource is not valid.
        return None
            
register_pipeline_node(SimpleParticleLoaderNode)


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags=ELLIPSIS)
