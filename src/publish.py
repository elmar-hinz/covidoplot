import time
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import json
# noinspection PyUnresolvedReferences
from configuration import configuration as config
# noinspection PyUnresolvedReferences
from configuration import plural as p
# noinspection PyUnresolvedReferences
from configuration import get as c

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
label_illness_density = 'Erkrankte je 100.000 Einwohner'
label_confirmed = 'bestätigte Fälle'
label_last_weeks_incidence = 'neue Fälle je 100.000 Einwohner'
title_last_weeks_incidence = '7-Tage-Inzidenz '
label_red_line = 'rote Line = 50'
label_yellow_line = 'gelbe Berliner Line = 20'

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

def write(dataframes):
    for key, df in dataframes.items():
        path = config['directories']['published']['data'] + key + '.json'
        df.to_json(path, orient='records', date_format='iso')

def write_configuration():
    path = c('directories.published.data') + 'configuration.json'
    with open(path, 'w') as outfile:
        json.dump(c(''), outfile)
    idents = c('names.communes')
    path = c('directories.published.data') + 'ident.json'
    with open(path, 'w') as outfile:
        json.dump(idents, outfile)

def save(type, key, title):
    name = type + '-' + key + '-' + title + '.png'
    path = config['directories']['published']['plots'] + name
    plt.savefig(path)
    time.sleep(0.3)
    plt.clf()
    time.sleep(0.1)
    plt.close()
    time.sleep(0.1)

def read():
    dfs = {}

    def read_csv(name):
        try:
            df = pd.read_csv(c('directories.processed') + name + '.csv',
                             parse_dates=['date'])
            df.set_index('date', drop=False, inplace=True)
            dfs[name] = df
        except FileNotFoundError:
            print('missing: ' + name)

    for key in c('names.communes'):
        read_csv('commune-' + key)

    for key in c('names.districts'):
        read_csv('district-' + key)

    for key in c('names.countries'):
        read_csv('country-' + key)

    return dfs

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
    _, ax = plt.subplots()
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
    _, ax = plt.subplots()
    style(ax)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.bar(df.date, df.confirmed, width, label='alle Fälle', color=blue)
    ax.bar(df.date, df.new, width, label='neue Fälle', color=orange)
    ax.plot(df.date, df.ill, label='erkrankt', color=red)
    ax.plot(df.date, df.recovered, label='wieder gesund', color=darkgreen)
    ax.plot(df.date, df.dead, label='verstorben', color=black)
    ax.legend(loc='upper left')
    plt.title('Übersicht: ' + title(type, key))
    plt.ylabel(label_confirmed)
    save(type, key, 'overview')

def plot_last_weeks_incidence(df, type, key):
    _, ax = plt.subplots()
    style(ax)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.plot(df.date, df.last_weeks_incidence, label='7-Tage-Inzidenz',
            color=blue)
    plt.axhline(50, color=red, label=label_red_line)
    plt.axhline(20, color=yellow, label=label_yellow_line)
    plt.title(title_last_weeks_incidence + title(type, key))
    plt.ylabel(label_last_weeks_incidence)
    ax.legend(loc='upper left')
    save(type, key, 'last_weeks_incidence')

def plot_stacked(df, type, key):
    # df = import_dates(df)
    _, ax = plt.subplots()
    style(ax)
    ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.stackplot(df.date,
                 df.ill, df.recovered, df.dead,
                 labels=['erkrankt', 'wieder gesund', 'verstorben'],
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
              'Italien']
    frames=[]
    frames.append(dfs['commune-' + commune][field])
    frames.append(dfs['district-hoexter'][field])
    frames.append(dfs['country-germany'][field])
    frames.append(dfs['country-italy'][field])
    df = pd.concat(frames, axis=1).dropna()
    _, ax = plt.subplots()
    style(ax)
    ax.plot(df)
    plt.legend(labels=labels)
    plt.ylabel(label_illness_density)
    save('commune', commune, 'upwards-risc-comparism')

def process_countries(dfs, cdfs):
    for country in config['names']['countries']:
        plot_overview(dfs['country-' + country], 'country', country)
        plot_stacked(dfs['country-' + country], 'country', country)

def process_disctricts(dfs, cdfs):
    for district in config['names']['districts']:
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
    for commune in config['names']['communes']:
        plot_overview(dfs['commune-' + commune], 'commune', commune)
        plot_stacked(dfs['commune-' + commune], 'commune', commune)
        plot_parents_risc_comparism(dfs, commune)

dfs = read()
cdfs = concat(dfs)
write_configuration()
write(dfs)
process_countries(dfs, cdfs)
process_disctricts(dfs, cdfs)
process_communes(dfs, cdfs)
