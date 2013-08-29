# coding: utf-8
"""ec4vis.plugins.particle_spatiocyte_loader --- Simple Spatiocyte data loader plugin.
"""
import os.path
import re
import glob
from urlparse import urlparse
import wx, wx.aui

import struct

# this allows module-wise execution
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[: p.rindex(os.sep + 'ec4vis')])

from ec4vis.logger import debug, log_call, warning
from ec4vis.pipeline import PipelineNode, PipelineSpec, UpdateEvent, UriSpec, register_pipeline_node
from ec4vis.pipeline.specs import NumberOfItemsSpec

from ec4vis.plugins.particle_csv_loader import ParticleSpaceSpec

from ec4vis.plugins.lattice_space import LatticeParticle, OffLatticeParticle, LatticeParticleSpace

class SpatiocyteLogReadingException(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class SpatiocyteLogReader:

    def __init__(self, logfile):
        self.logfile = open(logfile, 'rb')
        self.readInitialization()
        self.readCompVacant()
        self.headerSeek = self.tell()
        self.logfile.seek(0,2)
        self.footerSeek = self.tell()
        self.logfile.seek(self.headerSeek)
        self._indexSize = -1

    def close(self):
        self.logfile.close()

    def tell(self):
        return self.logfile.tell()

    def isEnd(self):
        return self.tell() == self.footerSeek

    def getIndexSize(self):
        if self._indexSize != -1:
            return self._indexSize
        count = 0
        while True:
            self.skipSpecies()
            count += 1
            if self.isEnd():
                return count


    def readInitialization(self):
        '''
        corresponding to VisualizationLogProcess::initializeLog()
        '''
        self.readHeader()
        self.readLatticeSpecies()
        self.readPolymerSpecies()
        self.readOffLatticeSpecies()


    def readHeader(self):
        data = {}
        data['aLatticeType'] = struct.unpack('<I', self.logfile.read(4))[0]
        data['theMeanCount'] = struct.unpack('I', self.logfile.read(4))[0]
        data['aStartCoord'] = struct.unpack('I', self.logfile.read(4))[0]

        data['aRowSize'] = struct.unpack('I', self.logfile.read(4))[0]
        data['aLayerSize'] = struct.unpack('I', self.logfile.read(4))[0]
        data['aColSize'] = struct.unpack('I', self.logfile.read(4))[0]

        data['aRealRowSize'] = struct.unpack('d', self.logfile.read(8))[0]
        data['aRealLayerSize'] = struct.unpack('d', self.logfile.read(8))[0]
        data['aRealColSize'] = struct.unpack('d', self.logfile.read(8))[0]

        data['theLatticeSpSize'] = struct.unpack('I', self.logfile.read(4))[0]
        data['thePolymerSize'] = struct.unpack('I', self.logfile.read(4))[0]
        data['aResersvedSize'] = struct.unpack('I', self.logfile.read(4))[0]
        data['theOffLatticeSpSize'] = struct.unpack('I', self.logfile.read(4))[0]
        data['theLogMarker'] = struct.unpack('I', self.logfile.read(4))[0]
        data['aVoxelRadius'] = struct.unpack('d', self.logfile.read(8))[0]
        self.header = data

    def getHeader(self):
        return self.header


    def readLatticeSpecies(self):
        species = []

        for i in range(self.header['theLatticeSpSize']):
            aStringSize = struct.unpack('I', self.logfile.read(4))[0]
            aString = struct.unpack(str(aStringSize) + 's',
                    self.logfile.read(aStringSize))[0]
            aRadius = struct.unpack('d', self.logfile.read(8))[0]
            species.append((aString, aRadius))

        self.header['latticeSpecies'] = species


    def readPolymerSpecies(self):
        species = []

        for i in range(self.header['thePolymerSize']):
            aRadius = struct.unpack('d', self.logfile.read(8))[0]
            species.append(aRadius)

        self.header['polymerSpecies'] = species


    def readOffLatticeSpecies(self):
        species = []
        for i in range(self.header['theOffLatticeSpSize']):
            aStringSize = struct.unpack('I', self.logfile.read(4))[0]
            aString = struct.unpack(str(aStringSize) + 's',
                    self.logfile.read(aStringSize))[0]
            aRadius = struct.unpack('d', self.logfile.read(8))[0]
            species.append((aString, aRadius))

        self.header['offLatticeSpecies'] = species


    def readCompVacant(self):
        '''
        corresponding to VisualizationLogProces::logCompVacant()
        '''
        data = {}
        aCurrentTime = struct.unpack('d', self.logfile.read(8))[0]

        data['Lattice'] = []
        for index in range(self.header['theLatticeSpSize']+1):
            i = struct.unpack('I', self.logfile.read(4))[0]
            if i == self.header['theLogMarker']:
                break
            lattices = {}
            lattices['index'] = i
            lattices['Coords'] = []
            aSize = struct.unpack('i', self.logfile.read(4))[0]
            for j in range(aSize):
                aCoord = struct.unpack('I', self.logfile.read(4))
                lattices['Coords'].append(aCoord)
            data['Lattice'].append(lattices)

        data['OffLattice'] = []
        for index in range(self.header['theOffLatticeSpSize']+1):
            i = struct.unpack('I', self.logfile.read(4))[0]
            if i == self.header['theLogMarker']:
                break
            offlattices = {}
            offlattices['index'] = i
            offlattices['Points'] = []
            aSize = struct.unpack('i', self.logfile.read(4))[0]
            for j in range(aSize):
                (x, y, z) = struct.unpack('ddd', self.logfile.read(8*3))
                offlattices['Points'].append((x, y, z))
            data['OffLattice'].append(offlattices)

        self.header['compVacant'] = data


    def readSpecies(self):
        '''
        corresponding to VisualizationLogProcess::logSpecies()
        '''
        data = {}

        aCurrentTime = struct.unpack('d', self.logfile.read(8))[0]
        data['theCurrentTime'] = aCurrentTime

        data['Lattice'] = []
        for i in range(self.header['theLatticeSpSize']):
            molecules = self.readMolecules()
            data['Lattice'].append(molecules)

        data['SourceMolecules'] = []
        for i in range(self.header['thePolymerSize']):
            molecules = self.readSourceMolecules()
            data['SourceMolecules'].append(molecules)

        data['TargetMolecules'] = []
        for i in range(self.header['thePolymerSize']):
            molecules = self.readTargetMolecules()
            data['TargetMolecules'].append(molecules)

        data['SharedMolecules'] = []
        for i in range(self.header['thePolymerSize']):
            molecule = self.readSharedMolecules()
            data['SharedMolecules'].append(molecule)

        theLogMarker0 = struct.unpack('I', self.logfile.read(4))[0]
        if theLogMarker0 != self.header['theLogMarker']:
            raise SpatiocyteLogReadingException('[ERROR]\tthe log marker is different!')

        data['Polymers'] = []
        for i in range(self.header['thePolymerSize']):
            polymer = self.readPolymers()
            data['Polymers'].append(polymer)

        data['OffLattice'] = []
        for i in range(self.header['theOffLatticeSpSize'] + 1):
            read = self.logfile.read(4)
            check = struct.unpack('I', read)[0]
            if check == self.header['theLogMarker']:
                break
            anIndex = struct.unpack('i', read)[0]
            offLattice = {'index':anIndex, 'Points':self.readOffLattice()}
            data['OffLattice'].append(offLattice)

        index = 0
        max_index = self.getIndexSize()
        col_size = self.header['aColSize']
        row_size = self.header['aRowSize']
        layer_size = self.header['aLayerSize']
        lattice_species = self.header['latticeSpecies']
        offlattice_species = self.header['offLatticeSpecies']
        voxel_radius = self.header['aVoxelRadius']
        ps = LatticeParticleSpace(index, max_index, col_size, row_size, layer_size,
                voxel_radius, lattice_species, offlattice_species)

        for sp in self.header['compVacant']['Lattice']:
            sid = sp['index']
            for coord in sp['Coords']:
                ps.add_particle(LatticeParticle(sid, coord))
        for sp in self.header['compVacant']['OffLattice']:
            sid = sp['index']
            for point in sp['Points']:
                ps.add_particle(OffLatticeParticle(sid, point))

        for sp in data['Lattice']:
            sid = sp['index']
            for coord in sp['Coords']:
                ps.add_particle(LatticeParticle(sid, coord))
        for sp in data['OffLattice']:
            sid = sp['index']
            for point in sp['Points']:
                ps.add_particle(OffLatticeParticle(sid, point))

        ps.setTime(data['theCurrentTime'])
        col = self.header['aRealColSize'] * 2 * ps.voxel_radius
        layer = self.header['aRealLayerSize'] * 2 * ps.voxel_radius
        row = self.header['aRealRowSize'] * 2 * ps.voxel_radius
        ps.static_bounds = [0.0, col, 0.0, layer, 0.0, row]

        return ps


    def skipSpecies(self):

        self.logfile.seek(8,1)

        for i in range(self.header['theLatticeSpSize']):
            self.skipMolecules()

        for i in range(self.header['thePolymerSize']):
            self.skipSourceMolecules()

        for i in range(self.header['thePolymerSize']):
            self.skipTargetMolecules()

        for i in range(self.header['thePolymerSize']):
            self.skipSharedMolecules()

        theLogMarker0 = struct.unpack('I', self.logfile.read(4))[0]
        if theLogMarker0 != self.header['theLogMarker']:
            raise SpatiocyteLogReadingException('[ERROR]\tthe log marker is different!')
            sys.exit()

        for i in range(self.header['thePolymerSize']):
            self.skipPolymers()

        for i in range(self.header['theOffLatticeSpSize'] + 1):
            check = struct.unpack('I', self.logfile.read(4))[0]
            if check == self.header['theLogMarker']:
                break
            self.skipOffLattice()


    def skipSpeciesTo(self, index):
        currentSeek = self.tell()
        self.logfile.seek(self.headerSeek)

        for i in range(index):
            self.skipSpecies()
            if self.isEnd():
                self.logfile.seek(currentSeek)
                raise SpatiocyteLogReadingException('[ERROR]\t'+index+' is out of bound')

        ps = self.readSpecies()
        ps.__index = index;
        return ps

    def readMolecules(self):
        '''
        read aSpecies->getCoord(i) i(0:aSpecies->size())
        '''
        molecules = {}
        (index, size) = struct.unpack('ii', self.logfile.read(8))
        molecules['index'] = index
        molecules['Coords'] = []
        for i in range(size):
            aCoord = struct.unpack('I', self.logfile.read(4))[0]
            molecules['Coords'].append(aCoord)
        return molecules


    def skipMolecules(self):
        self.logfile.seek(4,1)
        size = struct.unpack('i', self.logfile.read(4))[0]
        self.logfile.seek(4*size,1)


    def readSourceMolecules(self):
        '''
        read aSpecies->getSourceCoords()
        '''
        data = {}
        (aSourceIndex, aSize) = struct.unpack('ii', self.logfile.read(8))
        data['index'] = aSourceIndex
        data['Coords'] = []
        for i in range(aSize):
            aCoord = struct.unpack('I', self.logfile.read(4))[0]
            data['Coords'].append(aCoord)
        return data


    def skipSourceMolecules(self):
        self.logfile.seek(4,1)
        size = struct.unpack('i', self.logfile.read(4))[0]
        self.logfile.seek(4*size,1)


    def readTargetMolecules(self):
        '''
        read aSpecies->getTargetCoords()
        '''
        data = {}
        (aTargetIndex, aSize) = struct.unpack('ii', self.logfile.read(8))
        data['index'] = aTargetIndex
        data['Coords'] = []
        for i in range(aSize):
            aCoord = struct.unpack('I', self.logfile.read(4))[0]
            data['Coords'].append(aCoord)
        return data


    def readTargetMolecules(self):
        self.logfile.seek(4,1)
        size = struct.unpack('i', self.logfile.read(4))[0]
        self.logfile.seek(4*size,1)


    def readSharedMolecules(self):
        '''
        read aSpecies->getSharedCoords()
        '''
        data = {}
        (aSharedIndex, aSize) = struct.unpack('ii', self.logfile.read(8))
        data['index'] = aSharedIndex
        data['Coords'] = []
        for i in range(aSize):
            aCoord = struct.unpack('I', self.logfile.read(4))[0]
            data['Coords'].append(aCoord)
        return data

    def skipSharedMolecules(self):
        self.logfile.seek(4,1)
        size = struct.unpack('i', self.logfile.read(4))[0]
        self.logfile.seek(4*size,1)


    def readPolymers(self):
        '''
        read aSpecies->getPoint(i) i(0:aSpecies->size())
        '''
        data = {}
        (anIndex, aSize) = struct.unpack('ii', self.logfile.read(8))
        data['index'] = anIndex
        data['Points'] = []
        for i in range(aSize):
            (x, y, z) = struct.unpack('ddd', self.logfile.read(8*3))
            data['Points'].append({'x':x, 'y':y, 'z':z})
        return data

    def skipPolymers(self):
        self.logfile.seek(4,1)
        size = struct.unpack('i', self.logfile.read(4))[0]
        self.logfile.seek(24*size,1)


    def readOffLattice(self):
        '''
        read aSpecies->getPoint(i)
        or  aSpecies->getMultiscaleStructurePoint(i) i(0:aSpecies->size())
        '''
        points=[]
        aSize = struct.unpack('i', self.logfile.read(4))[0]
        for i in range(aSize):
            (x, y, z) = struct.unpack('ddd', self.logfile.read(8*3))
            points.append((x, y, z))
        return points

    def skipOffLattice(self):
        size = struct.unpack('i', self.logfile.read(4))[0]
        self.logfile.seek(8*3*size, 1)

def load_particles_from_spatiocyte(filename, index=0, ps=None):
    if not os.path.isfile(filename):
        return ps

    reader = None
    try:
        reader = SpatiocyteLogReader(filename)
        ps  = reader.skipSpeciesTo(index)
    except SpatiocyteLogReadingException, e:
        print e
    finally:
        if reader is not None:
            reader.close()
    return ps

class ParticleSpatiocyteLoaderProgressDialog(wx.ProgressDialog):

    def __init__(self, filenames):
        wx.ProgressDialog.__init__(
            self, "Loading ...",
            "File remaining", len(filenames),
            style=wx.PD_ELAPSED_TIME | wx.PD_REMAINING_TIME | wx.PD_AUTO_HIDE)

        self.filenames = filenames
        self.index = 0

    def Show(self):
        for i, filename in enumerate(self.filenames):
            ps = load_particles_from_spatiocyte(filename, self.index)
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
        self._index = -1
        PipelineNode.__init__(self, *args, **kwargs)

    @log_call
    def internal_update(self):
        """Reset cached spatiocyte data.
        """
        self._particle_space = None

    def load_spatiocyte_file(self, fullpath, index):
        rexp = re.compile('(.+)\.dat$')
        mobj = rexp.match(fullpath)
        if mobj is None:
            raise IOError, 'No suitable file.'

        filenames = glob.glob(fullpath)
        if len(filenames) > 1:
            dialog = ParticleSpatiocyteLoaderProgressDialog(filenames)
            dialog.index = index
            ps = dialog.Show()
            dialog.Destroy()
        elif len(filenames) == 1:
            ps = load_particles_from_spatiocyte(filenames[0],index)
        else:
            ps = None
        return ps

    def fetch_particle_space(self, **kwargs):
        """Property getter for particle_space
        """
        # examine cache
        uri = self.parent.request_data(UriSpec, **kwargs)

        if 'index' in kwargs:
            index = kwargs['index']
        else:
            index = 0

        if not (self._uri == uri and self._index == index):
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
                self._particle_space = self.load_spatiocyte_file(fullpath, index)
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
            ps = self.fetch_particle_space(**kwargs)
            if ps is None:
                return 0
            else:
                return ps.getNumberOfItems()
        elif spec == ParticleSpaceSpec:
            debug('Serving ParticleSpaceSpec')
            # this may be None if datasource is not valid.
            ps = self.fetch_particle_space(**kwargs)
            return ps
        return None


register_pipeline_node(ParticleSpatiocyteLoaderNode)


if __name__=='__main__':
    # TBD
    from doctest import testmod, ELLIPSIS
    testmod(optionflags = ELLIPSIS)
