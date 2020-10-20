import pandas as pd
from configuration import get as c
from getting.commons import write_dataframe, process_manual_data


def load(district, commune):
    path = c('directories.raw.districts')[district]
    path += 'district-' + commune + '.csv'
    return pd.read_csv(path, sep=';')


def run():
    for key, name in c('names.communes').items():
        df = load('hoexter', key)
        df = process_manual_data(df, 'commune', key)
        write_dataframe(df, 'commune-' + key)
