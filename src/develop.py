from lib import read_imported_dfs
from plotting.prepare import concat
from plotting.types import map
from plotting.StackedSupervisor import StackedSupervisor
from plotting.IncidenceSupervisor import IncidenceSupervisor
from plotting.ComparisonSupervisor import ComparisonSupervisor

def do():
    dfs = read_imported_dfs()
    cdfs = concat(dfs)
    # IncidenceSupervisor(dfs, 'district', 'hoexter').run()
    # StackedSupervisor(dfs, 'commune', 'bad-driburg').run()
    # ComparisonSupervisor(cdfs, 'ill', 'district', 'commune', 'hoexter',
    # 'Absolute Fallzahlen', 'absolute-comparison').run()

do()