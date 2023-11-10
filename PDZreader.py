# PDZreader by zh
versionNum = "v0.1.5"
versionDate = "2023/09/21"

import struct
import os
import sys
from datetime import datetime as dt
import logging as log
import matplotlib.pyplot as plt
from tkinter import filedialog


class PDZFile:
    """A collection of 1-3 XRFSpectrum objects makes up a single PDZFile object, depending on the number of phases/beams in the assay. Create by providing pdz_file_path (os.path or str)"""

    def __init__(self, pdz_file_path: str):
        self.name = os.path.basename(pdz_file_path)
        self.readPDZFileData(pdz_file_path)
        self.datetime = (
            self.spectrum1.datetime
        )  # pdz as a whole should use first phase datetime?

    def readPDZFileData(self, pdz_file_path: str):
        def readByte(reader):
            """1 byte"""
            return struct.unpack("B", reader.read(1))[0]

        def readShort(reader):
            """AKA Int16: 2 byte Int, -32,768 to 32,767"""
            return struct.unpack("<h", reader.read(2))[0]

        def readUShort(reader):
            """2 byte unsigned Int, 0 to 65,535"""
            return struct.unpack("<H", reader.read(2))[0]

        def readInt(reader):
            """4 byte Int, -2,147,483,648 to 2,147,483,647"""
            return struct.unpack("<i", reader.read(4))[0]

        def readUInt(reader):
            """4 byte unsigned Int, 0 to 4,294,967,295"""
            return struct.unpack("<I", reader.read(4))[0]

        def readFloatSingle(reader):  # 32-bit float = 'single' in c#
            """4 byte Float"""
            return struct.unpack("<f", reader.read(4))[0]

        def readFloatDouble(reader):  # 64-bit float = 'double' in c#
            """8 byte Float"""
            return struct.unpack("<d", reader.read(8))[0]

        def readString(reader):
            """variable length"""
            strlen = readInt(reader)
            # print(f"(string of length {str(strlen)})")
            return reader.read(strlen * 2).decode("utf16")

        def readSpectrumCounts(reader, spectrum):
            for i in range(spectrum.numberOfChannels):
                spectrum.counts.append(readInt(reader))
            log.debug("finished reading counts.")

        def readSpectrumParameters(reader, spectrum):
            # spectrum parameters
            log.debug("READING SPECTRUM PARAMETERS")
            log.debug(readInt(reader))
            log.debug(readFloatSingle(reader))
            spectrum.countsRaw = readInt(reader)
            spectrum.countsValid = readInt(reader)
            # spectrum.deadPercent =
            log.info(f"Spectrum Counts (raw total): {spectrum.countsRaw}")
            log.info(f"Spectrum Counts (valid total): {spectrum.countsValid}")
            log.debug(readFloatSingle(reader))
            log.debug(readFloatSingle(reader))

            spectrum.timeElapsedTotal = readFloatSingle(reader)
            log.info("total time elapsed: " + str(spectrum.timeElapsedTotal))
            log.debug(f"some other time value?: {readFloatSingle(reader)}")
            log.debug(readFloatSingle(reader))
            log.debug(readFloatSingle(reader))
            log.debug(readFloatSingle(reader))

            spectrum.sourceVoltage = readFloatSingle(reader)
            log.info(f"Source Voltage: {spectrum.sourceVoltage}")
            spectrum.sourceCurrent = readFloatSingle(reader)
            log.info(f"Source Current: {spectrum.sourceCurrent}")

            spectrum.filterLayer1ElementZ = readShort(reader)
            spectrum.filterLayer1Thickness = readShort(reader)
            spectrum.filterLayer2ElementZ = readShort(reader)
            spectrum.filterLayer2Thickness = readShort(reader)
            spectrum.filterLayer3ElementZ = readShort(reader)
            spectrum.filterLayer3Thickness = readShort(reader)
            spectrum.filterNumber = readShort(reader)
            spectrum.filterLayer1ElementSymbol = elementZtoSymbol(
                spectrum.filterLayer1ElementZ
            )
            spectrum.filterLayer2ElementSymbol = elementZtoSymbol(
                spectrum.filterLayer2ElementZ
            )
            spectrum.filterLayer3ElementSymbol = elementZtoSymbol(
                spectrum.filterLayer3ElementZ
            )
            spectrum.filterDesciption = f"{spectrum.filterLayer1ElementSymbol}({spectrum.filterLayer1Thickness}uM)/{spectrum.filterLayer2ElementSymbol}({spectrum.filterLayer2Thickness}uM)/{spectrum.filterLayer3ElementSymbol}({spectrum.filterLayer3Thickness}uM)".replace(
                "/(0uM)", ""
            ).replace(
                "(0uM)", "No Filter"
            )

            log.info(f"Filter: {spectrum.filterDesciption}")
            spectrum.detectorTempInC = readFloatSingle(reader)
            spectrum.ambientTempInF = readFloatSingle(reader)
            spectrum.ambientTempInC = (
                spectrum.ambientTempInF - 32
            ) / 1.8  # convert to C
            log.info(
                f"Temps : Detector(C): {spectrum.detectorTempInC:.2f}, Ambient(F): {spectrum.ambientTempInF:.2f}"
            )

            spectrum.vacuumState = readInt(reader)
            log.debug(
                f"vacuum(pdz): {spectrum.vacuumState}"
            )  # unsure how to properly read this value tbh

            spectrum.energyPerChannel = readFloatSingle(reader)
            log.info(f"Energy per channel (eV): {spectrum.energyPerChannel}")

            log.debug(
                f"gain control algorithm: {readShort(reader)}"
            )  # gain Control Algorithms? 0=None, 1=ClassicTurbo, 2=VassiliNextGen

            spectrum.energyChannelStart = readFloatSingle(reader)  # 4
            log.info(
                f"Spectrum channel starts at (ev): {spectrum.energyChannelStart}"
            )  # effectively abscissa

            spectrum_year = readShort(reader)
            spectrum_month = readShort(reader)
            spectrum_datetimedayofweek = readShort(reader)
            spectrum_day = readShort(reader)
            spectrum_hour = readShort(reader)
            spectrum_minute = readShort(reader)
            spectrum_second = readShort(reader)
            spectrum_millisecond = readShort(reader)
            spectrum.datetime = dt(
                spectrum_year,
                spectrum_month,
                spectrum_day,
                spectrum_hour,
                spectrum_minute,
                spectrum_second,
            )
            log.info(f"Date/Time: {spectrum.datetime}")

            spectrum.nosePressure = readFloatSingle(reader)
            log.info(f"Nose Pressure (mBar): {spectrum.nosePressure}")
            spectrum.numberOfChannels = readShort(reader)
            log.info(f"siNumChannels: {spectrum.numberOfChannels}")
            spectrum.noseTempInC = readShort(reader)
            log.info(f"Nose Temperature (C): {spectrum.noseTempInC:.2f}")
            log.debug(f"num8?={readShort(reader)}")  # num8 first assignment

            spectrum.name = readString(reader)
            log.info(f"spectrum name: {spectrum.name}")
            # depending on measurement mode treat spectrum name differently? maybe only applicable for artax spectra?
            log.debug(readShort(reader))  ##num8 second assignment
            log.debug("FINISHED READING SPECTRUM PARAMETERS.")

        # create pdz file reader object
        with open(pdz_file_path, "rb") as self.pdzfilereader:
            # read general pdz file data!
            # read pdz file version
            self.pdzfileversion = readShort(self.pdzfilereader)
            log.info("PDZ version: " + str(self.pdzfileversion))
            if self.pdzfileversion != 25:
                log.error("ERROR: wrong pdz version")

            log.debug("num1=" + str(readUInt(self.pdzfilereader)))
            self.pdzfileversionstr = self.pdzfilereader.read(10).decode("utf16")
            log.info(f"PDZ version (str): {self.pdzfileversionstr}")
            log.info(f"Instrument type: {readUInt(self.pdzfilereader)}")
            # while loop thing? for sections?

            log.debug(f"num2={readShort(self.pdzfilereader)}")
            log.debug(f"num3={readUInt(self.pdzfilereader)}")

            self.instrumentSerialNumber = readString(self.pdzfilereader)
            log.info(f"Instrument Serial Number: {self.instrumentSerialNumber}")

            self.instrumentBuildNumber = readString(self.pdzfilereader)
            log.info(f"Instrument Build Number: {self.instrumentBuildNumber}")

            self.anodeElementZ = int(readByte(self.pdzfilereader))
            self.anodeElementSymbol = elementZtoSymbol(self.anodeElementZ)
            self.anodeElementName = elementZtoName(self.anodeElementZ)
            log.info(f"Anode: {self.anodeElementName}")

            log.debug(
                f"strange 5-size byte thing: {self.pdzfilereader.read(5)}"
            )  # this comes out as b'--A}\x00' ?

            self.detectorType = readString(self.pdzfilereader)
            log.info(f"Detector type: {self.detectorType}")

            self.tubeType = (
                f"{readString(self.pdzfilereader)}:{readShort(self.pdzfilereader)}"
            )
            log.info(f"Source type: {self.tubeType}")

            self.collimatorType = readString(self.pdzfilereader)
            log.info(f"Collimator type: {self.collimatorType}")

            listLength = readInt(self.pdzfilereader)
            sw_fw_vers = {}
            for i in range(listLength):
                key = str(readShort(self.pdzfilereader))
                val = readString(self.pdzfilereader)
                sw_fw_vers[key] = val
            self.softwareFirmwareVersions = sw_fw_vers
            log.info(self.softwareFirmwareVersions)
            log.debug(readShort(self.pdzfilereader))
            log.debug(readInt(self.pdzfilereader))
            log.debug(readInt(self.pdzfilereader))
            log.debug(readInt(self.pdzfilereader))
            log.debug(readInt(self.pdzfilereader))
            log.debug(readInt(self.pdzfilereader))
            log.debug(readInt(self.pdzfilereader))

            log.debug(readFloatSingle(self.pdzfilereader))
            log.debug(readFloatSingle(self.pdzfilereader))
            log.debug(readFloatSingle(self.pdzfilereader))
            log.debug(readFloatSingle(self.pdzfilereader))

            self.assayTimeLive = readFloatSingle(
                self.pdzfilereader
            )  # live time of all phases combined
            self.assayTimeTotal = readFloatSingle(
                self.pdzfilereader
            )  # sum of all phases intended durations (e.g. 60.0 for 20/20/20)
            log.info(f"Time, live: {self.assayTimeLive}")
            log.info(f"Time, total: {self.assayTimeTotal}")

            self.measurementMode = readString(self.pdzfilereader)
            log.info(
                f"Measurement mode: {self.measurementMode} ({str(readInt(self.pdzfilereader))})"
            )
            self.user = readString(self.pdzfilereader)
            log.info(f"User: {self.user}")
            log.debug(f"some short: {readShort(self.pdzfilereader)}")

            # CREATE SPECTRUM 1
            self.spectrum1 = XRFSpectrum()
            readSpectrumParameters(self.pdzfilereader, self.spectrum1)
            readSpectrumCounts(self.pdzfilereader, self.spectrum1)
            self.spectrum1.generateEnergies()
            self.phasecount = 1

            if readShort(self.pdzfilereader) == 3:
                # CREATE SPECTRUM 2
                log.info("Second Phase found.")
                self.phasecount += 1
                self.spectrum2 = XRFSpectrum()
                readSpectrumParameters(self.pdzfilereader, self.spectrum2)
                readSpectrumCounts(self.pdzfilereader, self.spectrum2)
                self.spectrum2.generateEnergies()

                if readShort(self.pdzfilereader) == 3:
                    # CREATE SPECTRUM 3
                    log.info("Third Phase found.")
                    self.phasecount += 1
                    self.spectrum3 = XRFSpectrum()
                    readSpectrumParameters(self.pdzfilereader, self.spectrum3)
                    readSpectrumCounts(self.pdzfilereader, self.spectrum3)
                    self.spectrum3.generateEnergies()

    def __repr__(self) -> str:
        # attrs = vars(self)
        # return attrs
        return f"{self.name} / {self.phasecount} phase / {self.datetime} / {self.instrumentSerialNumber}"


