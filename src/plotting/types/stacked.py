import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from .lib.colors import red, black, green
from .lib.commons import style
from .lib.commons import figsize
from .lib.commons import title
from .lib.commons import save

label_confirmed = 'bestätigte Fälle'


def plot(df, type, key):
    _, ax = plt.subplots(figsize=figsize)
    style(ax)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.stackplot(df.date,
                 df.ill, df.recovered, df.dead,
                 labels=['infiziert', 'genesen', 'verstorben'],
                 colors=[red, green, black]
                 )
    ax.legend(loc='upper left')
    plt.title(title(type, key))
    plt.ylabel(label_confirmed)
    save(type, key, 'stacked')

