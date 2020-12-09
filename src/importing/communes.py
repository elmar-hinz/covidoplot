import pandas as pd
from configuration import get as c
from importing.commons import shorten_df
from importing.commons import process_manual_data
from lib import write_imported_dataframe


def load(district, commune):
    path = c('directories.raw.districts')[district]
    path += 'district-' + commune + '.csv'
    return pd.read_csv(path, sep=';')


def run():
    for key, name in c('names.communes').items():
        df = load('hoexter', key)
        df = shorten_df(df)
        df = process_manual_data(df, 'commune', key)
        write_imported_dataframe(df, 'commune-' + key)