class XRFSpectrum:
    """Class to represent and contain data from a single 'phase' of a PDZ file."""

    def __init__(self):
        self.name = ""
        self.datetime = dt(
            1970, 1, 1, 0, 0, 0
        )  # using unix timestamp 0-time as default.
        self.counts = []
        self.energies = []
        self.energyPerChannel = 20  # in eV
        self.energyChannelStart = 0  # in eV
        self.numberOfChannels = 0
        self.sourceVoltage = 0.0  # in kV
        self.sourceCurrent = 0.0  # in uA
        # filters
        self.filterLayer1ElementZ = 0  # Z num
        self.filterLayer1Thickness = 0  # in um
        self.filterLayer2ElementZ = 0  # Z num
        self.filterLayer2Thickness = 0  # in um
        self.filterLayer3ElementZ = 0  # Z num
        self.filterLayer3Thickness = 0  # in um
        self.filterNumber = 0

        # temp / pressure
        self.detectorTempInC = 0.0
        self.ambientTempInF = 0.0
        self.ambientTempInC = 0.0
        self.noseTempInC = 0.0
        self.nosePressure = 0.0

    def __repr__(self):  # used for print() of class
        return (self.name, self.datetime, self.sourceVoltage, self.sourceCurrent)

    def isNotEmpty(self):
        if self.counts == []:
            return False
        else:
            return True

    def generateEnergies(self):
        self.energies = list(
            ((i * self.energyPerChannel + self.energyChannelStart) * 0.001)
            for i in range(0, self.numberOfChannels)
        )
        log.info(f"Spectrum energies list created for {self.name}")
        return self.energies


