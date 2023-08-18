# PDZreader by zh
versionNum = 'v0.1.2'
versionDate = '2023/08/18'


import struct
from datetime import datetime as dt
import matplotlib.pyplot as plt
import os
import sys
from tkinter import filedialog


class PDZFile:
    """A collection of 1-3 XRFSpectrum objects makes up a single PDZFile object, depending on the number of phases/beams in the assay. Create by providing pdz_file_path (os.path or str)"""
    def __init__(self, pdz_file_path:str):
        self.name = os.path.basename(pdz_file_path)
        self.readPDZFileData(pdz_file_path)
        self.datetime = self.spectrum1.datetime     # pdz as a whole should use first phase datetime?

    def readPDZFileData(self, pdz_file_path:str):
        def readByte(reader):
            return struct.unpack("B",reader.read(1))[0]
        def readShort(reader):
            return struct.unpack("<h",reader.read(2))[0]
        def readUShort(reader):
            return struct.unpack("<H",reader.read(2))[0]
        def readInt(reader):
            return struct.unpack("<i",reader.read(4))[0]
        def readUInt(reader):
            return struct.unpack("<I",reader.read(4))[0]
        def read32bitFloat(reader): # 32-bit float = 'single' in c#
            return struct.unpack("<f",reader.read(4))[0]
        def readString(reader):
            length = readInt(reader)
            print(f"(string of length {str(length)})")
            return reader.read(length*2).decode("utf16")
        def readSpectrumParameters(reader,spectrum):
            print("spectrum parameters:")
            print(readInt(reader))
            print(read32bitFloat(reader))
            print('counts raw total: ' + str(readInt(reader)))
            print('counts valid total: '+ str(readInt(reader)))
            print(read32bitFloat(reader))
            print(read32bitFloat(reader))
            
            total_time = read32bitFloat(reader)
            print("total time: "+ str(total_time))
            print("(NOT really)live time: "+str(read32bitFloat(reader)))
            print(str(read32bitFloat(reader)))
            print(read32bitFloat(reader))
            print(read32bitFloat(reader))

            spectrum.sourceVoltage = read32bitFloat(reader)
            print("tube voltage: "+str(spectrum.sourceVoltage))
            spectrum.sourceCurrent = read32bitFloat(reader)
            print("tube current: "+str(spectrum.sourceCurrent))

            spectrum.filterLayer1ElementZ = readShort(reader)
            spectrum.filterLayer1Thickness = readShort(reader)
            spectrum.filterLayer2ElementZ = readShort(reader)
            spectrum.filterLayer2Thickness = readShort(reader)
            spectrum.filterLayer3ElementZ = readShort(reader)
            spectrum.filterLayer3Thickness = readShort(reader)
            spectrum.filterNumber = readShort(reader)
            spectrum.filterLayer1ElementSymbol = elementZtoSymbol(spectrum.filterLayer1ElementZ)
            spectrum.filterLayer2ElementSymbol = elementZtoSymbol(spectrum.filterLayer2ElementZ)
            spectrum.filterLayer3ElementSymbol = elementZtoSymbol(spectrum.filterLayer3ElementZ)
            spectrum.filterDesciption = f'{spectrum.filterLayer1ElementSymbol}({spectrum.filterLayer1Thickness}uM)/{spectrum.filterLayer2ElementSymbol}({spectrum.filterLayer2Thickness}uM)/{spectrum.filterLayer3ElementSymbol}({spectrum.filterLayer3Thickness}uM)'.replace('/(0uM)','').replace('(0uM)','No Filter')

            print(f'Filter: {spectrum.filterDesciption}')
            spectrum.detectorTempInC = read32bitFloat(reader)
            spectrum.ambientTempInF = read32bitFloat(reader)
            spectrum.ambientTempInC = (spectrum.ambientTempInF - 32)/1.8    #convert to C
            print(f'Temps (Celsius): Detector: {spectrum.detectorTempInC:.2f}, Ambient: {spectrum.ambientTempInC:.2f}')
            
            print(f'vacuum(pdz): {readInt(reader)}')    # unsure how to properly read this value

            spectrum.energyPerChannel = read32bitFloat(reader)
            print("energy per channel (eV): "+str(spectrum.energyPerChannel))

            print(readShort(reader)) # gain Control Algorithms? 0=None, 1=ClassicTurbo, 2=VassiliNextGen
            
            spectrum.energyChannelStart = read32bitFloat(reader) # 4
            print(f'Spectrum channel starts at (ev): {spectrum.energyChannelStart}') # effectively abscissa

            spectrum_year = readShort(reader) 
            spectrum_month = readShort(reader) 
            spectrum_datetimedayofweek = readShort(reader)
            spectrum_day = readShort(reader)
            spectrum_hour = readShort(reader)
            spectrum_minute = readShort(reader)
            spectrum_second = readShort(reader)
            spectrum_millisecond = readShort(reader)
            spectrum.datetime = dt(spectrum_year,spectrum_month,spectrum_day,spectrum_hour,spectrum_minute,spectrum_second)
            print(f'Date/Time: {spectrum.datetime}')
            
            spectrum.nosePressure = read32bitFloat(reader)
            print(f'nosepressure (mBar): {spectrum.nosePressure}')
            spectrum.numberOfChannels = readShort(reader)
            print(f'siNumChannels: {spectrum.numberOfChannels}')
            spectrum.noseTempInC = readShort(reader)
            print(f'Nose Temperature (C): {spectrum.noseTempInC:.2f}')
            print(readShort(reader))

            spectrum.name = readString(reader)
            print(f"spectrum name: {spectrum.name}")
            # depending on measurement mode treat spectrum name differently    
            print(readShort(reader))
            print("finished reading spectrum parameters")
        def readSpectrumCounts(reader,spectrum):
            for i in range(spectrum.numberOfChannels):
                spectrum.counts.append(readInt(reader))
            print("finished reading counts.")
        
        # create pdz file reader object
        with open(pdz_file_path, "rb") as self.pdzfilereader:

            # read general pdz file data!
            # read pdz file version
            self.pdzfileversion = readUShort(self.pdzfilereader)
            print("version: "+str(self.pdzfileversion))
            if self.pdzfileversion != 25:
                print("ERROR: wrong pdz version")
            print('num1='+str(readUShort(self.pdzfilereader)))
            print('num2?='+str(readUShort(self.pdzfilereader)))
            print(self.pdzfilereader.read(10).decode("utf16"))
            print(readInt(self.pdzfilereader))     #4
            print(readShort(self.pdzfilereader))   #2
            print(readInt(self.pdzfilereader))     #4

            self.instrumentSerialNumber = readString(self.pdzfilereader)
            print(f"Instrument Serial Number: {self.instrumentSerialNumber}")

            self.instrumentBuildNumber = readString(self.pdzfilereader)
            print(f"Instrument Build Number: {self.instrumentBuildNumber}")

            self.anodeElementZ = int(readByte(self.pdzfilereader))
            self.anodeElementSymbol = elementZtoSymbol(self.anodeElementZ)
            self.anodeElementName = elementZtoName(self.anodeElementZ)
            print(f'Anode: {self.anodeElementName}')

            print(self.pdzfilereader.read(5))  # this comes out as b'--A}\x00' ?

            self.detectorType = readString(self.pdzfilereader)
            print("detector type: "+ self.detectorType)

            print(readString(self.pdzfilereader)+": "+str(readShort(self.pdzfilereader)))
            print(readString(self.pdzfilereader))
            listLength = readInt(self.pdzfilereader)
            for i in range(listLength):
                print(str(readShort(self.pdzfilereader))+": "+readString(self.pdzfilereader))
            print(readShort(self.pdzfilereader))
            print(readInt(self.pdzfilereader))
            print(readInt(self.pdzfilereader))
            print(readInt(self.pdzfilereader))
            print(readInt(self.pdzfilereader))
            print(readInt(self.pdzfilereader))
            print(readInt(self.pdzfilereader))

            print(read32bitFloat(self.pdzfilereader))
            print(read32bitFloat(self.pdzfilereader))
            print(read32bitFloat(self.pdzfilereader))
            print(read32bitFloat(self.pdzfilereader))
            print(f'Time, live: {read32bitFloat(self.pdzfilereader)}')
            print(f'Time, total: {read32bitFloat(self.pdzfilereader)}')

            measurementMode = readString(self.pdzfilereader)
            print("Measurement mode: "+measurementMode+" "+str(readInt(self.pdzfilereader)))
            print("User: "+readString(self.pdzfilereader))
            print("some short: "+str(readShort(self.pdzfilereader)))

            # CREATE SPECTRUM 1
            self.spectrum1 = XRFSpectrum()
            readSpectrumParameters(self.pdzfilereader,self.spectrum1)
            readSpectrumCounts(self.pdzfilereader,self.spectrum1)
            self.phasecount = 1

            if readShort(self.pdzfilereader) == 3:
                print('Second Phase found.')
                self.phasecount += 1
                self.spectrum2 = XRFSpectrum()
                readSpectrumParameters(self.pdzfilereader,self.spectrum2)
                readSpectrumCounts(self.pdzfilereader,self.spectrum2)
                # print(readShort(pdzfile))
                # print(readInt(pdzfile))
                # print(readInt(pdzfile))
                # print(readInt(pdzfile))
                # print(readInt(pdzfile))
                # print(readShort(pdzfile))
                if readShort(self.pdzfilereader) == 3:
                    print('Third Phase found.')
                    self.phasecount += 1
                    self.spectrum3 = XRFSpectrum()
                    readSpectrumParameters(self.pdzfilereader,self.spectrum3)
                    readSpectrumCounts(self.pdzfilereader,self.spectrum3)
                    # print(readShort(self.pdzfilereader))
                    # print(readInt(self.pdzfilereader))
                    # print(readInt(self.pdzfilereader))
                    # print(readInt(self.pdzfilereader))
                    # print(readInt(self.pdzfilereader))
                    # print(readShort(self.pdzfilereader))


    def __repr__(self) -> str:
        return f'{self.name} / {self.phasecount} phases / {self.datetime} / {self.instrumentSerialNumber}'
        pass

