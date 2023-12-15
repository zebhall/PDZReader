# Spectra Checking tools
# ZH
# 2023/12/13

import numpy as np
from PDZreader import PDZFile

# from functools import wraps
# import time
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


# @timeit
def sanityCheckSpectrum(
    spectrum_counts: list, spectrum_energies: list, source_voltage_in_kV: int
) -> bool:
    """Checks that a spectrum is sensible, and that the listed voltage is accurate. This is required because of a bug in Bruker pXRF instrument software, sometimes causing phases of an assay to use an incorrect voltage. Returns TRUE if sanity check passed, return FALSE if not."""
    # Calculate the standard deviation of the spectrum
    std_dev = np.std(spectrum_counts)
    # print(f"spectrum std dev = {std_dev}")

    # Set a threshold for noise detection (too small might be prone to noise, too high isn't useful. starting with stddev/100.)
    threshold = std_dev / 50
    print(f"{threshold=}")

    # reverse iterate list to search backwards - no zero peak to worry about, and generally should be faster.
    for i in range(len(spectrum_counts) - 1, 0, -1):
        if spectrum_counts[i] > threshold:
            # Found a peak above the noise threshold
            peak_index = i
            break
    else:
        # No peak above the noise threshold found
        peak_index = None

    if peak_index is not None:
        print(
            f"Latest point with a peak above noise: energy={spectrum_energies[peak_index]}, counts={spectrum_counts[peak_index]}"
        )
        if spectrum_energies[peak_index] < source_voltage_in_kV:
            # this point should be LOWER than source voltage *almost* always. some exclusions, incl. sum peaks, but those should be niche.
            return True
        else:
            return False

    else:
        # No peak above noise detected - flat spectra?
        return False


def main():
    # assay = PDZFile("01142-GeoExploration-FAIL20231214.pdz")
    # assay = PDZFile("00156-REE_IDX.pdz")
    # assay = PDZFile("00007-Spectrometer Mode.pdz")
    # assay = PDZFile("00007-GeoExploration-SiO2.pdz")
    assay = PDZFile("00279-GeoExploration-SiO2-180s.pdz")
    # assay = PDZFile("00148-GeoExploration.pdz")
    # assay = PDZFile("00020-AuPathfinder.pdz")
    print(f"{assay.spectrum1.sourceVoltage=}")
    print(f"{assay.spectrum1.timeLive=}")
    sanityCheckSpectrum(
        spectrum_counts=assay.spectrum1.counts,
        spectrum_energies=assay.spectrum1.energies,
        source_voltage_in_kV=int(assay.spectrum1.sourceVoltage),
    )
    try:
        print(f"{assay.spectrum2.sourceVoltage=}")
        print(f"{assay.spectrum2.timeLive=}")
        sanityCheckSpectrum(
            spectrum_counts=assay.spectrum2.counts,
            spectrum_energies=assay.spectrum2.energies,
            source_voltage_in_kV=int(assay.spectrum2.sourceVoltage),
        )
    except AttributeError:
        print("no phase 2 present in pdz")
    try:
        print(f"{assay.spectrum3.sourceVoltage=}")
        print(f"{assay.spectrum3.timeLive=}")
        sanityCheckSpectrum(
            spectrum_counts=assay.spectrum3.counts,
            spectrum_energies=assay.spectrum3.energies,
            source_voltage_in_kV=int(assay.spectrum3.sourceVoltage),
        )
    except AttributeError:
        print("no phase 3 present in pdz")

    assay.plot()


if __name__ == "__main__":
    # log.basicConfig(level=log.DEBUG)
    main()
