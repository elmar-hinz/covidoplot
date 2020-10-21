import pandas as pd
from configuration import get as c
from importing.commons import process_entity
from lib import write_imported_dataframe

def load_jhu_data():
    df_confirmed = pd.read_csv(c('files.jhu_confirmed'))
    df_deaths = pd.read_csv(c('files.jhu_deaths'))
    df_recovered = pd.read_csv(c('files.jhu_recovered'))
    return df_confirmed, df_deaths, df_recovered


def process_jhu_data(df_confirmed, df_deaths, df_recovered, country, key):
    def date(row):
        return pd.to_datetime(row.date, format='%m/%d/%y')

    dfc = df_confirmed[df_confirmed['Country/Region'] == country]
    dfr = df_recovered[df_recovered['Country/Region'] == country]
    dfd = df_deaths[df_deaths['Country/Region'] == country]
    sc = dfc.iloc[:, 4:]
    sr = dfr.iloc[:, 4:]
    sd = dfd.iloc[:, 4:]
    df = pd.concat([sc, sr, sd], ignore_index=True) \
        .rename(index={0: 'confirmed', 1: 'recovered', 2: 'dead'}) \
        .transpose().reset_index().rename(columns={'index': 'date'})
    df['date'] = df.apply(date, axis=1)
    process_entity(df, 'country', key)
    return df

def run():
    dfs = load_jhu_data()

    for key, names in c('names.countries').items():
        df = process_jhu_data(*dfs, country=names['jhu'], key=key)
        write_imported_dataframe(df, 'country-' + key)

