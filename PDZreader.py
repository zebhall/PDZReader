# PDZreader by zh
versionNum = 'v0.0.1'
versionDate = '2023/08/09'


import struct
import matplotlib.pyplot as plt

class XRFSpectrum:
    def __init__(self):
        self.name = ''
        self.counts = []
        self.energies = []
        self.energyPerChannel = 20      # in eV
        self.energyChannelStart = 0     # in eV
        self.numberOfChannels = 0
        self.sourceVoltage = 0.0        # in kV
        self.sourceCurrent = 0.0        # in uA
        # filters
        self.filterLayer1Element = 0    # Z num
        self.filterLayer1Thickness = 0  # in um
        self.filterLayer2Element = 0    # Z num
        self.filterLayer2Thickness = 0  # in um
        self.filterLayer3Element = 0    # Z num
        self.filterLayer3Thickness = 0  # in um
        self.filterNumber = 0
        
        self.detectorTempInC = 0.0
        self.ambientTempInF = 0.0

    def isValid(self):
        if self.counts == []:
            return False
        else:
            return True
        
    def generateEnergies(self):
        self.energies = list((i*self.energyPerChannel+self.energyChannelStart) for i in range(0,self.numberOfChannels))
        print(f'Spectrum energies list created for {self.name}')
        return self.energies

    def printCounts(self):
        print(self.counts)
    
    def printParameters(self):
        print(f'Source Voltage: {self.sourceVoltage}')
        print(f'Source Current: {self.sourceVoltage}')

def readByte(pdzfile):
    return struct.unpack("B",pdzfile.read(1))[0]

def readShort(pdzfile):
    return struct.unpack("<h",pdzfile.read(2))[0]

def readUShort(pdzfile):
    return struct.unpack("<H",pdzfile.read(2))[0]

def readInt(pdzfile):
    return struct.unpack("<i",pdzfile.read(4))[0]

def readUInt(pdzfile):
    return struct.unpack("<I",pdzfile.read(4))[0]

def read32bitFloat(pdzfile):
    return struct.unpack("<f",pdzfile.read(4))[0]

def readString(pdzfile):
    length = readInt(pdzfile)
    print(f"(string of length {str(length)})")
    return pdzfile.read(length*2).decode("utf16")