class XRFSpectrum:
    """Class to represent and contain data from a single 'phase' of a PDZ file."""
    def __init__(self):
        self.name = ''
        self.datetime = dt(1970,1,1,0,0,0)  # using unix timestamp 0-time as default.
        self.counts = []
        self.energies = []
        self.energyPerChannel = 20      # in eV
        self.energyChannelStart = 0     # in eV
        self.numberOfChannels = 0
        self.sourceVoltage = 0.0        # in kV
        self.sourceCurrent = 0.0        # in uA
        # filters
        self.filterLayer1ElementZ = 0    # Z num
        self.filterLayer1Thickness = 0  # in um
        self.filterLayer2ElementZ = 0    # Z num
        self.filterLayer2Thickness = 0  # in um
        self.filterLayer3ElementZ = 0    # Z num
        self.filterLayer3Thickness = 0  # in um
        self.filterNumber = 0
        
        # temp / pressure
        self.detectorTempInC = 0.0
        self.ambientTempInF = 0.0
        self.noseTempInC = 0.0
        self.nosePressure = 0.0

    def __repr__(self): # used for print() of class
        return (self.name, self.datetime, self.sourceVoltage, self.sourceCurrent)

    def isNotEmpty(self):
        if self.counts == []:
            return False
        else:
            return True
        
    def generateEnergies(self):
        self.energies = list(((i*self.energyPerChannel+self.energyChannelStart)*0.001) for i in range(0,self.numberOfChannels))
        print(f'Spectrum energies list created for {self.name}')
        return self.energies
    

