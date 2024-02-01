download PDZreader.py

USAGE:
(PDZreader.py must be accessible in env):

    from PDZreader import PDZfile

    pdz_object = PDZFile('pdz_file_path_as_string')
    
    print(pdz_object.spectrum1.counts) # 2048-item list
    print(pdz_object.spectrum1.energies) # 2048-item list
    # etc. for spectrum2/spectrum3 if multiphase assay

    pdz_object.plot() # plot all spectra of pdz file using plotly
    
    

    
