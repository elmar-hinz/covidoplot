from .lib.TimePlotter import TimePlotter
import matplotlib.pyplot as plt

label_line_35 = 'Gefährdungsstufe 1 = 35'
label_line_50 = 'Gefährdungsstufe 2 = 50'
label_line_100 = 'Inzidenz von 100'
label_line_200 = 'Inzidenz von 200'


class IncidencePlotter(TimePlotter):

    ylabel = '7-Tage-Inzidenz'

    def prepare(self):
        self.df = self.data[self.start:]

    def plot(self):
        district = self.df
        self.ax.plot(
            district.date,
            district.last_weeks_incidence,
            label='Eigenberechnung von Covidoplot',
            alpha=0.5,
            linewidth=1.5,
        )
        try:
            self.ax.plot(
                district.date,
                district['STI-LZG'],
                label='amtlich laut LZG',
                alpha=0.9,
                linewidth=1.5,
            )
        except KeyError:
            pass

    def y(self):
        plt.axhline(35, color='y', label=label_line_35, linewidth=1.5, alpha=0.8)
        plt.axhline(50, color='r', label=label_line_50, linewidth=1.5, alpha=0.8)
        plt.axhline(100, color='#800000', label=label_line_100, linewidth=1.5,
                    alpha=0.8)
        plt.axhline(200, color='#600000', label=label_line_200, linewidth=1.5,
                    alpha=0.8)

