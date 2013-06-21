# -*- encoding: utf-8 -*-
import struct

class SpatiocyteLogReader:

    def __init__(self, logfile):
        self.logfile = open(logfile, 'rb')
        self.readInitialization()
        self.readCompVacant()
        self.headerSeek = self.tell()
        self.logfile.seek(0,2)
        self.footerSeek = self.tell()
        self.logfile.seek(self.headerSeek)

    def closeLogFile(self):
        self.logfile.close()

    def tell(self):
        return self.logfile.tell()

    def isEnd(self):
        return self.tell() == self.footerSeek

    """ corresponding to VisualizationLogProcess::initializeLog()
    """
    def readInitialization(self):
        self.readHeader()
        self.readLatticeSpecies()
        self.readPolymerSpecies()


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
        """
        header_format = '<IIIIIIdddIIIIId'
        header_titles = ['aLatticeType', 'theMeanCount', 'aStartCoord',
                'aRowSize', 'aLayerSize', 'aColSize', 'aRealRowSize',
                'aRealLayerSize', 'aRealColSize', 'theLatticeSpSize',
                'thePolymerSize', 'aResersvedSize', 'theOffLatticeSpSize',
                'theLogMarker', 'aVoxelRadius']
        read = struct.unpack(header_format,f.read(4*19))
        print read
        """
        self.header = data


    def readLatticeSpecies(self):
        species = {}

        for i in range(self.header['theLatticeSpSize']):
            aStringSize = struct.unpack('I', self.logfile.read(4))[0]
            aString = struct.unpack('s' + str(aStringSize),
                    self.logfile.read(aStringSize))[0]
            aRadius = struct.unpack('d', self.logfile.read(8))[0]
            """
            print 'aStringSize + 8 = ' + str(aStringSize + 8)
            (aString, aRadius) = struct.unpack('s' + str(aStringSize) + 'd',
                    self.logfile.read(aStringSize + 8))
            """
            species[aString] = aRadius;

        self.latticeSpecies = species


    def readPolymerSpecies(self):
        species = []

        for i in range(self.header['thePolymerSize']):
            aRadius = struct.unpack('d', self.logfile.read(8))[0]
            species.append(aRadius)

        self.polymerSpecies = species


    def readOffLatticeSpecies(self):
        species = []
        for i in range(size):
            aRadius = struct.unpack('d', logfile.read(8))[0]
            species.append(aRadius)
        return species


    """ corresponding to VisualizationLogProces::logCompVacant()
    """
    def readCompVacant(self):
        data = {}
        aCurrentTime = struct.unpack('d', self.logfile.read(8))[0]
        i = 0
        data['Coords'] = {}
        for index in range(self.header['theLatticeSpSize']+1):
            i = struct.unpack('I', self.logfile.read(4))[0]
            #print 'Coords:',i,'\n'
            if i == self.header['theLogMarker']:
                break
            aSize = struct.unpack('i', self.logfile.read(4))[0]
            data['Coords'][i] = []
            for j in range(aSize):
                aCoord = struct.unpack('I', self.logfile.read(4))
                data['Coords'][i].append(aCoord)
        data['Points'] = {}
        for index in range(self.header['theOffLatticeSpSize']+1):
            i = struct.unpack('I', self.logfile.read(4))[0]
            #print 'Points:',i,'\n'
            if i == self.header['theLogMarker']:
                break
            aSize = struct.unpack('i', self.logfile.read(4))[0]
            data['Points'][i] = []
            for j in range(aSize):
                (x, y, z) = struct.unpack('ddd', self.logfile.read(8*3))
                data['Points'][i].append({'x':x, 'y':y, 'z':z})
        self.compVacant = data
        return data


    """ corresponding to VisualizationLogProcess::logSpecies()
    """
    def readSpecies(self):
        data = {}

        aCurrentTime = struct.unpack('d', self.logfile.read(8))[0]
        data['aCurrentTime'] = aCurrentTime

        data['Molecules'] = []
        for i in range(self.header['theLatticeSpSize']):
            molecules = self.readMolecules()
            data['Molecules'].append(molecules)

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
            print '[ERROR]\tthe log marker is different!'
            sys.exit()

        data['Polymers'] = []
        for i in range(self.header['thePolymerSize']):
            polymer = self.readPolymers()
            data['Polymers'].append(polymer)

        data['OffLattice'] = []
        for i in range(self.header['theOffLatticeSpSize']):
            offLattice = self.readOffLattice()
            data['OffLattice'].append(offLattice)

        theLogMarker1 = struct.unpack('I', self.logfile.read(4))[0]
        if theLogMarker1 != self.header['theLogMarker']:
            print '[ERROR]\tthe log marker is different!'
            sys.exit()

        return data


    def skipSpecies(self):

        self.logfile.seek(8,1)

        for i in range(self.header['theLatticeSpSize']):
            molecules = self.skipMolecules()

        for i in range(self.header['thePolymerSize']):
            molecules = self.skipSourceMolecules()

        for i in range(self.header['thePolymerSize']):
            molecules = self.skipTargetMolecules()

        for i in range(self.header['thePolymerSize']):
            molecule = self.skipSharedMolecules()

        theLogMarker0 = struct.unpack('I', self.logfile.read(4))[0]
        if theLogMarker0 != self.header['theLogMarker']:
            print '[ERROR]\tthe log marker is different!'
            sys.exit()

        for i in range(self.header['thePolymerSize']):
            polymer = self.skipPolymers()

        for i in range(self.header['theOffLatticeSpSize']):
            offLattice = self.skipOffLattice()

        theLogMarker1 = struct.unpack('I', self.logfile.read(4))[0]
        if theLogMarker1 != self.header['theLogMarker']:
            print '[ERROR]\tthe log marker is different!'
            sys.exit()

    def skipSpeciesTo(self, index):
        currentSeek = self.tell()
        self.logfile.seek(self.headerSeek)

        for i in range(index):
            self.skipSpecies()
            if self.isEnd():
                self.logfile.seek(currentSeek)
                print index," is out of bound."
                return

        return self.readSpecies()


    """ read aSpecies->getCoord(i) i(0:aSpecies->size())
    """
    def readMolecules(self):
        molecules = {}
        (index, size) = struct.unpack('ii', self.logfile.read(8));
        molecules['index'] = index
        molecules['aCoords'] = []
        for i in range(size):
            aCoord = struct.unpack('I', self.logfile.read(4))[0];
            molecules['aCoords'].append(aCoord);
        return molecules


    def skipMolecules(self):
        self.logfile.seek(4,1)
        size = struct.unpack('i', self.logfile.read(4))[0]
        self.logfile.seek(4*size,1)


    """ read aSpecies->getSourceCoords()
    """
    def readSourceMolecules(self):
        data = {}
        (aSourceIndex, aSize) = struct.unpack('ii', self.logfile.read(8))
        data['index'] = aSourceIndex
        data['aCoords'] = []
        for i in range(aSize):
            aCoord = struct.unpack('I', self.logfile.read(4))[0]
            data['aCoords'].append(aCoord)
        return data


    def skipSourceMolecules(self):
        self.logfile.seek(4,1)
        size = struct.unpack('i', self.logfile.read(4))[0]
        self.logfile.seek(4*size)


    """ read aSpecies->getTargetCoords()
    """
    def readTargetMolecules(self):
        data = {}
        (aTargetIndex, aSize) = struct.unpack('ii', self.logfile.read(8))
        data['index'] = aTargetIndex
        data['aCoords'] = []
        for i in range(aSize):
            aCoord = struct.unpack('I', self.logfile.read(4))[0]
            data['aCoords'].append(aCoord)
        return data


    def readTargetMolecules(self):
        self.logfile.seek(4,1)
        size = struct.unpack('i', self.logfile.read(4))[0]
        self.logfile.seek(4*size)


    """ read aSpecies->getSharedCoords()
    """
    def readSharedMolecules(self):
        data = {}
        (aSharedIndex, aSize) = struct.unpack('ii', self.logfile.read(8))
        data['index'] = aSharedIndex
        data['aCoords'] = []
        for i in range(aSize):
            aCoord = struct.unpack('I', self.logfile.read(4))[0]
            data['aCoords'].append(aCoord)
        return data

    def skipSharedMolecules(self):
        self.logfile.seek(4,1)
        size = struct.unpack('i', self.logfile.read(4))[0]
        self.logfile.seek(4*size)


    """ read aSpecies->getPoint(i) i(0:aSpecies->size())
    """
    def readPolymers(self):
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
        self.logfile.seek(24*size)


    """ read aSpecies->getPoint(i)
         or  aSpecies->getMultiscaleStructurePoint(i) i(0:aSpecies->size())
    """
    def readOffLattice(self):
        data = {}
        (anIndex, aSize) = struct.unpack('ii', self.logfile.read(8))
        data['index'] = anIndex
        data['Points'] = []
        for i in range(aSize):
            (x, y, z) = struct.unpack('ddd', self.logfile.read(8*3))
            data['Points'].append({'x':x, 'y':y, 'z':z})
        return data

    def skipOffLattice(self):
        self.logfile.seek(4,1)
        size = struct.unpack('i', self.logfile.read(4))[0]
        self.logfile.seek(24*size)


""" main function
"""
def main():
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