def elementZtoSymbol(Z):        # Returns 1-2 character Element symbol as a string
    if Z == 0:
        return ''
    elif Z <= 118:
        elementSymbols = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
        return elementSymbols[Z-1]
    else:
        print('Error: Z out of range')
        return 'ERR'

def elementZtoSymbolZ(Z):       # Returns 1-2 character Element symbol formatted WITH atomic number in brackets
    if Z <= 118:
        elementSymbols = ['H (1)', 'He (2)', 'Li (3)', 'Be (4)', 'B (5)', 'C (6)', 'N (7)', 'O (8)', 'F (9)', 'Ne (10)', 'Na (11)', 'Mg (12)', 'Al (13)', 'Si (14)', 'P (15)', 'S (16)', 'Cl (17)', 'Ar (18)', 'K (19)', 'Ca (20)', 'Sc (21)', 'Ti (22)', 'V (23)', 'Cr (24)', 'Mn (25)', 'Fe (26)', 'Co (27)', 'Ni (28)', 'Cu (29)', 'Zn (30)', 'Ga (31)', 'Ge (32)', 'As (33)', 'Se (34)', 'Br (35)', 'Kr (36)', 'Rb (37)', 'Sr (38)', 'Y (39)', 'Zr (40)', 'Nb (41)', 'Mo (42)', 'Tc (43)', 'Ru (44)', 'Rh (45)', 'Pd (46)', 'Ag (47)', 'Cd (48)', 'In (49)', 'Sn (50)', 'Sb (51)', 'Te (52)', 'I (53)', 'Xe (54)', 'Cs (55)', 'Ba (56)', 'La (57)', 'Ce (58)', 'Pr (59)', 'Nd (60)', 'Pm (61)', 'Sm (62)', 'Eu (63)', 'Gd (64)', 'Tb (65)', 'Dy (66)', 'Ho (67)', 'Er (68)', 'Tm (69)', 'Yb (70)', 'Lu (71)', 'Hf (72)', 'Ta (73)', 'W (74)', 'Re (75)', 'Os (76)', 'Ir (77)', 'Pt (78)', 'Au (79)', 'Hg (80)', 'Tl (81)', 'Pb (82)', 'Bi (83)', 'Po (84)', 'At (85)', 'Rn (86)', 'Fr (87)', 'Ra (88)', 'Ac (89)', 'Th (90)', 'Pa (91)', 'U (92)', 'Np (93)', 'Pu (94)', 'Am (95)', 'Cm (96)', 'Bk (97)', 'Cf (98)', 'Es (99)', 'Fm (100)', 'Md (101)', 'No (102)', 'Lr (103)', 'Rf (104)', 'Db (105)', 'Sg (106)', 'Bh (107)', 'Hs (108)', 'Mt (109)', 'Ds (110)', 'Rg (111)', 'Cn (112)', 'Nh (113)', 'Fl (114)', 'Mc (115)', 'Lv (116)', 'Ts (117)', 'Og (118)']
        return elementSymbols[Z-1]
    else:
        print('Error: Z out of range')
        return 'ERR'

