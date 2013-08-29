# coding: utf-8
"""ec4vis.plugins.particle_space --- Draft implementation of ParticleSpace.
"""

import numpy
try:
    import ec4vis
except ImportError:
    import sys, os
    p = os.path.abspath(__file__); sys.path.insert(0, p[: p.rindex(os.sep + 'ec4vis')])

from ec4vis.plugins.spatiocyte_tools import coord2point
from ec4vis.plugins.particle_space import Particle

class LatticeParticle(object):

    def __init__(self, sid, coord):
        self.sid = sid
        self.coord = coord

class OffLatticeParticle(object):

    def __init__(self, sid, point):
        self.sid = sid
        self.point = point

class LatticeParticleSpace(object):

    def __init__(self, index, max_index, col_size, row_size, layer_size, voxel_radius,
            lattice_species, offlattice_species):
        self.__index = index
        self.__max_index = max_index
        self.__time = 0
        self.__lattice_pool = {}
        self.__offlattice_pool = {}
        self.__row_size = row_size
        self.__layer_size = layer_size
        self.__voxel_radius = voxel_radius
        #self.__species = []
        #self.__species.extend(lattice_species)
        #self.__species.extend(offlattice_species)
        self.__lattice_species = lattice_species
        self.__offlattice_species = offlattice_species

        self.static_bounds = None

    def getIndex(self):
        return self.__index

    def getNumberOfItems(self):
        return self.__max_index

    def setTime(self, time):
        self.__time = time

    def getTime(self):
        return self.__time

    @property
    def voxel_radius(self):
        return self.__voxel_radius

    @property
    def species(self):
        species = []
        if self.__lattice_pool is not None:
            for sid in self.__lattice_pool.keys():
                (string, radius) = self.__lattice_species[sid]
                species.append(string)
        if self.__offlattice_pool is not None:
            for sid in self.__offlattice_pool.keys():
                (string, radius) = self.__offlattice_species[sid]
                species.append(string)
        return species

    def add_particle(self, particle):
        if isinstance(particle, LatticeParticle):
            self.__add_particle_on_lattice(particle)
        elif isinstance(particle, OffLatticeParticle):
            self.__add_particle_off_lattice(particle)

    def __add_particle_on_lattice(self, lattice):
        sid = lattice.sid
        if sid not in self.__lattice_pool.keys():
            self.__lattice_pool[sid] = []
        self.__lattice_pool[sid].append(lattice)

    def __add_particle_off_lattice(self, offlattice):
        sid = offlattice.sid
        if sid not in self.__offlattice_pool.keys():
            self.__offlattice_pool[sid] = []
        self.__offlattice_pool[sid].append(offlattice)

    def __lattice2particle(self, lattice):
        pos = coord2point(lattice.coord, self.__row_size, self.__layer_size)
        pos = numpy.array(pos) * 2 * self.__voxel_radius
        (string, radius) = self.__lattice_species[lattice.sid]
        return Particle(string, pos, radius)

    def __offlattice2particle(self, offlattice):
        #pos = list(offlattice.point)
        pos = offlattice.point
        pos = numpy.array(pos) * 2 * self.__voxel_radius
        (string, radius) = self.__offlattice_species[offlattice.sid]
        return Particle(string, pos, radius)

    def __translate2particles(self, particles):
        result = []
        pid = 0
        for p in particles:
            if isinstance(p, LatticeParticle):
                result.append((pid,self.__lattice2particle(p)))
            elif isinstance(p, OffLatticeParticle):
                result.append((pid,self.__offlattice2particle(p)))
        return result

    def __string2key_of_lattice(self, string):
        for key in range(len(self.__lattice_species)):
            #for key in self.__lattice_pool.keys():
            (s, r) = self.__lattice_species[key]
            if (string is s):
                return key
        return None

    def __string2key_of_offlattice(self, string):
        for key in range(len(self.__offlattice_species)):
            #for key in self.__offlattice_pool.keys():
            (s, r) = self.__offlattice_species[key]
            if (string is s):
                return key
        return None

    def list_particles(self, sid=None):
        retval = []
        retval.extend(self.list_lattice(sid))
        retval.extend(self.list_offlattice(sid))

        for particle in retval:
            p = particle[1]

        return retval

    def list_lattice(self, sid=None):
        if sid is None:
            retval = []
            for lattices in self.__lattice_pool.values():
                retval.extend(self.__translate2particles(lattices))
            return retval
        else:
            sid = self.__string2key_of_lattice(sid)
            if sid is None:
                return []
            return self.__translate2particles(self.__lattice_pool[sid])

    def list_offlattice(self, sid=None):
        if sid is None:
            retval = []
            for offlattices in self.__offlattice_pool.values():
                retval.extend(self.__translate2particles(offlattices))
            return retval
        else:
            sid = self.__string2key_of_offlattice(sid)
            if sid is None:
                return []
            return self.__translate2particles(self.__offlattice_pool[sid])

    def num_particles(self, sid=None):
        num = 0
        num += self.num_lattices(sid)
        num += self.num_offlattices(sid)
        return num

    def num_lattices(self, sid=None):
        if sid is None:
            counts = [len(lattices) for lattices in self.__lattice_pool.values()]
            return sum(counts)
        else:
            sid = self.__string2key_of_lattice(sid)
            if sid is None:
                return 0
            return len(self.__lattice_pool[sid])

    def num_offlattices(self, sid=None):
        if sid is None:
            counts = [len(offlattices) for offlattices in self.__offlattice_pool.values()]
            return sum(counts)
        else:
            sid = self.__string2key_of_offlattice(sid)
            if sid is None:
                return 0
            return len(self.__offlattice_pool[sid])

# end of LatticeParticleSpace
