# for chris geo temps questions from bruker 20230907

from PDZreader import PDZFile
import os
import sys
import numpy as np
from pprint import pprint
import csv


def isNullSpectra(
    spectrum_counts: list,
    spectrum_energies: list,
    source_voltage_in_kV: int,
) -> bool:
    """Checks that a spectrum is not empty. Returns TRUE if spectrum seems to be empty/nothing. return FALSE if it seems fine."""
    counts_sum = np.sum(spectrum_counts)
    two_percent_counts_threshold = counts_sum * 0.02
    sum_counting = 0
    for i in range(len(spectrum_counts) - 1, 0, -1):
        sum_counting += spectrum_counts[i]
        if sum_counting > two_percent_counts_threshold:
            abovethreshold_index = i
            break
    if spectrum_energies[abovethreshold_index] < 1:
        # should be considered a fail if 2% sumcounts position is in/near the zero-peak. to check this, check if it is below 1kv?.
        print(
            f"FAILED: {source_voltage_in_kV}kV phase, threshold point: {spectrum_energies[abovethreshold_index]}"
        )
        return True
    else:
        # print(
        #     f"PASSED: {source_voltage_in_kV}kV phase, threshold point: {spectrum_energies[abovethreshold_index]}"
        # )
        return False


def main():
    noDirSelected = True
    while noDirSelected:
        # Ask user for directory
        selectedDir = input(
            f"Please enter the directory you want to check pdz files in (or leave blank to use {os.getcwd()}): "
        )

        # Check if user input is blank
        if selectedDir == "":
            # Set user input to current working directory
            selectedDir = os.getcwd()

        # Check if directory exists
        if os.path.isdir(selectedDir):
            # Print success message
            print(f"Success: Directory {selectedDir} exists.")
            pdz_in_dir_count = 0
            pdz_fnames = []
            # Check if directory contains .pdz files
            for fname in os.listdir(selectedDir):
                if fname.endswith(".pdz"):
                    # print(f'PDZ File Found: {fname}')
                    pdz_fnames.append(fname)
                    pdz_in_dir_count += 1
                    noDirSelected = False
            if pdz_in_dir_count == 0:  # if no pdz files exist
                # Print error message
                print(f"Error: No pdz files exist in {selectedDir}.")

        else:
            # Print error message
            print(f"Error: Directory {selectedDir} does not exist.")

    # Sort pdz_fnames_original
    pdz_fnames.sort()
    # print(f'pdz_fnames_original SORTED: {pdz_fnames_original}')

    # PROCEEDS ONCE SELECTEDDIR IS VALID
    print(f"{pdz_in_dir_count} PDZ files found in {selectedDir}.\n")

    failed_pdz_name_list = []
    report_csv_row_list = []

    for i in range(len(pdz_fnames)):
        file_path = os.path.join(selectedDir, pdz_fnames[i])
        # getdata goes here
        newpdz = PDZFile(file_path)
        # can assume single-spectrum pdz files.
        newspectra = newpdz.spectrum1
        if isNullSpectra(
            spectrum_counts=newspectra.counts,
            spectrum_energies=newspectra.energies,
            source_voltage_in_kV=newspectra.sourceVoltage,
        ):
            failed_pdz_name_list.append(newpdz.name)
            report_csv_row_list.append([newpdz.name, "FAIL"])
        else:
            report_csv_row_list.append([newpdz.name, "PASS"])

        print(f'"{pdz_fnames[i]}" processed. ({i+1}/{len(pdz_fnames)})')
    print(f"All {len(pdz_fnames)} PDZ files were successfully processed.")
    pprint(failed_pdz_name_list)
    print(f"Found {len(failed_pdz_name_list)} failed PDZs.")
    print("Outputting data to CSV...")
    outputcsvpath = os.path.join(selectedDir, "spectrumcheck_results.csv")
    with open(outputcsvpath, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(report_csv_row_list)
        print("Data saved as CSV...")
    input()


if __name__ == "__main__":
    main()
