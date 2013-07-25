#!/usr/bin/env python
# coding: utf-8
import os
import sys
sys.path.insert(0, '../')

from spatiocyte_tools import SpatiocyteLogReader

def main():
    '''
    main function
    '''
    if (len(sys.argv) != 2):
        print "USAGE: python %s filename" % sys.argv[0]
        return

    name = sys.argv[1]
    if (not os.path.exists(name)):
        print "%s does not exist!" % name
        return

    reader = SpatiocyteLogReader(name)

    header = reader.header
    print '[header]\t',header

    count = 0
    while not reader.isEnd() :
        species = reader.readSpecies()
        num_of_lattices = len(species['Molecules'])
        num_of_offlattices = len(species['OffLattice'])
        print "count : %d, tell : %d, num of lattices : %d, num of offlattices : %d" % (count, reader.tell(), num_of_lattices, num_of_offlattices)
        count += 1

    index = count - 1
    print "LastSeek : %d, FooterSeek : %d" % (reader.tell(), reader.footerSeek)
    print "Index : %d" % index
    species = reader.skipSpeciesTo(index)
    for spiece in species['Molecules']:
        print spiece

    reader.close()

if __name__ == "__main__":
    main()