def elementZtoSymbol(Z):  # Returns 1-2 character Element symbol as a string
    if Z == 0:
        return ""
    elif Z <= 118:
        elementSymbols = [
            "H",
            "He",
            "Li",
            "Be",
            "B",
            "C",
            "N",
            "O",
            "F",
            "Ne",
            "Na",
            "Mg",
            "Al",
            "Si",
            "P",
            "S",
            "Cl",
            "Ar",
            "K",
            "Ca",
            "Sc",
            "Ti",
            "V",
            "Cr",
            "Mn",
            "Fe",
            "Co",
            "Ni",
            "Cu",
            "Zn",
            "Ga",
            "Ge",
            "As",
            "Se",
            "Br",
            "Kr",
            "Rb",
            "Sr",
            "Y",
            "Zr",
            "Nb",
            "Mo",
            "Tc",
            "Ru",
            "Rh",
            "Pd",
            "Ag",
            "Cd",
            "In",
            "Sn",
            "Sb",
            "Te",
            "I",
            "Xe",
            "Cs",
            "Ba",
            "La",
            "Ce",
            "Pr",
            "Nd",
            "Pm",
            "Sm",
            "Eu",
            "Gd",
            "Tb",
            "Dy",
            "Ho",
            "Er",
            "Tm",
            "Yb",
            "Lu",
            "Hf",
            "Ta",
            "W",
            "Re",
            "Os",
            "Ir",
            "Pt",
            "Au",
            "Hg",
            "Tl",
            "Pb",
            "Bi",
            "Po",
            "At",
            "Rn",
            "Fr",
            "Ra",
            "Ac",
            "Th",
            "Pa",
            "U",
            "Np",
            "Pu",
            "Am",
            "Cm",
            "Bk",
            "Cf",
            "Es",
            "Fm",
            "Md",
            "No",
            "Lr",
            "Rf",
            "Db",
            "Sg",
            "Bh",
            "Hs",
            "Mt",
            "Ds",
            "Rg",
            "Cn",
            "Nh",
            "Fl",
            "Mc",
            "Lv",
            "Ts",
            "Og",
        ]
        return elementSymbols[Z - 1]
    else:
        log.error("Error: Z out of range")
        return "ERR"


