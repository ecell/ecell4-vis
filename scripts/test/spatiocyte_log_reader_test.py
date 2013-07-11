#!/usr/bin/env python
# coding: utf-8
import os
import sys
sys.path.insert(0, '../')

from spatiocyte_log_reader import SpatiocyteLogReader

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
        print "count : %d, tell : %d, num of species : %d" % (count, reader.tell(), len(species))
        count += 1

    print "LastSeek : %d, FooterSeek : %d" % (reader.tell(), reader.footerSeek)
    print "Index : %d" % (count - 1)
    species = reader.skipSpeciesTo(count - 1)
    for spiece in species['Molecules']:
        print spiece

    reader.close()

if __name__ == "__main__":
    main()
