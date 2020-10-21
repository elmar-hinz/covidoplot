import matplotlib.pyplot as plt
from .lib.commons import style, title, ticker, figsize, save
from .lib.colors import blue, red, yellow

title_last_weeks_incidence = '7-Tage-Inzidenz '
label_last_weeks_incidence = 'neue Fälle je 100.000 Einwohner'
label_red_line = 'Gefährdungsstufe 2 = 50'
label_yellow_line = 'Gefährdungsstufe 1 = 35'

def plot(df, type, key):
    _, ax = plt.subplots(figsize=figsize)
    style(ax)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.plot(df.date, df.last_weeks_incidence, label='7-Tage-Inzidenz',
            color=blue)
    plt.axhline(50, color=red, label=label_red_line)
    plt.axhline(35, color=yellow, label=label_yellow_line)
    plt.title(title_last_weeks_incidence + title(type, key))
    plt.ylabel(label_last_weeks_incidence)
    ax.legend(loc='upper left')
    save(type, key, 'last_weeks_incidence')