def elementZtoSymbolZ(
    Z,
):  # Returns 1-2 character Element symbol formatted WITH atomic number in brackets
    if Z <= 118:
        elementSymbols = [
            "H (1)",
            "He (2)",
            "Li (3)",
            "Be (4)",
            "B (5)",
            "C (6)",
            "N (7)",
            "O (8)",
            "F (9)",
            "Ne (10)",
            "Na (11)",
            "Mg (12)",
            "Al (13)",
            "Si (14)",
            "P (15)",
            "S (16)",
            "Cl (17)",
            "Ar (18)",
            "K (19)",
            "Ca (20)",
            "Sc (21)",
            "Ti (22)",
            "V (23)",
            "Cr (24)",
            "Mn (25)",
            "Fe (26)",
            "Co (27)",
            "Ni (28)",
            "Cu (29)",
            "Zn (30)",
            "Ga (31)",
            "Ge (32)",
            "As (33)",
            "Se (34)",
            "Br (35)",
            "Kr (36)",
            "Rb (37)",
            "Sr (38)",
            "Y (39)",
            "Zr (40)",
            "Nb (41)",
            "Mo (42)",
            "Tc (43)",
            "Ru (44)",
            "Rh (45)",
            "Pd (46)",
            "Ag (47)",
            "Cd (48)",
            "In (49)",
            "Sn (50)",
            "Sb (51)",
            "Te (52)",
            "I (53)",
            "Xe (54)",
            "Cs (55)",
            "Ba (56)",
            "La (57)",
            "Ce (58)",
            "Pr (59)",
            "Nd (60)",
            "Pm (61)",
            "Sm (62)",
            "Eu (63)",
            "Gd (64)",
            "Tb (65)",
            "Dy (66)",
            "Ho (67)",
            "Er (68)",
            "Tm (69)",
            "Yb (70)",
            "Lu (71)",
            "Hf (72)",
            "Ta (73)",
            "W (74)",
            "Re (75)",
            "Os (76)",
            "Ir (77)",
            "Pt (78)",
            "Au (79)",
            "Hg (80)",
            "Tl (81)",
            "Pb (82)",
            "Bi (83)",
            "Po (84)",
            "At (85)",
            "Rn (86)",
            "Fr (87)",
            "Ra (88)",
            "Ac (89)",
            "Th (90)",
            "Pa (91)",
            "U (92)",
            "Np (93)",
            "Pu (94)",
            "Am (95)",
            "Cm (96)",
            "Bk (97)",
            "Cf (98)",
            "Es (99)",
            "Fm (100)",
            "Md (101)",
            "No (102)",
            "Lr (103)",
            "Rf (104)",
            "Db (105)",
            "Sg (106)",
            "Bh (107)",
            "Hs (108)",
            "Mt (109)",
            "Ds (110)",
            "Rg (111)",
            "Cn (112)",
            "Nh (113)",
            "Fl (114)",
            "Mc (115)",
            "Lv (116)",
            "Ts (117)",
            "Og (118)",
        ]
        return elementSymbols[Z - 1]
    else:
        log.error("Error: Z out of range")
        return "ERR"


