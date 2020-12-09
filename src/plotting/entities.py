from configuration import get as c
from plotting.types import parent_risc_comparism
from plotting.types import overview
from plotting.types import map
from .ComparisonSupervisor import ComparisonSupervisor
from .StackedSupervisor import StackedSupervisor
from .IncidenceSupervisor import IncidenceSupervisor
from .VerticalComparisonSupervisor import VerticalComparisonSupervisor


def process_countries(dfs, args):
    print('Argument List:', str(args))
    for country in c('names.countries'):
        overview.plot(dfs['country-' + country], 'country', country)
        StackedSupervisor(dfs, 'country', country).run()
        IncidenceSupervisor(dfs, 'country', country).run()

def process_disctricts(dfs, cdfs, args):
    print('Argument List:', str(args))
    for district in c('names.districts'):
        overview.plot(dfs['district-' + district], 'district', district)
        StackedSupervisor(dfs, 'district', district).run()
        ComparisonSupervisor(cdfs, 'confirmed', 'district', 'commune', district,
                             'Absolute Fallzahlen', 'absolute-comparison').run()
        ComparisonSupervisor(cdfs, 'density_of_cases', 'district', 'commune',
                             district, 'Relative Fallzahlen',
                             'relative-comparison').run()
        ComparisonSupervisor(cdfs, 'density_of_illness', 'district', 'commune',
                             district, 'Infektionsrisiko',
                             'risc-comparison').run()
        IncidenceSupervisor(dfs, 'district', district).run()
        map.plot(dfs['district-' + district], cdfs['district-' + district],
                 'district', 'commune', district)
        VerticalComparisonSupervisor(dfs, 'density_of_illness', 'district',
                                     district, 'Risikovergleich',
                                     'Aktiv Infizierte je 100.000 Einwohner',
                                     'vertical-risc-comparison').run()

def process_communes(dfs, args):
    print('Argument List:', str(args))
    if len(args) > 0:
        communes = args
    else:
        communes = c('names.communes')
    for commune in communes:
        # overview.plot(dfs['commune-' + commune], 'commune', commune)
        StackedSupervisor(dfs, 'commune', commune).run()
        IncidenceSupervisor(dfs, 'commune', commune).run()
        # parent_risc_comparism.plot(dfs, commune)
        VerticalComparisonSupervisor(dfs, 'density_of_illness', 'commune',
                                     commune, 'Risikovergleich',
                                     'Aktiv Infizierte je 100.000 Einwohner',
                                     'vertical-risc-comparison').run()

