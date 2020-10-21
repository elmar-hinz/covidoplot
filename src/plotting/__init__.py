from lib import read_imported_dfs
from plotting.prepare import concat
from plotting.entities import process_countries
from plotting.entities import process_disctricts
from plotting.entities import process_communes

def do():
    dfs = read_imported_dfs()
    cdfs = concat(dfs)
    process_countries(dfs, cdfs)
    process_disctricts(dfs, cdfs)
    process_communes(dfs, cdfs)

