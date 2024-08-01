# Spectra Checking tools
# ZH
# 2023/12/13

import numpy as np
import os
from PDZreader import PDZFile
from tkinter import filedialog
import csv

# import time
# from functools import wraps


# def timeit(func):
#     @wraps(func)
#     def timeit_wrapper(*args, **kwargs):
#         start_time = time.perf_counter()
#         result = func(*args, **kwargs)
#         end_time = time.perf_counter()
#         total_time = end_time - start_time
#         print(f"Function {func.__name__} Took {total_time:.4f} seconds")
#         return result

#     return timeit_wrapper


def sanity_check_spectrum_summethod(spectrum_counts: list[int], spectrum_energies: list[float], source_voltage_in_kV: int) -> bool:
    """Checks that a spectrum is 'sensible', and that the communicated voltage is accurate.
    This is required because of a 'voltage bug' in Bruker pXRF instrument software (or NSI tube firmware), 
    sometimes causing phases of an assay to use an incorrect voltage from a previous phase.
    This algorithm operates by working backwards through the list of counts (starting from the right-hand-side of the spectrum), 
    and summing those counts it passes until it reaches the point where 2% of the total counts of the spectrum have been passed.
    At this point on the spectrum, the energy of that channel should be below the source voltage used for the spectrum 
    (assuming no sum-peaks, which CAN give a false-positive). The Bremsstrahlung in the spectrum *should* drop down 
    to near 0 counts beyond the source voltage (in keV).
    
    `spectrum_counts` is a ordered list of 2048 integers representing the counts from each channel/bin of the detector.\n
    `spectrum_energies` is a ordered list of 2048 floats representing the energy (keV) of each channel/bin of the detector.\n
    `source_voltage_in_kV` is the voltage of the source for the given spectrum, AS REPORTED BY THE OEM API AND IN THE PDZ FILE.\n
    Returns TRUE if sanity check passed, return FALSE if not.
    """
    counts_sum = sum(spectrum_counts)
    two_percent_counts_threshold = counts_sum * 0.02
    sum_counting = 0
    for i in range((len(spectrum_counts) - 1), 0, -1):
        sum_counting += spectrum_counts[i]
        if sum_counting > two_percent_counts_threshold:
            abovethreshold_index = i
            break
    if spectrum_energies[abovethreshold_index] > source_voltage_in_kV:
        # this point should be LOWER than source voltage always, unless a voltage bug has occurred.
        print(f"FAILED Sanity Check! Details: The 2%-total-counts threshold energy ({spectrum_energies[abovethreshold_index]:.2f}kV) was HIGHER than the Reported source voltage ({source_voltage_in_kV}kV).")
        return False
    else:
        # spectum passed checks
        return True


def is_null_spectrum(
    spectrum_counts: list,
    spectrum_energies: list,
    source_voltage_in_kV: int,
) -> bool:
    """Checks that a spectrum is not empty. Returns TRUE if spectrum seems to be empty/nothing. return FALSE if it seems fine."""
    counts_sum = np.sum(spectrum_counts)
    two_percent_counts_threshold = counts_sum * 0.02
    sum_counting = 0
    for i in range((len(spectrum_counts) - 1), 0, -1):
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


# @timeit
# def sanityCheckSpectrum(
#     spectrum_counts: list,
#     spectrum_energies: list,
#     source_voltage_in_kV: int,
#     spectrum_live_time_in_s: float,
# ) -> bool:
#     """Checks that a spectrum is sensible, and that the listed voltage is accurate. This is required because of a bug in Bruker pXRF instrument software, sometimes causing phases of an assay to use an incorrect voltage. Returns TRUE if sanity check passed, return FALSE if not."""

#     # basic method - Set a threshold for noise detection (too small might be prone to noise, too high isn't useful. starting with stddev/100.)
#     # std_dev = np.std(spectrum_counts)
#     # threshold = std_dev / 50

#     # trying method using stddev and mean of last 10-20 bins, plus check for 40+kv excitation
#     noise_mean = np.mean(spectrum_counts[-20:])
#     noise_std_dev = np.std(spectrum_counts[-20:])

#     print(f"{noise_mean=}, {noise_std_dev=}")
#     test_threshold = noise_mean + (10 * noise_std_dev)
#     # if excitation is >40kV (end of spectrum) then this will be unecessary, so need to check for that. trying max reasonable noise mean counts is 3*spectrum_live_time_in_s
#     if noise_mean > (3 * spectrum_live_time_in_s):
#         # set to 1 so that it instantly flags.
#         test_threshold = 1
#     # also fails if counts are 0/1/0/0/1 etc then this won't work. must implement floor. trying min floor assuming 1 count per live second
#     elif test_threshold < (1 * spectrum_live_time_in_s):
#         test_threshold = 1 * spectrum_live_time_in_s

#     threshold = test_threshold

#     # noise_mean = np.mean(spectrum_counts[-20:])
#     # print(f"{noise_mean=}, {spectrum_live_time_in_s=}")
#     # if noise_mean < 2:
#     #     threshold = 2 * spectrum_live_time_in_s
#     # elif noise_mean > spectrum_live_time_in_s:
#     #     threshold = spectrum_live_time_in_s
#     # else:
#     #     threshold = spectrum_live_time_in_s

