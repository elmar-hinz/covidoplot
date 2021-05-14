from .lib.Plotter import Plotter
import seaborn as sns
import matplotlib.pyplot as plt

class AgesPlotter(Plotter):

    ylabel = 'Personen'
    xlabel = 'Altersgruppen'

    def prepare(self):
        row = self.data.iloc[0]
        month = str(row['Monat'])
        year = str(row['Jahr'])
        self.title = 'Altersverteilung ' + month + ' ' + year

    def plot(self):
        ages = self.data
        sns.set_theme(style="ticks", color_codes=True)
        sns.barplot(data=ages, x='Altersgruppe', y='Anzahl')\
            .set_title(self.title)
