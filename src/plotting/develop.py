from lib import read_imported_dfs
from plotting.prepare import concat
from plotting.types import map

def do():
    dfs = read_imported_dfs()
    cdfs = concat(dfs)
    map.plot(dfs['district-hoexter'], cdfs['district-hoexter'],
             'district', 'commune', 'hoexter')

do()