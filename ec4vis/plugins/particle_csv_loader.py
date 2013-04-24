# coding: utf-8
"""ec4vis.plugins.particle_csv_loader --- Simple CSV data loader plugin.
"""
import os.path
import csv
import re
import glob
from urlparse import urlparse
import wx, wx.aui

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[: p.rindex(os.sep + 'ec4vis')])

from ec4vis.logger import debug, log_call, warning
from ec4vis.pipeline import PipelineNode, PipelineSpec, UpdateEvent, UriSpec, register_pipeline_node
from ec4vis.pipeline.specs import NumberOfItemsSpec
from ec4vis.plugins.particle_space import Particle, ParticleSpace

class ParticleSpaceSpec(PipelineSpec):
    pass

class ParticleCSVLoaderNode(PipelineNode):
    """Simple CSV loader.
    """
    INPUT_SPEC = [UriSpec]
    OUTPUT_SPEC = [ParticleSpaceSpec, NumberOfItemsSpec]

    def __init__(self, *args, **kwargs):
        self._particle_space = None
        self._uri = None
        PipelineNode.__init__(self, *args, **kwargs)

    @log_call
    def internal_update(self):
        """Reset cached csv data.
        """
        self._particle_space = None

    def load_csv_file(self, fullpath):
        debug("load_csv_file [%s]." % fullpath)
        rexp = re.compile('(.+)\.csv$')
        mobj = rexp.match(fullpath)
        if mobj is None:
            raise IOError, 'No suitable file.'
        debug("load_csv_file ... start [%s]." % fullpath)

        particles = {}
        ps = ParticleSpace()
        for filename in glob.glob(fullpath):
            if not os.path.isfile(filename):
                continue
            debug("load_csv_file ... loading [%s]." % filename)
            fin = open(filename, 'r')
            try:
                line = fin.readline() # skip the first line

                reader = csv.reader(fin)
                for row in reader:
                    pos = [float(column) for column in row[: 3]]
                    radius = float(row[3])
                    pid = row[4] # eval(row[4])
                    sid = row[5] # eval(row[5])

                    p = Particle(sid, pos, radius)
                    ps.add_particle(pid, p)

                    if sid in particles.keys():
                        particles[sid].append((pos, radius, pid, sid))
                    else:
                        particles[sid] = [(pos, radius, pid, sid)]
            finally:
                fin.close()
        return ps

    def fetch_particle_space(self, **kwargs):
        """Property getter for particle_space
        """
        # examine cache
        uri = self.parent.request_data(UriSpec, **kwargs)
        if not (self._uri == uri):
            self._particle_space = None
            self._uri = uri

        if self._particle_space:
            pass
        else: # self._particle_space is None
            if uri is None:
                return

            debug('csv data uri=%s' % uri)

            try:
                parsed = urlparse(uri)
                fullpath = parsed.netloc + parsed.path
                self._particle_space = self.load_csv_file(fullpath)
            except IOError, e:
                warning('Failed to open %s: %s', fullpath, str(e))
                pass

        # self._particle_space is left None if something wrong in loading data.
        return self._particle_space

    @log_call
    def request_data(self, spec, **kwargs):
        """Provides particle data.
        """
        if spec == NumberOfItemsSpec:
            debug('Serving NumberOfItemsSpec')
            if self.fetch_particle_space(**kwargs) is None:
                return 0
            else:
                return 1
        elif spec == ParticleSpaceSpec:
            debug('Serving ParticleSpaceSpec')
            # this may be None if datasource is not valid.
            return self.fetch_particle_space(**kwargs) 
        return None
            

register_pipeline_node(ParticleCSVLoaderNode)


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags = ELLIPSIS)