def elementZtoName(Z):  # Returns Element name
    if Z <= 118:
        elementNames = [
            "Hydrogen",
            "Helium",
            "Lithium",
            "Beryllium",
            "Boron",
            "Carbon",
            "Nitrogen",
            "Oxygen",
            "Fluorine",
            "Neon",
            "Sodium",
            "Magnesium",
            "Aluminium",
            "Silicon",
            "Phosphorus",
            "Sulfur",
            "Chlorine",
            "Argon",
            "Potassium",
            "Calcium",
            "Scandium",
            "Titanium",
            "Vanadium",
            "Chromium",
            "Manganese",
            "Iron",
            "Cobalt",
            "Nickel",
            "Copper",
            "Zinc",
            "Gallium",
            "Germanium",
            "Arsenic",
            "Selenium",
            "Bromine",
            "Krypton",
            "Rubidium",
            "Strontium",
            "Yttrium",
            "Zirconium",
            "Niobium",
            "Molybdenum",
            "Technetium",
            "Ruthenium",
            "Rhodium",
            "Palladium",
            "Silver",
            "Cadmium",
            "Indium",
            "Tin",
            "Antimony",
            "Tellurium",
            "Iodine",
            "Xenon",
            "Caesium",
            "Barium",
            "Lanthanum",
            "Cerium",
            "Praseodymium",
            "Neodymium",
            "Promethium",
            "Samarium",
            "Europium",
            "Gadolinium",
            "Terbium",
            "Dysprosium",
            "Holmium",
            "Erbium",
            "Thulium",
            "Ytterbium",
            "Lutetium",
            "Hafnium",
            "Tantalum",
            "Tungsten",
            "Rhenium",
            "Osmium",
            "Iridium",
            "Platinum",
            "Gold",
            "Mercury",
            "Thallium",
            "Lead",
            "Bismuth",
            "Polonium",
            "Astatine",
            "Radon",
            "Francium",
            "Radium",
            "Actinium",
            "Thorium",
            "Protactinium",
            "Uranium",
            "Neptunium",
            "Plutonium",
            "Americium",
            "Curium",
            "Berkelium",
            "Californium",
            "Einsteinium",
            "Fermium",
            "Mendelevium",
            "Nobelium",
            "Lawrencium",
            "Rutherfordium",
            "Dubnium",
            "Seaborgium",
            "Bohrium",
            "Hassium",
            "Meitnerium",
            "Darmstadtium",
            "Roentgenium",
            "Copernicium",
            "Nihonium",
            "Flerovium",
            "Moscovium",
            "Livermorium",
            "Tennessine",
            "Oganesson",
        ]
        return elementNames[Z - 1]
    else:
        log.error("Error: Z out of range")
        return "ERR"


