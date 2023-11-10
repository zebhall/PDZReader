download PDZreader.py

USAGE:
(with PDZreader.py in same dir):

    from PDZreader import PDZfile

    pdz_object = PDZFile('pdz_file_path_as_string')
    print(pdz_object.spectrum1.counts)
    print(pdz_object.spectrum1.energies)
    # etc. for spectrum2/spectrum3 if multiphase assay

main func of PDZreader.py has plotting examples for mpl
    