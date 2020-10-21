from configuration import get as c
from plotting.types import risc_comparism
from plotting.types import last_weeks_incidence
from plotting.types import absolute_comparism
from plotting.types import parent_risc_comparism
from plotting.types import relative_comparism
from plotting.types import stacked
from plotting.types import overview
from plotting.types import map


def process_countries(dfs, cdfs):
    for country in c('names.countries'):
        overview.plot(dfs['country-' + country], 'country', country)
        stacked.plot(dfs['country-' + country], 'country', country)

def process_disctricts(dfs, cdfs):
    for district in c('names.districts'):
        overview.plot(dfs['district-' + district], 'district', district)
        stacked.plot(dfs['district-' + district], 'district', district)
        absolute_comparism.plot(cdfs['district-' + district], 'district',
                                'commune', district)
        relative_comparism.plot(cdfs['district-' + district], 'district',
                                'commune', district)
        risc_comparism.plot(cdfs['district-' + district], 'district',
                            'commune', district)
        last_weeks_incidence.plot(dfs['district-' + district], 'district',
                                  district)
        map.plot(cdfs['district-' + district], 'district', 'commune', district)

def process_communes(dfs, cdfs):
    for commune in c('names.communes'):
        overview.plot(dfs['commune-' + commune], 'commune', commune)
        stacked.plot(dfs['commune-' + commune], 'commune', commune)
        parent_risc_comparism.plot(dfs, commune)

