from lib import read_imported_dfs
from plotting.prepare import concat
from plotting.entities import process_countries
from plotting.entities import process_disctricts
from plotting.entities import process_communes
from plotting.entities import process_ages

def do(args):
    print('Argument List:', str(args))
    dfs = read_imported_dfs()
    if len(args) == 0 or args[0] == 'countries':
        process_countries(dfs, args[1:])
    if len(args) == 0 or args[0] == 'districts':
        cdfs = concat(dfs)
        process_disctricts(dfs, cdfs, args[1:])
    if len(args) == 0 or args[0] == 'communes':
        process_communes(dfs, args[1:])
    if len(args) == 0 or args[0] == 'ages':
        process_ages(dfs, args[1:])

