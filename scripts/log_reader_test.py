#!/usr/bin/env python
# coding: utf-8

from log_reader import SpatiocyteLogReader

def main():
    '''
    main function
    '''
    name = 'VisualLog.dat'
    reader = SpatiocyteLogReader(name)

    header = reader.header
    print '[header]\t',header

    latticeSpecies = reader.latticeSpecies
    print '[latticeSpecies]\t',latticeSpecies

    polymerSpecies = reader.polymerSpecies
    print '[polymerSpecies]\t',polymerSpecies

    compVacant = reader.compVacant
    print '[compVacant]',compVacant

    while not reader.isEnd() :
        reader.skipSpecies()
        #species = reader.readSpecies()
        #print '[species]',species

    print 'CurrentSeek : ',reader.tell(),'\n'
    print 'Index : 30'
    print reader.skipSpeciesTo(30)

    reader.closeLogFile()

if __name__ == "__main__":
    main()
