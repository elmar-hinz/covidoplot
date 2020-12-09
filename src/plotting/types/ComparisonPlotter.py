from .lib.TimePlotter import TimePlotter
import matplotlib.pyplot as plt

class ComparisonPlotter(TimePlotter):

    field = ''
    labels = []
    colors = []

    def prepare(self):
        self.frames = []
        for df in self.data:
            self.frames.append(df[self.start:])

    def plot(self):
        for i in range(len(self.frames)):
            df = self.frames[i]
            self.ax.plot(
                df.date,
                df[self.field],
                color=self.colors[i],
                label=self.labels[i],
                alpha=1,
                linewidth=1,
            )
