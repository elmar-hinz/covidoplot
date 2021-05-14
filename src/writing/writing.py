from configuration import get as c
from lib import read_imported_dfs
import json


def write_configuration():
    path = c('directories.export.data') + 'configuration.json'
    with open(path, 'w') as outfile:
        json.dump(c(''), outfile)
    idents = c('names.communes')
    path = c('directories.export.data') + 'ident.json'
    with open(path, 'w') as outfile:
        json.dump(idents, outfile)


def write_dataframes(dataframes):
    for key, df in dataframes.items():
        path = c('directories.export.data') + key + '.json'
        df.to_json(path, orient='records', date_format='iso')
    key = 'district-hoexter-ages'
    path = c('directories.export.data') + key + '.json'
    df.to_json(path, orient='records', date_format='iso')

def do():
    write_configuration()
    write_dataframes(read_imported_dfs())