def elementSymboltoName(sym: str):
    if len(sym) < 4:
        elementSymbols = [
            "H",
            "He",
            "Li",
            "Be",
            "B",
            "C",
            "N",
            "O",
            "F",
            "Ne",
            "Na",
            "Mg",
            "Al",
            "Si",
            "P",
            "S",
            "Cl",
            "Ar",
            "K",
            "Ca",
            "Sc",
            "Ti",
            "V",
            "Cr",
            "Mn",
            "Fe",
            "Co",
            "Ni",
            "Cu",
            "Zn",
            "Ga",
            "Ge",
            "As",
            "Se",
            "Br",
            "Kr",
            "Rb",
            "Sr",
            "Y",
            "Zr",
            "Nb",
            "Mo",
            "Tc",
            "Ru",
            "Rh",
            "Pd",
            "Ag",
            "Cd",
            "In",
            "Sn",
            "Sb",
            "Te",
            "I",
            "Xe",
            "Cs",
            "Ba",
            "La",
            "Ce",
            "Pr",
            "Nd",
            "Pm",
            "Sm",
            "Eu",
            "Gd",
            "Tb",
            "Dy",
            "Ho",
            "Er",
            "Tm",
            "Yb",
            "Lu",
            "Hf",
            "Ta",
            "W",
            "Re",
            "Os",
            "Ir",
            "Pt",
            "Au",
            "Hg",
            "Tl",
            "Pb",
            "Bi",
            "Po",
            "At",
            "Rn",
            "Fr",
            "Ra",
            "Ac",
            "Th",
            "Pa",
            "U",
            "Np",
            "Pu",
            "Am",
            "Cm",
            "Bk",
            "Cf",
            "Es",
            "Fm",
            "Md",
            "No",
            "Lr",
            "Rf",
            "Db",
            "Sg",
            "Bh",
            "Hs",
            "Mt",
            "Ds",
            "Rg",
            "Cn",
            "Nh",
            "Fl",
            "Mc",
            "Lv",
            "Ts",
            "Og",
        ]
        elementNames = [
            "Hydrogen",
            "Helium",
            "Lithium",
            "Beryllium",
            "Boron",
            "Carbon",
            "Nitrogen",
            "Oxygen",
            "Fluorine",
            "Neon",
            "Sodium",
            "Magnesium",
            "Aluminium",
            "Silicon",
            "Phosphorus",
            "Sulfur",
            "Chlorine",
            "Argon",
            "Potassium",
            "Calcium",
            "Scandium",
            "Titanium",
            "Vanadium",
            "Chromium",
            "Manganese",
            "Iron",
            "Cobalt",
            "Nickel",
            "Copper",
            "Zinc",
            "Gallium",
            "Germanium",
            "Arsenic",
            "Selenium",
            "Bromine",
            "Krypton",
            "Rubidium",
            "Strontium",
            "Yttrium",
            "Zirconium",
            "Niobium",
            "Molybdenum",
            "Technetium",
            "Ruthenium",
            "Rhodium",
            "Palladium",
            "Silver",
            "Cadmium",
            "Indium",
            "Tin",
            "Antimony",
            "Tellurium",
            "Iodine",
            "Xenon",
            "Caesium",
            "Barium",
            "Lanthanum",
            "Cerium",
            "Praseodymium",
            "Neodymium",
            "Promethium",
            "Samarium",
            "Europium",
            "Gadolinium",
            "Terbium",
            "Dysprosium",
            "Holmium",
            "Erbium",
            "Thulium",
            "Ytterbium",
            "Lutetium",
            "Hafnium",
            "Tantalum",
            "Tungsten",
            "Rhenium",
            "Osmium",
            "Iridium",
            "Platinum",
            "Gold",
            "Mercury",
            "Thallium",
            "Lead",
            "Bismuth",
            "Polonium",
            "Astatine",
            "Radon",
            "Francium",
            "Radium",
            "Actinium",
            "Thorium",
            "Protactinium",
            "Uranium",
            "Neptunium",
            "Plutonium",
            "Americium",
            "Curium",
            "Berkelium",
            "Californium",
            "Einsteinium",
            "Fermium",
            "Mendelevium",
            "Nobelium",
            "Lawrencium",
            "Rutherfordium",
            "Dubnium",
            "Seaborgium",
            "Bohrium",
            "Hassium",
            "Meitnerium",
            "Darmstadtium",
            "Roentgenium",
            "Copernicium",
            "Nihonium",
            "Flerovium",
            "Moscovium",
            "Livermorium",
            "Tennessine",
            "Oganesson",
        ]
        try:
            i = elementSymbols.index(sym)
            return elementNames[i]
        except Exception:
            log.error("Element symbol unrecognised")
            return "ERR"
    else:
        log.error("Error: Symbol too long")
        return "ERR"


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


