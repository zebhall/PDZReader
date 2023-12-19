import numpy as np
from scipy.signal import savgol_filter
import plotly.express as px
import pandas as pd
from functools import wraps
import time
from PDZreader import PDZFile


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


@timeit
def smooth_spectrum(spectrum, window_size=51, order=3):
    """
    Smooth a spectrum using the Savitzky-Golay filter.

    Parameters:
    - spectrum: array-like, input spectrum with 2048 values.
    - window_size: int, the size of the smoothing window. Must be an odd integer.
    - order: int, the order of the polynomial used in the filtering. Typically a small positive integer.

    Returns:
    - smoothed_spectrum: array, the smoothed spectrum.
    """

    # Ensure window_size is odd
    if window_size % 2 == 0:
        window_size += 1

    # Apply Savitzky-Golay filter
    smoothed_spectrum = savgol_filter(spectrum, window_size, order)

    return smoothed_spectrum


def main():
    # import spectrum from pdz
    assay = PDZFile("00093-GeoExploration.pdz")
    original_spectrum = assay.spectrum1.counts
    energies = assay.spectrum1.energies
    # Smooth the spectrum
    smoothed_spectrum = smooth_spectrum(original_spectrum, 5, 3)
    # extra_smoothed_spectrum = smooth_spectrum(smoothed_spectrum, 7, 3)
    # Plot original and smoothed spectra for comparison
    df = pd.DataFrame(
        {
            "Energy": energies,
            "Original Spectrum": original_spectrum,
            "Smoothed Spectrum": smoothed_spectrum,
        }
    )

    # Plot with Plotly Express
    fig = px.line(
        df,
        x="Energy",
        y=["Original Spectrum", "Smoothed Spectrum"],
        title="Spectrum Smoothing",
        labels={"value": "Counts", "variable": "Spectrum Type"},
    )
    fig.show()


if __name__ == "__main__":
    main()
