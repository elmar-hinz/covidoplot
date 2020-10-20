from configuration import get as c
from configuration import plural as p
import pandas as pd

lakh = 10**5

def process_entity(df, type, key):

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

def process_manual_data(df, type, key):
    def date(row):
        return pd.to_datetime(row.date, format='%d.%m.%Y')

    df.rename(columns={'Datum': 'date', 'Fälle': 'confirmed', 'Genesungen':
        'recovered', 'Verstorbene': 'dead'}, inplace=True)
    df['date'] = df.apply(date, axis=1)
    process_entity(df, type, key)
    return df

def write_dataframe(df, filename_trunk):
    file = c('directories.processed') + filename_trunk + '.csv'
    df.to_csv(file, index=False)


