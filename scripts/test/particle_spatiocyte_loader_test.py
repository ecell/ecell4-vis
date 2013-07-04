#!/usr/bin/env python
# coding: utf-8
import sys
sys.path.insert(0, '../')

from spatiocyte_log_reader import SpatiocyteLogReader
from particle_spatiocyte_loader import load_particles_from_spatiocyte

def main():
    filename = "VisualLog.dat"
    ps = None
    ps = load_particles_from_spatiocyte(filename, 30, ps)
    plist = ps.list_particles(0)
    if plist is not None:
        print len(plist)
    plist = ps.list_particles(1)
    if plist is not None:
        print len(plist)
    plist = ps.list_particles(2)
    if plist is not None:
        print len(plist)

if __name__ == "__main__":
    main()
