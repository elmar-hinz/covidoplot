import pandas as pd
# noinspection PyUnresolvedReferences
from configuration import get as c
# noinspection PyUnresolvedReferences
from configuration import plural as p

lakh = 10**5

def load_jhu_data():
    df_confirmed = pd.read_csv(c('files.jhu_confirmed'))
    df_deaths = pd.read_csv(c('files.jhu_deaths'))
    df_recovered = pd.read_csv(c('files.jhu_recovered'))
    return (df_confirmed, df_deaths, df_recovered)

def load_commune(district, commune):
    path = c('directories.raw.districts')[district]
    path += 'district-' + commune + '.csv'
    return pd.read_csv(path, sep=';')

def load_district(district):
    path = c('files.raw.districts')[district]
    return pd.read_csv(path, sep=';')

def process_common(df, type, key):

    def new_cases(df):
        df['new'] = 0
        df.loc[0, 'new'] = df.loc[0, 'confirmed']
        for i in range(1, len(df)):
            df.loc[i, 'new'] = df.loc[i, 'confirmed'] - df.loc[i - 1,
                                                               'confirmed']
    def last_weeks_incidence(df):
        def f(row):
            r = lakh * row.last_weeks_incidence / c('populations')[p(type)][key]
            return round(r, 3)
        df['last_weeks_incidence'] = df['new'].rolling(min_periods=1,
                                                   window=7).sum()
        df['last_weeks_incidence'] = df.apply(f, axis=1)

    def ill(row):
        return row.confirmed - row.recovered - row.dead

    def density_of_cases(row):
        r = lakh * row.confirmed / c('populations')[p(type)][key]
        return round(r, 3)

    def density_of_illness(row):
        r = lakh * row.ill / c('populations')[p(type)][key]
        return round(r, 3)

    def density_of_death(row):
        r = lakh * row.dead / c('populations')[p(type)][key]
        return round(r, 3)

    def density_of_recoverance(row):
        r = lakh * row.recovered / c('populations')[p(type)][key]
        return round(r, 3)

    df['ill'] = df.apply(ill, axis=1)
    new_cases(df)
    last_weeks_incidence(df)
    df['density_of_cases'] = df.apply(density_of_cases, axis=1)
    df['density_of_illness'] = df.apply(density_of_illness, axis=1)
    df['density_of_death'] = df.apply(density_of_death, axis=1)
    df['density_of_recoverance'] = df.apply(density_of_recoverance, axis=1)


def process_jhu_data(df_confirmed, df_deaths, df_recovered, country, key):
    def date(row):
        return pd.to_datetime(row.date, format='%m/%d/%y')

    dfc = df_confirmed[df_confirmed['Country/Region'] == country]
    dfr = df_recovered[df_recovered['Country/Region'] == country]
    dfd = df_deaths[df_deaths['Country/Region'] == country]
    sc = dfc.iloc[:,4:]
    sr = dfr.iloc[:,4:]
    sd = dfd.iloc[:,4:]
    df = pd.concat([sc, sr, sd], ignore_index=True) \
        .rename(index={0: 'confirmed', 1: 'recovered', 2: 'dead'}) \
        .transpose().reset_index().rename(columns={'index': 'date'})
    df['date'] = df.apply(date, axis=1)
    process_common(df, 'country', key)
    return df

def process_manual_data(df, type, key):
    def date(row):
        return pd.to_datetime(row.date, format='%d.%m.%Y')

    df.rename(columns={'Datum': 'date', 'Fälle': 'confirmed', 'Genesungen':
        'recovered', 'Verstorbene': 'dead'}, inplace=True)
    df['date'] = df.apply(date, axis=1)
    process_common(df, type, key)
    return df

def write_dataframe(df, filename_trunk):
    file = c('directories.processed') + filename_trunk + '.csv'
    df.to_csv(file, index=False)

dfs = load_jhu_data()

for key, names in c('names.countries').items():
    df = process_jhu_data(*dfs, country=names['jhu'], key=key)
    write_dataframe(df, 'country-' + key)

for key, name in c('names.districts').items():
    df = load_district(key)
    df = process_manual_data(df, 'district', key)
    write_dataframe(df, 'district-' + key)

for key, name in c('names.communes').items():
    df = load_commune('hoexter', key)
    df = process_manual_data(df, 'commune', key)
    write_dataframe(df, 'commune-' + key)

