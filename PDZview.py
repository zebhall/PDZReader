# PDZview by ZH
versionNum = "v0.0.3"
versionDate = "2023/10/24"

from PDZreader import PDZFile
import flet as ft


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
        self.s1_points = []
        self.s2_points = []
        self.s3_points = []
        self.chartdata = []

        # create data point lists
        if self.s1_energies and self.s1_counts:
            for energy, count in zip(self.s1_energies, self.s1_counts):
                self.s1_points.append(ft.LineChartDataPoint(x=energy, y=count))
            self.s1_chartdata = ft.LineChartData(
                data_points=self.s1_points,
                stroke_width=2,
                color=ft.colors.BLUE,
                curved=False,
            )
            self.chartdata.append(self.s1_chartdata)

        if self.s2_energies and self.s2_counts:
            for energy, count in zip(self.s2_energies, self.s2_counts):
                self.s2_points.append(ft.LineChartDataPoint(x=energy, y=count))
            self.s2_chartdata = ft.LineChartData(
                data_points=self.s2_points,
                stroke_width=2,
                color=ft.colors.GREEN,
                curved=False,
            )
            self.chartdata.append(self.s2_chartdata)

        if self.s3_energies and self.s3_counts:
            for energy, count in zip(self.s3_energies, self.s3_counts):
                self.s3_points.append(ft.LineChartDataPoint(x=energy, y=count))
            self.s3_chartdata = ft.LineChartData(
                data_points=self.s3_points,
                stroke_width=2,
                color=ft.colors.PINK,
                curved=False,
            )
            self.chartdata.append(self.s3_chartdata)

        # create chart object
        self.chart = ft.LineChart(
            data_series=self.chartdata,
            border=ft.border.all(3, ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE)),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=5000,
                color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE),
                width=1,
            ),
            vertical_grid_lines=ft.ChartGridLines(
                interval=5,
                color=ft.colors.with_opacity(0.2, ft.colors.ON_SURFACE),
                width=1,
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.8, ft.colors.BLUE_GREY),
            min_y=0,
            # max_y=max(max(self.s1_counts),max(self.s2_counts),max(self.s3_counts))*1.2,
            min_x=0,
            max_x=50,
            expand=True,
        )

    def build(self):
        return ft.Row(
            controls=[self.chart],
            # height=600,
            # alignment = ft.MainAxisAlignment.CENTER,
            expand=True,
        )


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