def readSpectrumParameters(pdzfile,spectrum):
    print("spectrum parameters:")
    print(readInt(pdzfile))
    print(read32bitFloat(pdzfile))
    print('counts raw total: ' + str(readInt(pdzfile)))
    print('counts valid total: '+ str(readInt(pdzfile)))
    print(read32bitFloat(pdzfile))
    print(read32bitFloat(pdzfile))
    
    total_time = read32bitFloat(pdzfile)
    print("total time: "+ str(total_time))
    print("live xxtime: "+str(read32bitFloat(pdzfile)))
    print(str(read32bitFloat(pdzfile)))
    print(read32bitFloat(pdzfile))
    print(read32bitFloat(pdzfile))

    spectrum.sourceVoltage = read32bitFloat(pdzfile)
    print("tube voltage: "+str(spectrum.sourceVoltage))
    spectrum.sourceCurrent = read32bitFloat(pdzfile)
    print("tube current: "+str(spectrum.sourceCurrent))

    spectrum.filterLayer1Element = readShort(pdzfile)
    spectrum.filterLayer1Thickness = readShort(pdzfile)
    spectrum.filterLayer2Element = readShort(pdzfile)
    spectrum.filterLayer2Thickness = readShort(pdzfile)
    spectrum.filterLayer3Element = readShort(pdzfile)
    spectrum.filterLayer3Thickness = readShort(pdzfile)
    spectrum.filterNumber = readShort(pdzfile)
    print(f'Filter {spectrum.filterNumber}: {spectrum.filterLayer1Element}({spectrum.filterLayer1Thickness}uM)/{spectrum.filterLayer2Element}({spectrum.filterLayer2Thickness}uM)/{spectrum.filterLayer3Element}({spectrum.filterLayer3Thickness}uM)')
    #print(read32bitFloat(pdzfile))
    #print(read32bitFloat(pdzfile))
    #print(read32bitFloat(pdzfile))
    #print(readShort(pdzfile))

    # print(read32bitFloat(pdzfile))
    # print(read32bitFloat(pdzfile))
    spectrum.detectorTempInC = read32bitFloat(pdzfile)
    spectrum.ambientTempInF = read32bitFloat(pdzfile)
    print(f'Temps: det(c): {spectrum.detectorTempInC}, amb(f): {spectrum.ambientTempInF}')
    
    print(f'vacuum(pdz): {readInt(pdzfile)}')

    spectrum.energyPerChannel = read32bitFloat(pdzfile)
    print("energy per channel (eV): "+str(spectrum.energyPerChannel))

    print(readShort(pdzfile)) # gain Control Algorithms? 0=None, 1=ClassicTurbo, 2=VassiliNextGen
    
    spectrum.energyChannelStart = read32bitFloat(pdzfile) # 4
    print(f'spec channel starts (ev): {spectrum.energyChannelStart}')
    #print("abscissa: "+str(read32bitFloat(pdzfile)))

    year = readShort(pdzfile) 
    month = readShort(pdzfile) 
    datetimedayofweek = readShort(pdzfile)
    day = readShort(pdzfile)
    hour = readShort(pdzfile)
    minute = readShort(pdzfile)
    second = readShort(pdzfile)
    millisecond = readShort(pdzfile)
    print(f'date: {year}/{month}/{day}')
    print(f'time: {hour}:{minute}:{second}')
    print(f'weird bruker thing: {datetimedayofweek}')
    print(f'nosepressure (mBar): {read32bitFloat(pdzfile)}')
    spectrum.numberOfChannels = readShort(pdzfile)
    print(f'siNumChannels: {spectrum.numberOfChannels}')
    print(f'nosetemp (C): {readShort(pdzfile)}')
    print(readShort(pdzfile))
    # print(read32bitFloat(pdzfile))
    # print(read32bitFloat(pdzfile))
    # print(read32bitFloat(pdzfile))
    # print(readShort(pdzfile)) #unnecc
    # print(read32bitFloat(pdzfile))
    # print(read32bitFloat(pdzfile))
    # print(read32bitFloat(pdzfile))
    # 26

    spectrum.name = readString(pdzfile)
    print(f"spectrum name: {spectrum.name}")
#    depending on measurement mode treat spectrum name differently    
    print(readShort(pdzfile))
    print("finished reading spectrum parameters")

def readSpectrumCounts(pdzfile,spectrum):
    for i in range(spectrum.numberOfChannels):
        spectrum.counts.append(readInt(pdzfile))
    print("finished reading counts.")

