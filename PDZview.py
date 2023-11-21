# PDZview by ZH
versionNum = "v0.0.3"
versionDate = "2023/10/24"

from PDZreader import PDZFile
import plotly.express as px
import flet as ft
from flet.plotly_chart import PlotlyChart
import pandas as pd


class App:
    def __init__(self, page: ft.Page):
        self.page = page


class SpectrumPlot(ft.UserControl):
    def __init__(
        self,
        title,
        s1_energies: list = None,
        s1_counts: list = None,
        s2_energies: list = None,
        s2_counts: list = None,
        s3_energies: list = None,
        s3_counts: list = None,
        pick_peaks: bool = False,
    ):
        super().__init__()
        self.title = title
        self.s1_energies = s1_energies
        self.s1_counts = s1_counts
        self.s2_energies = s2_energies
        self.s2_counts = s2_counts
        self.s3_energies = s3_energies
        self.s3_counts = s3_counts
        print(len(self.s1_energies))
        print(len(self.s1_counts))

        self.df1 = pd.DataFrame(
            data={
                "phase": [1] * 2048,
                "energy": self.s1_energies,
                "counts": self.s1_counts,
            }
        )
        self.df2 = pd.DataFrame(
            data={
                "phase": [2] * 2048,
                "energy": self.s2_energies,
                "counts": self.s2_counts,
            }
        )
        self.df3 = pd.DataFrame(
            data={
                "phase": [3] * 2048,
                "energy": self.s3_energies,
                "counts": self.s3_counts,
            }
        )

        self.df = pd.concat([self.df1, self.df2, self.df3])

        # create figure
        self.fig = px.line(self.df, x="energy", y="counts", color="phase")

        # create data point df

    def build(self):
        return PlotlyChart(self.fig, expand=True)


def main(page: ft.Page) -> None:
    # initial window settings
    page.title = "PDZView"
    page.expand = True
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_EVENLY
    page.padding = 20

    # get pdz data
    pdz = PDZFile("00093-GeoExploration.pdz")

    # create widgets
    viewer = SpectrumPlot(
        title="pdz",
        s1_energies=pdz.spectrum1.energies,
        s1_counts=pdz.spectrum1.counts,
        s2_energies=pdz.spectrum2.energies,
        s2_counts=pdz.spectrum2.counts,
        s3_energies=pdz.spectrum3.energies,
        s3_counts=pdz.spectrum3.counts,
    )

    # add widgets
    page.add(viewer)

    # resize logic
    # def page_resize(e):
    #     viewer.height = page.__getattribute__("window_height") / 1.1
    #     viewer.width = page.__getattribute__("window_width") / 1.1
    #     viewer.update()
    # page.on_resize = page_resize

    page.update()


if __name__ == "__main__":
    ft.app(target=main)