#     # trying a new method of threshold calculation 20231219, using the last few values of the list to get the 'noise std dev', then adding it to the last channel counts value
#     # std_dev_noise = np.std(spectrum_counts[-10:])
#     # print(f"{std_dev_noise=}")
#     # print(f"{spectrum_live_time_in_s=}")
#     # spectrum_total_cps = sum(spectrum_counts) / spectrum_live_time_in_s
#     # std_dev = np.std(spectrum_counts)
#     # mean_counts = np.mean(spectrum_counts)
#     # median_counts = np.median(spectrum_counts)
#     # print(f"{std_dev=}, {mean_counts=}, {median_counts=}")

#     # threshold = median_counts

#     print(f"{threshold=}")

#     # reverse iterate list to search backwards - no zero peak to worry about, and generally should be faster.
#     for i in range(len(spectrum_counts) - 1, 0, -1):
#         if spectrum_counts[i] > threshold:
#             # Found a peak above the noise threshold
#             peak_index = i
#             break
#     else:
#         # No peak above the noise threshold found
#         peak_index = None

#     if peak_index is not None:
#         print(
#             f"Latest point with a peak above noise: energy={spectrum_energies[peak_index]}, counts={spectrum_counts[peak_index]}"
#         )
#         if spectrum_energies[peak_index] < source_voltage_in_kV:
#             # this point should be LOWER than source voltage *almost* always. some exclusions, incl. sum peaks, but those should be niche.
#             return True
#         else:
#             print(f"FAILED: {source_voltage_in_kV}kV phase")
#             return False

#     else:
#         # No peak above noise detected - flat spectra?
#         print(f"FAILED: {source_voltage_in_kV}kV phase")
#         return False

def sanity_check_directory(dir:str):

    print(f"Recursively searching for PDZ files in {dir}...")

    pdz_in_dir_count = 0
    pdz_fnames = []

    # # Check if directory contains .pdz files
    # for fname in os.listdir(dir):
    #     if fname.endswith(".pdz"):
    #         pdz_fnames.append(fname)
    #         pdz_in_dir_count += 1

        # Check if directory contains .pdz files and gather them from all subdirectories
    for root, _, files in os.walk(dir):
        for fname in files:
            if fname.endswith(".pdz"):
                full_path = os.path.join(root, fname)
                pdz_fnames.append(full_path)
                pdz_in_dir_count += 1

    if pdz_in_dir_count == 0:  # if no pdz files exist
        print(f"Error: No pdz files exist in {dir}.")

    # Sort pdz_fnames
    pdz_fnames.sort()

    print(f"{pdz_in_dir_count} PDZ files found in {dir}.\n")

    failed_pdz_name_list = []
    failed_pdz_filepath_list = []
    failed_pdz_dt_list = []

    for i in range(len(pdz_fnames)):
        file_path = pdz_fnames[i]
        
        try:
            test_pdz = PDZFile(file_path)

            for test_spectrum in [test_pdz.spectrum1, test_pdz.spectrum2, test_pdz.spectrum3]:
                if test_spectrum.is_not_empty():
                    if not sanity_check_spectrum_summethod(
                        spectrum_counts=test_spectrum.counts,
                        spectrum_energies=test_spectrum.energies,
                        source_voltage_in_kV=int(test_spectrum.source_voltage),
                    ):
                        failed_pdz_name_list.append(test_pdz.pdz_file_name)
                        failed_pdz_filepath_list.append(file_path)
                        failed_pdz_dt_list.append(test_pdz.datetime)
                        break
        except Exception as e:
            print(f"Error: PDZ File {pdz_fnames[i]} could not be processed ({e})")
    

        print(f'"{os.path.relpath(file_path, dir)}" processed. ({i+1}/{len(pdz_fnames)})')
    print(f"All {len(pdz_fnames)} PDZ files were successfully processed.")
    print(f"Found {len(failed_pdz_name_list)} failed PDZs.")
    if len(failed_pdz_name_list) != 0:
        print(f"Failed PDZ Files: {failed_pdz_name_list}")
        print("Creating CSV File...")
        csv_fname = 'pdz_results.csv'
        with open(csv_fname, 'x', newline='') as csvfile:
            fieldnames = ['File', 'PDZ Date', 'Path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in range(len(failed_pdz_name_list)):
                writer.writerow({'File': failed_pdz_name_list[i], 'PDZ Date': failed_pdz_dt_list[i], 'Path': failed_pdz_filepath_list[i]})
        print(f"CSV File Created, saved as {csv_fname}...")
        
    input()



def main():

    starting_dir = filedialog.askdirectory(initialdir=os.getcwd(), title="Select Directory to Recursively Search for PDZ Files")
    sanity_check_directory(starting_dir)

    # assay = PDZFile("PDZ for test/00007-Spectrometer Mode.pdz")

    # sanity_check_spectrum_summethod(
    #     spectrum_counts=assay.spectrum1.counts,
    #     spectrum_energies=assay.spectrum1.energies,
    #     source_voltage_in_kV=int(assay.spectrum1.source_voltage),
    # )
    # if assay.spectrum2.is_not_empty():
    #     sanity_check_spectrum_summethod(
    #         spectrum_counts=assay.spectrum2.counts,
    #         spectrum_energies=assay.spectrum2.energies,
    #         source_voltage_in_kV=int(assay.spectrum2.source_voltage),
    #     )
    # if assay.spectrum3.is_not_empty():
    #     sanity_check_spectrum_summethod(
    #         spectrum_counts=assay.spectrum3.counts,
    #         spectrum_energies=assay.spectrum3.energies,
    #         source_voltage_in_kV=int(assay.spectrum3.source_voltage),
    #     )
    # assay.plot()


if __name__ == "__main__":
    # log.basicConfig(level=log.DEBUG)
    main()
