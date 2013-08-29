# coding; utf-8
#
# from ecell3-spatiocyte/SpatiocyteStepper.cpp
#

from math import sqrt

HCP_LATTICE = 0
CUBIC_LATTICE = 1
NVR = 0.5# the Normalized Voxel Radius
HCPl = NVR / sqrt(2)
HCPx = NVR * sqrt(8.0/3)
HCPy = NVR * sqrt(3)

latticeType = HCP_LATTICE

def coord2point(coord, row_size, layer_size):
    """
    input : coord, row_size, layer_size
    output: a tuple (x, y, z)
    """
    (grow, glayer, gcol) = coord2global(coord, row_size, layer_size)
    if latticeType == HCP_LATTICE:
        y = (gcol % 2) * HCPl + HCPy * glayer
        z = grow * 2 * NVR + ((glayer + gcol) % 2) * NVR
        x = gcol * HCPx
    elif latticeType == CUBIC_LATTICE:
        y = glayer * 2 * NVR
        z = grow * 2 * NVR
        x = gcol * 2 * NVR
    else:
        return
    point = (x, y, z)
    return point

def coord2global(coord, row_size, layer_size):
    """
    input : coord, row_size, layer_size
    output: a tuple (grow, glayer, gcol)
    """
    gcol = coord / (row_size * layer_size)
    glayer = (coord % (row_size * layer_size)) / row_size
    grow = (coord % (row_size * layer_size)) % row_size
    point = (grow, glayer, gcol)
    return point

