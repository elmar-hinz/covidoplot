import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
from configuration import plural as p
from configuration import get as c
from lib import read_imported_dfs

figsize=(9, 6)

black = c('colors.black')
grey = c('colors.grey')
white = c('colors.white')
darkred = c('colors.darkred')
red = c('colors.red')
pink = c('colors.pink')
orange = c('colors.orange')
yellow = c('colors.yellow')
lightgreen = c('colors.lightgreen')
green = c('colors.green')
darkgreen = c('colors.darkgreen')
blue = c('colors.blue')
darkblue = c('colors.darkblue')
purple = c('colors.purple')

colors = [ red, pink, orange, yellow, lightgreen, darkgreen, blue, darkblue,
           purple, grey, darkred, black, white ]

label_confirmed_density = 'bestätigte Fälle je 100.000 Einwohner'
label_illness_density = 'Aktiv Infizierte je 100.000 Einwohner'
label_confirmed = 'bestätigte Fälle'
label_last_weeks_incidence = 'neue Fälle je 100.000 Einwohner'
title_last_weeks_incidence = '7-Tage-Inzidenz '
label_red_line = 'Gefährdungsstufe 2 = 50'
label_yellow_line = 'Gefährdungsstufe 1 = 35'


def title(type, key):
    name = c('names')[p(type)][key]
    if isinstance(name, str):
        return name
    else:
        return name['german']

def style(ax):
    major = mdates.DateFormatter('%d.%m.')
    ax.xaxis.set_major_formatter(major)
    plt.xticks(rotation=45)
    plt.grid(True, alpha=0.3, linestyle='dashdot')

def save(type, key, title):
    name = type + '-' + key + '-' + title + '.png'
    path = c('directories.export.plots') + name
    plt.savefig(path)
    time.sleep(0.3)
    plt.clf()
    time.sleep(0.1)
    plt.close()
    time.sleep(0.1)

def concat(dfs):
    cdfs = {}
    for district in c('names.districts'):
        frames = []
        keys = []
        for commune, parent in c('parents.communes').items():
            if parent == district:
                frames.append(dfs['commune-' + commune].transpose())
                keys.append(commune)
        df = pd.concat(frames, keys=keys)
        cdfs['district-' + district] = df
    return cdfs

def plot_helper_comparism(
        cdf, type, child_type, key, subindex, ylabel, title_prefix,
        file_suffix):
    _, ax = plt.subplots(figsize=figsize)
    style(ax)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    i = 0
    for k, v in c('names')[p(child_type)].items():
        mf = cdf.loc[(k, subindex)]
        ax.plot(mf, label=v, color=colors[i])
        i += 1
    ax.legend(loc='upper left')
    plt.title(title_prefix + ': ' + title(type, key))
    plt.ylabel(ylabel)
    save(type, key, file_suffix + '-comparism')

def plot_overview(df, type, key):
    # Can't use the df.plot() syntax here.
    # To pretty format the x-axis a datetime object is required as index.
    # But if that requirement is satisfied, bars are dropped, when
    # lines are plotted. Seems to be a strange bug in the pandas implementation.
    width = 1
    # df = import_dates(df)
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

def plot_last_weeks_incidence(df, type, key):
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

def plot_stacked(df, type, key):
    # df = import_dates(df)
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

def plot_absolute_comparism(cdf, type, child_type, key):
    plot_helper_comparism(
        cdf, type, child_type, key,
        'confirmed',
        label_confirmed,
        'Absolute Fallzahlen',
        'absolute'
    )

def plot_relative_comparism(cdf, type, child_type, key):
    plot_helper_comparism(
        cdf, type, child_type, key,
        'density_of_cases',
        label_confirmed_density,
        'Relative Fallzahlen',
        'relative'
    )

def plot_risc_comparism(cdf, type, child_type, key):
    plot_helper_comparism(
        cdf, type, child_type, key,
        'density_of_illness',
        label_illness_density,
        'Infektionsrisiko',
        'risc'
    )

def plot_parents_risc_comparism(dfs, commune):
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

def process_countries(dfs, cdfs):
    for country in c('names.countries'):
        plot_overview(dfs['country-' + country], 'country', country)
        plot_stacked(dfs['country-' + country], 'country', country)

def process_disctricts(dfs, cdfs):
    for district in c('names.districts'):
        plot_overview(dfs['district-' + district], 'district', district)
        plot_stacked(dfs['district-' + district], 'district', district)
        plot_last_weeks_incidence(dfs['district-' + district], 'district', district)
        plot_absolute_comparism(cdfs['district-' + district], 'district',
                                'commune', district)
        plot_relative_comparism(cdfs['district-' + district], 'district',
                                'commune', district)
        plot_risc_comparism(cdfs['district-' + district], 'district',
                            'commune', district)

def process_communes(dfs, cdfs):
    for commune in c('names.communes'):
        plot_overview(dfs['commune-' + commune], 'commune', commune)
        plot_stacked(dfs['commune-' + commune], 'commune', commune)
        plot_parents_risc_comparism(dfs, commune)

def do():
    dfs = read_imported_dfs()
    cdfs = concat(dfs)
    process_countries(dfs, cdfs)
    process_disctricts(dfs, cdfs)
    process_communes(dfs, cdfs)
