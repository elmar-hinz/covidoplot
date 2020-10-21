import pandas as pd
import matplotlib.pyplot as plt
from configuration import get as c
from .lib.colors import grey
from .lib.commons import style
from .lib.commons import figsize
from .lib.commons import save

label_illness_density = 'Aktiv Infizierte je 100.000 Einwohner'

def plot(dfs, commune):
    field = 'density_of_illness'
    labels = [c('names.communes')[commune], 'Kreis Höxter', 'Deutschland',
              'Italien', 'Deutschlandtrend ohne Lockerungen']
    frames=[]
    frames.append(dfs['commune-' + commune][field])
    frames.append(dfs['district-hoexter'][field])
    frames.append(dfs['country-germany'][field])
    frames.append(dfs['country-italy'][field])
    df = pd.concat(frames, axis=1).dropna()
    _, ax = plt.subplots(figsize=figsize)
    style(ax)
    ax.plot(df)
    start = pd.to_datetime('2020-03-15')
    end = pd.to_datetime('2020-05-20')
    ax.plot([start, end], [130, 0], linestyle='--', color=grey)
    plt.legend(labels=labels)
    plt.ylabel(label_illness_density)
    save('commune', commune, 'upwards-risc-comparism')