def readPDZ(pdzfile_name):
    spectrum1 = XRFSpectrum()
    spectrum2 = XRFSpectrum()
    spectrum3 = XRFSpectrum()
    pdzfile = open(pdzfile_name, "rb")

    version = readUShort(pdzfile)
    print("version: "+str(version))
    if version != 25:
        print("wrong pdz version")
        exit()
    #print(readInt(pdzfile))
    print('num1='+str(readUShort(pdzfile)))
    print('num2?='+str(readUShort(pdzfile)))

    print(pdzfile.read(10).decode("utf16"))
    print(readInt(pdzfile))     #4
    print(readShort(pdzfile))   #2
    print(readInt(pdzfile))     #4

    instrument_serial_number = readString(pdzfile)
    print(f"Instrument Serial Number: {instrument_serial_number}")

    instrument_build_number = readString(pdzfile)
    print(f"Instrument Build Number: {instrument_build_number}")

    print('anode material: ' + str(readByte(pdzfile)))
    print(pdzfile.read(5))

    detector_type = readString(pdzfile)
    print("detector type: "+ detector_type)

    print(readString(pdzfile)+": "+str(readShort(pdzfile)))
    print(readString(pdzfile))
    listLength = readInt(pdzfile)
    for i in range(listLength):
        print(str(readShort(pdzfile))+": "+readString(pdzfile))
    print(readShort(pdzfile))
    print(readInt(pdzfile))
    print(readInt(pdzfile))
    print(readInt(pdzfile))
    print(readInt(pdzfile))
    print(readInt(pdzfile))
    print(readInt(pdzfile))

    print(read32bitFloat(pdzfile))
    print(read32bitFloat(pdzfile))
    print(read32bitFloat(pdzfile))
    print(read32bitFloat(pdzfile))
    print(f'Time, live: {read32bitFloat(pdzfile)}')
    print(f'Time, total: {read32bitFloat(pdzfile)}')

    measurementMode = readString(pdzfile)
    print("Measurement mode: "+measurementMode+" "+str(readInt(pdzfile)))
    print("User: "+readString(pdzfile))
    print("some short: "+str(readShort(pdzfile)))
    readSpectrumParameters(pdzfile,spectrum1)

    # here starts the array of 2048 32 bit integers (little endian)
    readSpectrumCounts(pdzfile,spectrum1)
    # if measurementMode == "Artax":
    #     print("ready")
    #     exit()
    if readShort(pdzfile) == 3:
        print('Second Phase found.')
        readSpectrumParameters(pdzfile,spectrum2)
        readSpectrumCounts(pdzfile,spectrum2)
        # print(readShort(pdzfile))
        # print(readInt(pdzfile))
        # print(readInt(pdzfile))
        # print(readInt(pdzfile))
        # print(readInt(pdzfile))
        # print(readShort(pdzfile))

        if readShort(pdzfile) == 3:
            print('Third Phase found.')
            readSpectrumParameters(pdzfile,spectrum3)
            readSpectrumCounts(pdzfile,spectrum3)
            print(readShort(pdzfile))
            print(readInt(pdzfile))
            print(readInt(pdzfile))
            print(readInt(pdzfile))
            print(readInt(pdzfile))
            print(readShort(pdzfile))

    return spectrum1, spectrum2, spectrum3


def main():

    #pdzfile_name = 'PDZReader/00091-GeoExploration.pdz'
    pdzfile_name = 'PDZReader/00002-Spectrometer Mode.pdz'

    #plot stuff
    plt.figure(figsize=(16, 8)).set_tight_layout(True)  # Adjust the figure size as needed
    plt.xlabel('Energy (eV)')
    plt.ylabel('Counts')
    plt.title('Spectra')
    plt.legend(['Phase 1', 'Phase 2', 'Phase 3'])  # Customize the legend labels as needed
    #plt.grid(True, which='both', axis='both')

    phase1, phase2, phase3 = readPDZ(pdzfile_name)

    if phase1.isValid():
        print('phase 1 valid!')
        phase1.generateEnergies()
        plt.plot(phase1.energies, phase1.counts)
        plt.legend([phase1.name])
        if phase2.isValid():
            print('phase 2 valid!')
            phase2.generateEnergies()
            plt.plot(phase2.energies, phase2.counts)
            plt.legend([phase1.name, phase2.name])
            if phase3.isValid():
                print('phase 3 valid!')
                phase3.generateEnergies()
                plt.plot(phase3.energies, phase3.counts)
                plt.legend([phase1.name, phase2.name, phase3.name])
    
    plt.xlabel('Energy (eV)')
    plt.ylabel('Counts')
    plt.title(pdzfile_name)
    plt.grid(True, which='both', axis='both')
    #plt.minorticks_on()
    plt.rcParams['path.simplify'] = False
    plt.style.use("seaborn-v0_8-whitegrid")
    plt.show()


if __name__ == '__main__':
    main()