def main():
    pdzpath = filedialog.askopenfilename(
        title="Select PDZ File to view",
        filetypes=[("PDZ File", "*.pdz")],
        initialdir=os.getcwd(),
    )
    if pdzpath == "":
        exit()
    # pdzpath = resource_path('00156-REE_IDX.pdz')
    # pdzpath = resource_path('00093-GeoExploration.pdz')
    # pdzpath = resource_path('00148-GeoExploration.pdz')
    # pdzpath = resource_path('00002-Spectrometer Mode.pdz')
    assay = PDZFile(pdzpath)
    print(f"PDZ File Loaded: {assay}")

    # plot stuff
    plt.set_loglevel("error")
    plt.figure(figsize=(16, 8)).set_tight_layout(True)  # Adjust figure size as needed
    plt.xlabel("Energy (keV)")
    plt.ylabel("Counts")
    plt.title(f"{assay.instrumentSerialNumber} - {assay.name}")
    plt.grid(True, which="major", axis="both")
    plt.minorticks_on()
    plt.rcParams["path.simplify"] = False
    plt.style.use("seaborn-v0_8-whitegrid")

    plt.plot(assay.spectrum1.energies, assay.spectrum1.counts)
    plt.legend([assay.spectrum1.name])
    if assay.phasecount > 1:
        plt.plot(assay.spectrum2.energies, assay.spectrum2.counts)
        plt.legend([assay.spectrum1.name, assay.spectrum2.name])
        if assay.phasecount > 2:
            plt.plot(assay.spectrum3.energies, assay.spectrum3.counts)
            plt.legend(
                [assay.spectrum1.name, assay.spectrum2.name, assay.spectrum3.name]
            )

    plt.show()


if __name__ == "__main__":
    log.basicConfig(level=log.INFO)

    main()
