#!/usr/bin/env python
# coding: utf-8
import sys
sys.path.insert(0, '../')

from spatiocyte_log_reader import SpatiocyteLogReader

def main():
    '''
    main function
    '''
    name = 'VisualLog.dat'
    reader = SpatiocyteLogReader(name)

    header = reader.header
    print '[header]\t',header

    while not reader.isEnd() :
        reader.skipSpecies()
        #species = reader.readSpecies()
        #print '[species]',species

    print 'CurrentSeek : ',reader.tell(),'\n'
    print 'Index : 30'
    print reader.skipSpeciesTo(30)

    reader.close()

if __name__ == "__main__":
    main()
