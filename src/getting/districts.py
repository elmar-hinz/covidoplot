import pandas as pd
from configuration import get as c
from getting.commons import write_dataframe, process_manual_data


def load(district):
    path = c('files.raw.districts')[district]
    return pd.read_csv(path, sep=';')


def run():

    for key, name in c('names.districts').items():
        df = load(key)
        df = process_manual_data(df, 'district', key)
        write_dataframe(df, 'district-' + key)
