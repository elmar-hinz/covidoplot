import os
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
blue = c('colors.blue')
green = c('colors.green')
orange = c('colors.orange')
red = c('colors.red')

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

dfs = read()
print(dfs.keys())

collect = []
collect.append(dfs['commune-brakel'])
collect.append(dfs['country-germany'])

df = pd.concat(collect, keys=['brakel', 'germany'], axis='columns')
print(df.dropna())

