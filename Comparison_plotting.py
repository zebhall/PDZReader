# plotting for RZ R&D
# zh 20240305

from PDZreader import PDZFile
import pandas as pd
import plotly_express as px
from tkinter import filedialog
import os


def main():

    pdzpaths: tuple[str] = filedialog.askopenfilenames(
        title="Select PDZ Files to include in plot",
        filetypes=[("PDZ File", "*.pdz")],
        initialdir=os.getcwd(),
    )

    # print(pdzpaths)

    pdz_dfs: list[pd.DataFrame] = []

    for pdz_fname in pdzpaths:
        pdz = PDZFile(f"{pdz_fname}")

        df = pd.DataFrame(
            data={
                "Info": [
                    f"{pdz.pdz_file_name} ({pdz.spectrum1.source_voltage:.0f}kV / {pdz.spectrum1.source_current:.2f}uA / {pdz.spectrum1.filterDesciption} / {pdz.spectrum1.timeLive:.2f}s live)"
                ]
                * 2048,
                "Energy (keV)": pdz.spectrum1.energies,
                "Counts": pdz.spectrum1.counts,
            }
        )
        pdz_dfs.append(df)

        # df = pd.DataFrame(
        #     data={
        #         "Info": [
        #             f"{pdz.name} ({pdz.spectrum3.sourceVoltage:.0f}kV / {pdz.spectrum3.sourceCurrent:.2f}uA / {pdz.spectrum3.filterDesciption} / {pdz.spectrum3.timeLive:.2f}s live)"
        #         ]
        #         * 2048,
        #         "Energy (keV)": pdz.spectrum3.energies,
        #         "Counts": pdz.spectrum3.counts,
        #     }
        # )
        # pdz_dfs.append(df)

    df_all = pd.concat(pdz_dfs)  # all

    # plot
    fig = px.line(df_all, x="Energy (keV)", y="Counts", color="Info")
    fig.add_vline(
        x=4.512,
        annotation_text="Ti Kα",
        annotation_position="bottom right",
        line_width=1,
        line_dash="dash",
        line_color="gray",
    )
    fig.add_vline(
        x=15.775,
        annotation_text="Zr Kα",
        annotation_position="bottom right",
        line_width=1,
        line_dash="dash",
        line_color="gray",
    )
    fig.update_layout(legend=dict(yanchor="top", y=0.99, xanchor="right", x=0.99))
    # fig.show()

    # save interactive html file with plot
    plot_name = input("Please Enter a Name for the Interactable Plot: ")
    output_file_name = f"{plot_name}_interactable_plot.html"
    fig.write_html(output_file_name)
    print(f"File saved as {output_file_name}.")


if __name__ == "__main__":
    main()
