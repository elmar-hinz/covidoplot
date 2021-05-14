import pandas as pd
import matplotlib.pyplot as plt
from configuration import get as c
from plotting.types import map
from .ComparisonSupervisor import ComparisonSupervisor
from .StackedSupervisor import StackedSupervisor
from .IncidenceSupervisor import IncidenceSupervisor
from .VerticalComparisonSupervisor import VerticalComparisonSupervisor
from .types.AgesPlotter import AgesPlotter
import os

if not os.environ.get('PRODUCTION'):
    counts = [31]
else:
    counts = [9999, 370, 100, 33, 7]

def process_countries(dfs, args):
    print('Countries argument list:', str(args))
    for country in c('names.countries'):
        for count in counts:
            StackedSupervisor(dfs, count, 'country', country).run()
            IncidenceSupervisor(dfs, count, 'country', country).run()

def process_disctricts(dfs, cdfs, args):
    print('Districts argument list:', str(args))
    for district in c('names.districts'):
        map.plot(dfs['district-' + district], cdfs['district-' + district],
                 'district', 'commune', district)
        for count in counts:
            StackedSupervisor(dfs, count, 'district', district).run()
            ComparisonSupervisor(cdfs, count, 'confirmed', 'district', 'commune', district,
                                 'Absolute Fallzahlen', 'absolute-comparison').run()
            ComparisonSupervisor(cdfs, count, 'density_of_cases', 'district', 'commune',
                                 district, 'Relative Fallzahlen',
                                 'relative-comparison').run()
            ComparisonSupervisor(cdfs, count, 'density_of_illness', 'district', 'commune',
                                 district, 'Infektionsrisiko',
                                 'risc-comparison').run()
            ComparisonSupervisor(cdfs, count, 'last_weeks_incidence',
                                 'district', 'commune',
                                 district, 'Wocheninzidenzen',
                                 'incidence-comparison').run()
            IncidenceSupervisor(dfs, count, 'district', district).run()
            VerticalComparisonSupervisor(dfs, count, 'last_weeks_incidence',
                                         'district',
                                         district, 'Risikovergleich',
                                         # 'Aktiv Infizierte je 100.000 Einwohner',
                                         'Wocheninzidenz',
                                         'vertical-risc-comparison').run()

def process_communes(dfs, args):
    print('Communes argument List:', str(args))
    if len(args) > 0:
        communes = args
    else:
        communes = c('names.communes')
    for commune in communes:
        for count in counts:
            StackedSupervisor(dfs, count, 'commune', commune).run()
            IncidenceSupervisor(dfs, count, 'commune', commune).run()
            VerticalComparisonSupervisor(dfs, count, 'last_weeks_incidence',
                                         'commune',
                                         commune, 'Risikovergleich',
                                         'Wocheninzidenz',
                                         'vertical-risc-comparison').run()
def process_ages(dfs, args):
    print('Ages argument List:', str(args))
    ages = dfs['district-hoexter-ages']
    for key, group in ages.groupby(['Jahr', 'Monat']):
        AgesPlotter(group).run()
        name = 'district-hoexter-ages-' \
               + str(key[0]) + '-' + str(key[1]) + '.png'
        path = c('directories.export.plots') + name
        plt.savefig(path)
        plt.close()


