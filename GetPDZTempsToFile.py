# for chris geo temps questions from bruker 20230907

from PDZreader import PDZFile
import os
import sys


#a = PDZFile('C:/Users/Zeb/Documents/GitHub/PDZReader/00002-Spectrometer Mode.pdz')

def main():
    noDirSelected = True
    while noDirSelected:
        # Ask user for directory
        selectedDir = input(f'Please enter the directory you want to rename pdz files in (or leave blank to use {os.getcwd()}): ')

        # Check if user input is blank
        if selectedDir == '':
            # Set user input to current working directory
            selectedDir = os.getcwd()

        # Check if directory exists
        if os.path.isdir(selectedDir):
            # Print success message
            print(f'Success: Directory {selectedDir} exists.')
            pdz_in_dir_count = 0
            pdz_fnames = []
            # Check if directory contains .pdz files
            for fname in os.listdir(selectedDir):
                if fname.endswith('.pdz'):
                    #print(f'PDZ File Found: {fname}')
                    pdz_fnames.append(fname)
                    pdz_in_dir_count += 1
                    noDirSelected = False
            if pdz_in_dir_count == 0:   # if no pdz files exist
                # Print error message
                print(f'Error: No pdz files exist in {selectedDir}.')
            
        else:
            # Print error message
            print(f'Error: Directory {selectedDir} does not exist.')


    # Sort pdz_fnames_original
    pdz_fnames.sort()
    #print(f'pdz_fnames_original SORTED: {pdz_fnames_original}')

    # PROCEEDS ONCE SELECTEDDIR IS VALID
    print(f'{pdz_in_dir_count} PDZ files found in {selectedDir}.\n')
   
    datetimes = []
    detectortemps = []
    ambienttemps = []
    nosetemps = []
    
    for i in range(len(pdz_fnames)):
        file_path = os.path.join(selectedDir, pdz_fnames[i])
        # getdata goes here
        newpdz = PDZFile(file_path)
        datetimes.append(newpdz.datetime.strftime("%H:%M:%S"))
        #print(f'pdz datetime: {newpdz.datetime.strftime("%H:%M:%S")}')
        detectortemps.append(newpdz.spectrum2.detectorTempInC)
        #print(f'detector temp (c): {newpdz.spectrum2.detectorTempInC}')
        ambienttemps.append(newpdz.spectrum2.ambientTempInC)
        #print(f'ambient temp (c): {newpdz.spectrum2.ambientTempInC}')
        nosetemps.append(newpdz.spectrum2.noseTempInC)
        #print(f'nose temp (c): {newpdz.spectrum2.noseTempInC}')

        print(f'"{pdz_fnames[i]}" processed. ({i+1}/{len(pdz_fnames)})')

    with open('temps.txt','x') as fw:
        fw.write(str(datetimes))
        fw.write('\n')
        fw.write(str(detectortemps))
        fw.write('\n')
        fw.write(str(ambienttemps))
        fw.write('\n')
        fw.write(str(nosetemps))   

    print(f'All {len(pdz_fnames)} PDZ files were successfully processed.')


    
    input()

if __name__ == '__main__':
    main()
