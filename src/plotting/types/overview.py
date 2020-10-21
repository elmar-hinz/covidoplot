import matplotlib.pyplot as plt
from .lib.commons import style, title, ticker, figsize, save
from .lib.colors import blue, orange, darkgreen, black, red

label_confirmed = 'bestätigte Fälle'

def plot(df, type, key):
    # Can't use the df.plot() syntax here.
    # To pretty format the x-axis a datetime object is required as index.
    # But if that requirement is satisfied, bars are dropped, when
    # lines are plotted. Seems to be a strange bug in the pandas implementation.
    width = 1
    _, ax = plt.subplots(figsize=figsize)
    style(ax)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.bar(df.date, df.confirmed, width, label='alle Fälle', color=blue)
    ax.bar(df.date, df.new, width, label='neue Fälle', color=orange)
    ax.plot(df.date, df.ill, label='infiziert', color=red)
    ax.plot(df.date, df.recovered, label='genesen', color=darkgreen)
    ax.plot(df.date, df.dead, label='verstorben', color=black)
    ax.legend(loc='upper left')
    plt.title('Übersicht: ' + title(type, key))
    plt.ylabel(label_confirmed)
    save(type, key, 'overview')

