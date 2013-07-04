# coding: utf-8
"""ec4vis.plugins.particle_spatiocyte_loader --- Simple Spatiocyte data loader plugin.
"""
import os.path
from spatiocyte_log_reader import SpatiocyteLogReader
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

def load_particles_from_spatiocyte(filename, index=0, ps=None):
    if not os.path.isfile(filename):
        return ps

    if ps is None:
        ps = ParticleSpace()

    reader = SpatiocyteLogReader(filename)
    try:
        species = reader.skipSpeciesTo(index)
        pid = 0
        molecules = species['Molecules'];
        for sp in molecules:
            index = sp['index']
            radius = #TODO float
            sid = #TODO
            for coor in sp['Coords']:
                pos = #TODO
                ps.add_particle(pid, Particle(sid, pos, radius))
                pid += 1
    finally:
        fin.close()
    return ps

class ParticleSpatiocyteLoaderProgressDialog(wx.ProgressDialog):
# TODO introduce index

    def __init__(self, filenames):
        wx.ProgressDialog.__init__(
            self, "Loading ...",
            "File remaining", len(filenames),
            style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)

        self.filenames = filenames

    def Show(self):
        ps = ParticleSpace()

        for i, filename in enumerate(self.filenames):
            ps = load_particles_from_spatiocyte(filename, ps)
            if not self.Update(i):
                return None
        return ps

class ParticleSpatiocyteLoaderNode(PipelineNode):
    """Simple Spatiocyte loader.
    """
    INPUT_SPEC = [UriSpec]
    OUTPUT_SPEC = [ParticleSpaceSpec, NumberOfItemsSpec]

    def __init__(self, *args, **kwargs):
        self._particle_space = None
        self._uri = None
        PipelineNode.__init__(self, *args, **kwargs)

    @log_call
    def internal_update(self):
        """Reset cached spatiocyte data.
        """
        self._particle_space = None

    def load_spatiocyte_file(self, fullpath):
        rexp = re.compile('(.+)\.dat$')
        mobj = rexp.match(fullpath)
        if mobj is None:
            raise IOError, 'No suitable file.'

        filenames = glob.glob(fullpath)
        if len(filenames) > 1:
            dialog = ParticleSpatiocyteLoaderProgressDialog(glob.glob(fullpath))
            #dialog = ParticleSpatiocyteLoaderProgressDialog(filenames) FIXME
            ps = dialog.Show()
            dialog.Destroy()
        elif len(filenames) == 1:
            ps = load_particles_from_spatiocyte(filenames[0])
        else:
            ps = None
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

            debug('spatiocyte data uri=%s' % uri)

            try:
                parsed = urlparse(uri)
                fullpath = parsed.netloc + parsed.path
                self._particle_space = self.load_spatiocyte_file(fullpath)
            except IOError, e:
                warning('Failed to open %s: %s', fullpath, str(e))
                pass

        # self._particle_space is left None if something wrong in loading data.
        return self._particle_space

    @log_call
    def request_data(self, spec, **kwargs):
    # TODO
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


register_pipeline_node(ParticleSpatiocyteLoaderNode)


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags = ELLIPSIS)
