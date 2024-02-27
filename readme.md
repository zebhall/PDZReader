# PDZReader
Read, display, and Extract data from Bruker's proprietary binary xrf-spectra file format (.pdz).

### Usage:

*(PDZreader.py must be accessible in env)*

    from PDZreader import PDZfile

    pdz_object = PDZFile('pdz_file_path_as_string')
    
    print(pdz_object.spectrum1.counts) # 2048-item list
    print(pdz_object.spectrum1.energies) # 2048-item list
    # etc. for spectrum2/spectrum3 if multiphase assay

    pdz_object.plot() # plot all spectra of pdz file using plotly
    
- two object types: *pdzfile* and *spectrum*. One *pdzfile* is made up of 1-3 *spectrum* objects.
- each *spectrum* object has properties of:
    - counts (2048-long list of integers: the photon counts per 'bin' from the detector, the y-axis values of the spectrum
    - energies (2048-long list of floats: the energy (in keV) of each 'bin' of the detector, the x-axis values of the spectrum
    - 

    
