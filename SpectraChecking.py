# Spectra Checking tools
# ZH
# 2023/12/13

import numpy as np
from PDZreader import PDZFile

from functools import wraps
import time


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


def sanityCheckSpectrum_sumMethod(
    spectrum_counts: list,
    spectrum_energies: list,
    source_voltage_in_kV: int,
    spectrum_live_time_in_s: float,
) -> bool:
    """Checks that a spectrum is sensible, and that the listed voltage is accurate. This is required because of a bug in Bruker pXRF instrument software, sometimes causing phases of an assay to use an incorrect voltage. Returns TRUE if sanity check passed, return FALSE if not."""
    counts_sum = np.sum(spectrum_counts)
    two_percent_counts_threshold = counts_sum * 0.02
    sum_counting = 0
    for i in range(len(spectrum_counts) - 1, 0, -1):
        sum_counting += spectrum_counts[i]
        if sum_counting > two_percent_counts_threshold:
            # Found a peak above the noise threshold
            abovethreshold_index = i
            break
    if spectrum_energies[abovethreshold_index] < source_voltage_in_kV:
        # this point should be LOWER than source voltage always.
        print(
            f"PASSED: {source_voltage_in_kV}kV phase, threshold point: {spectrum_energies[abovethreshold_index]}"
        )
        return True
    else:
        print(
            f"FAILED: {source_voltage_in_kV}kV phase, threshold point: {spectrum_energies[abovethreshold_index]}"
        )
        return False


# @timeit
def sanityCheckSpectrum(
    spectrum_counts: list,
    spectrum_energies: list,
    source_voltage_in_kV: int,
    spectrum_live_time_in_s: float,
) -> bool:
    """Checks that a spectrum is sensible, and that the listed voltage is accurate. This is required because of a bug in Bruker pXRF instrument software, sometimes causing phases of an assay to use an incorrect voltage. Returns TRUE if sanity check passed, return FALSE if not."""

    # basic method - Set a threshold for noise detection (too small might be prone to noise, too high isn't useful. starting with stddev/100.)
    # std_dev = np.std(spectrum_counts)
    # threshold = std_dev / 50

    # trying method using stddev and mean of last 10-20 bins, plus check for 40+kv excitation
    noise_mean = np.mean(spectrum_counts[-20:])
    noise_std_dev = np.std(spectrum_counts[-20:])

    print(f"{noise_mean=}, {noise_std_dev=}")
    test_threshold = noise_mean + (10 * noise_std_dev)
    # if excitation is >40kV (end of spectrum) then this will be unecessary, so need to check for that. trying max reasonable noise mean counts is 3*spectrum_live_time_in_s
    if noise_mean > (3 * spectrum_live_time_in_s):
        # set to 1 so that it instantly flags.
        test_threshold = 1
    # also fails if counts are 0/1/0/0/1 etc then this won't work. must implement floor. trying min floor assuming 1 count per live second
    elif test_threshold < (1 * spectrum_live_time_in_s):
        test_threshold = 1 * spectrum_live_time_in_s

    threshold = test_threshold

    # noise_mean = np.mean(spectrum_counts[-20:])
    # print(f"{noise_mean=}, {spectrum_live_time_in_s=}")
    # if noise_mean < 2:
    #     threshold = 2 * spectrum_live_time_in_s
    # elif noise_mean > spectrum_live_time_in_s:
    #     threshold = spectrum_live_time_in_s
    # else:
    #     threshold = spectrum_live_time_in_s

    # trying a new method of threshold calculation 20231219, using the last few values of the list to get the 'noise std dev', then adding it to the last channel counts value
    # std_dev_noise = np.std(spectrum_counts[-10:])
    # print(f"{std_dev_noise=}")
    # print(f"{spectrum_live_time_in_s=}")
    # spectrum_total_cps = sum(spectrum_counts) / spectrum_live_time_in_s
    # std_dev = np.std(spectrum_counts)
    # mean_counts = np.mean(spectrum_counts)
    # median_counts = np.median(spectrum_counts)
    # print(f"{std_dev=}, {mean_counts=}, {median_counts=}")

    # threshold = median_counts

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
            print(f"FAILED: {source_voltage_in_kV}kV phase")
            return False

    else:
        # No peak above noise detected - flat spectra?
        print(f"FAILED: {source_voltage_in_kV}kV phase")
        return False


def main():
    assay = PDZFile("01142-GeoExploration-FAIL20231214.pdz")
    # assay = PDZFile("00156-REE_IDX.pdz")
    # assay = PDZFile("00007-Spectrometer Mode.pdz")
    # assay = PDZFile("00007-GeoExploration-SiO2.pdz")
    # assay = PDZFile("00279-GeoExploration-SiO2-180s.pdz")
    # assay = PDZFile("00148-GeoExploration.pdz")
    # assay = PDZFile("00020-AuPathfinder.pdz")
    # assay = PDZFile("00332-GeoExploration-VOLTAGEBUGGED.pdz")
    # assay = PDZFile("00333-GeoExploration-VOLTAGEBUGGED.pdz")
    # assay = PDZFile("00334-GeoExploration-VOLTAGEBUGGED.pdz")
    # assay = PDZFile("00335-GeoExploration-VOLTAGEBUGGED.pdz")
    # assay = PDZFile("00336-GeoExploration-VOLTAGEBUGGED.pdz")
    # assay = PDZFile("00337-GeoExploration-VOLTAGEBUGGED.pdz")
    # assay = PDZFile("00338-GeoExploration-VOLTAGEBUGGED.pdz")
    # assay = PDZFile("00339-GeoExploration-VOLTAGEBUGGED.pdz")
    # assay = PDZFile("Fe-Mn-SumPeak-Example_00020-AuPathfinder.pdz")
    # print(f"{assay.spectrum1.sourceVoltage=}")
    # print(f"{assay.spectrum1.timeLive=}")
    sanityCheckSpectrum_sumMethod(
        spectrum_counts=assay.spectrum1.counts,
        spectrum_energies=assay.spectrum1.energies,
        source_voltage_in_kV=int(assay.spectrum1.sourceVoltage),
        spectrum_live_time_in_s=assay.spectrum1.timeLive,
    )
    try:
        # print(f"{assay.spectrum2.sourceVoltage=}")
        # print(f"{assay.spectrum2.timeLive=}")
        sanityCheckSpectrum_sumMethod(
            spectrum_counts=assay.spectrum2.counts,
            spectrum_energies=assay.spectrum2.energies,
            source_voltage_in_kV=int(assay.spectrum2.sourceVoltage),
            spectrum_live_time_in_s=assay.spectrum2.timeLive,
        )
    except AttributeError:
        print("No Phase 2 present in pdz")
    try:
        # print(f"{assay.spectrum3.sourceVoltage=}")
        # print(f"{assay.spectrum3.timeLive=}")
        sanityCheckSpectrum_sumMethod(
            spectrum_counts=assay.spectrum3.counts,
            spectrum_energies=assay.spectrum3.energies,
            source_voltage_in_kV=int(assay.spectrum3.sourceVoltage),
            spectrum_live_time_in_s=assay.spectrum3.timeLive,
        )
    except AttributeError:
        print("No Phase 3 present in pdz")

    assay.plot()


if __name__ == "__main__":
    # log.basicConfig(level=log.DEBUG)
    main()
