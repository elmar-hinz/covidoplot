from .lib.TimePlotter import TimePlotter

class StackedPlotter(TimePlotter):

    ylabel = 'bestätigte Fälle'

    def prepare(self):
        self.df = self.data[self.start:]

    def plot(self):
        district = self.df
        self.ax.stackplot(
            district.date,
            district.ill,
            district.recovered,
            district.dead,
            labels=['infiziert', 'genesen', 'verstorben'],
            colors=['r', 'g', 'k'],
            alpha=0.9,
            linewidth=0,
        )

