# PDZ-Spectra-To-CSV test
versionNum = "v0.0.1"
versionDate = "2024/01/30"

from PDZreader import PDZFile
import os
import pandas as pd


def getPDZFilePathList(directory: str) -> list[str]:
    """Given directory path, return list of every pdz file within, as full filepaths."""
    if not os.path.isdir(directory):
        raise ValueError(f"The directory '{directory}' does not exist.")
    pdz_file_paths: list[str] = []
    # iterate through all files in dir
    for root, dirs, files in os.walk(directory):
        for file in files:
            # check if pdz file
            if file.endswith(".pdz"):
                # construct full file path and add to list
                file_path = os.path.join(root, file)
                pdz_file_paths.append(file_path)

    return pdz_file_paths


def main():
    pdz_directory: str = input(f"Enter directory to look for PDZ Files: ")
    pdz_paths: list[str] = getPDZFilePathList(pdz_directory)
    pdz_count_total: int = len(pdz_paths)
    pdz_count_processed: int = 0
    print(f"Processing All {pdz_count_total} PDZ Files...")
    # iterate over pdz path strs and feed to PDZFile init, then extract required data to create row object, then convert to df then CSV.
    for pdz_path in pdz_paths:
        pdz_obj = PDZFile(pdz_path)
        pdz_data_dict = {}
        if pdz_obj.spectrum1.is_not_empty():
            pdz_data_dict[
                f"Phase 1 Counts ({pdz_obj.spectrum1.source_voltage:.0f}kV)"
            ] = pdz_obj.spectrum1.counts
            pdz_data_dict[
                f"Phase 1 Energies ({pdz_obj.spectrum1.source_voltage:.0f}kV)"
            ] = pdz_obj.spectrum1.energies
        if pdz_obj.spectrum2.is_not_empty():
            pdz_data_dict[
                f"Phase 2 Counts ({pdz_obj.spectrum2.source_voltage:.0f}kV)"
            ] = pdz_obj.spectrum2.counts
            pdz_data_dict[
                f"Phase 2 Energies ({pdz_obj.spectrum2.source_voltage:.0f}kV)"
            ] = pdz_obj.spectrum2.energies
        if pdz_obj.spectrum3.is_not_empty():
            pdz_data_dict[
                f"Phase 3 Counts ({pdz_obj.spectrum3.source_voltage:.0f}kV)"
            ] = pdz_obj.spectrum3.counts
            pdz_data_dict[
                f"Phase 3 Energies ({pdz_obj.spectrum3.source_voltage:.0f}kV)"
            ] = pdz_obj.spectrum3.energies
        csv_name = pdz_obj.pdz_file_name.replace(".pdz", ".csv")
        csv_path = os.path.join(pdz_directory, csv_name)
        df = pd.DataFrame(pdz_data_dict)
        df.to_csv(csv_path)
        pdz_count_processed += 1
        print(f"Processed: {pdz_obj.pdz_file_name} [{pdz_count_processed}/{pdz_count_total}]")


if __name__ == "__main__":
    main()