def elementZtoName(Z):          # Returns Element name 
    if Z <= 118:
        elementNames = ['Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', 'Carbon', 'Nitrogen', 'Oxygen', 'Fluorine', 'Neon', 'Sodium', 'Magnesium', 'Aluminium', 'Silicon', 'Phosphorus', 'Sulfur', 'Chlorine', 'Argon', 'Potassium', 'Calcium', 'Scandium', 'Titanium', 'Vanadium', 'Chromium', 'Manganese', 'Iron', 'Cobalt', 'Nickel', 'Copper', 'Zinc', 'Gallium', 'Germanium', 'Arsenic', 'Selenium', 'Bromine', 'Krypton', 'Rubidium', 'Strontium', 'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum', 'Technetium', 'Ruthenium', 'Rhodium', 'Palladium', 'Silver', 'Cadmium', 'Indium', 'Tin', 'Antimony', 'Tellurium', 'Iodine', 'Xenon', 'Caesium', 'Barium', 'Lanthanum', 'Cerium', 'Praseodymium', 'Neodymium', 'Promethium', 'Samarium', 'Europium', 'Gadolinium', 'Terbium', 'Dysprosium', 'Holmium', 'Erbium', 'Thulium', 'Ytterbium', 'Lutetium', 'Hafnium', 'Tantalum', 'Tungsten', 'Rhenium', 'Osmium', 'Iridium', 'Platinum', 'Gold', 'Mercury', 'Thallium', 'Lead', 'Bismuth', 'Polonium', 'Astatine', 'Radon', 'Francium', 'Radium', 'Actinium', 'Thorium', 'Protactinium', 'Uranium', 'Neptunium', 'Plutonium', 'Americium', 'Curium', 'Berkelium', 'Californium', 'Einsteinium', 'Fermium', 'Mendelevium', 'Nobelium', 'Lawrencium', 'Rutherfordium', 'Dubnium', 'Seaborgium', 'Bohrium', 'Hassium', 'Meitnerium', 'Darmstadtium', 'Roentgenium', 'Copernicium', 'Nihonium', 'Flerovium', 'Moscovium', 'Livermorium', 'Tennessine', 'Oganesson']
        return elementNames[Z-1]
    else:
        print('Error: Z out of range')
        return 'ERR'

def elementSymboltoName(sym:str):
    if len(sym) < 4:
        elementSymbols = ['H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne', 'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th', 'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og']
        elementNames = ['Hydrogen', 'Helium', 'Lithium', 'Beryllium', 'Boron', 'Carbon', 'Nitrogen', 'Oxygen', 'Fluorine', 'Neon', 'Sodium', 'Magnesium', 'Aluminium', 'Silicon', 'Phosphorus', 'Sulfur', 'Chlorine', 'Argon', 'Potassium', 'Calcium', 'Scandium', 'Titanium', 'Vanadium', 'Chromium', 'Manganese', 'Iron', 'Cobalt', 'Nickel', 'Copper', 'Zinc', 'Gallium', 'Germanium', 'Arsenic', 'Selenium', 'Bromine', 'Krypton', 'Rubidium', 'Strontium', 'Yttrium', 'Zirconium', 'Niobium', 'Molybdenum', 'Technetium', 'Ruthenium', 'Rhodium', 'Palladium', 'Silver', 'Cadmium', 'Indium', 'Tin', 'Antimony', 'Tellurium', 'Iodine', 'Xenon', 'Caesium', 'Barium', 'Lanthanum', 'Cerium', 'Praseodymium', 'Neodymium', 'Promethium', 'Samarium', 'Europium', 'Gadolinium', 'Terbium', 'Dysprosium', 'Holmium', 'Erbium', 'Thulium', 'Ytterbium', 'Lutetium', 'Hafnium', 'Tantalum', 'Tungsten', 'Rhenium', 'Osmium', 'Iridium', 'Platinum', 'Gold', 'Mercury', 'Thallium', 'Lead', 'Bismuth', 'Polonium', 'Astatine', 'Radon', 'Francium', 'Radium', 'Actinium', 'Thorium', 'Protactinium', 'Uranium', 'Neptunium', 'Plutonium', 'Americium', 'Curium', 'Berkelium', 'Californium', 'Einsteinium', 'Fermium', 'Mendelevium', 'Nobelium', 'Lawrencium', 'Rutherfordium', 'Dubnium', 'Seaborgium', 'Bohrium', 'Hassium', 'Meitnerium', 'Darmstadtium', 'Roentgenium', 'Copernicium', 'Nihonium', 'Flerovium', 'Moscovium', 'Livermorium', 'Tennessine', 'Oganesson']
        try:
            i = elementSymbols.index(sym)
            return elementNames[i]
        except:
            print('Element symbol unrecognised')
            return 'ERR'
    else:
        print('Error: Symbol too long')
        return 'ERR'

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def main():
    
    pdzpath = filedialog.askopenfilename(title="Select PDZ File to view",filetypes=[("PDZ File", "*.pdz")], initialdir = os.getcwd())
    if pdzpath == '':
        exit()
    #pdzpath = resource_path('00156-REE_IDX.pdz')
    #pdzpath = resource_path('00093-GeoExploration.pdz')
    #pdzpath = resource_path('00148-GeoExploration.pdz')
    #pdzpath = resource_path('00002-Spectrometer Mode.pdz')
    assay = PDZFile(pdzpath)



    
    

    #plot stuff
    plt.figure(figsize=(16, 8)).set_tight_layout(True)  # Adjust figure size as needed
    plt.xlabel('Energy (keV)')
    plt.ylabel('Counts')
    plt.title(f'{assay.instrumentSerialNumber} - {assay.name}')
    plt.grid(True, which='major', axis='both')
    plt.minorticks_on()
    plt.rcParams['path.simplify'] = False
    plt.style.use("seaborn-v0_8-whitegrid")

    if assay.spectrum1.isNotEmpty():
        print('phase 1 valid!')
        assay.spectrum1.generateEnergies()
        plt.plot(assay.spectrum1.energies, assay.spectrum1.counts)
        plt.legend([assay.spectrum1.name])
        if assay.spectrum2.isNotEmpty():
            print('phase 2 valid!')
            assay.spectrum2.generateEnergies()
            plt.plot(assay.spectrum2.energies, assay.spectrum2.counts)
            plt.legend([assay.spectrum1.name, assay.spectrum2.name])
            if assay.spectrum3.isNotEmpty():
                print('phase 3 valid!')
                assay.spectrum3.generateEnergies()
                plt.plot(assay.spectrum3.energies, assay.spectrum3.counts)
                plt.legend([assay.spectrum1.name, assay.spectrum2.name, assay.spectrum3.name])

    
    print(assay)
    plt.show()

if __name__ == '__main__':
    main()



