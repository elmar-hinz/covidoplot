import os
from pathlib import Path
my_directory = os.path.dirname(os.path.realpath(__file__)) + '/'

configuration = {
    'plurals': {
        'district': 'districts',
        'commune': 'communes',
        'country': 'countries',
    },
    'colors': {
        'red': 'firebrick',
        'blue': 'dodgerblue',
        'green': 'forestgreen',
        'black': 'black',
        'orange': 'orange',
    },
    'names': {
        'communes': {
            'bad-driburg': 'Bad Driburg',
            'brakel': 'Brakel',
            'borgentreich': 'Borgentreich',
            'beverungen': 'Beverungen',
            'hoexter': 'Höxter',
            'marienmuenster': 'Marienmünster',
            'nieheim': 'Nieheim',
            'steinheim': 'Steinheim',
            'warburg': 'Warburg',
            'willebadessen': 'Willebadessen'
        },
        'districts': {
            'hoexter': 'Kreis Höxter'
        },
        'countries': {
            'germany': {
                'german': 'Deutschland',
                'english': 'Germany',
                'jhu': 'Germany',
            },
            'italy': {
                'german': 'Italien',
                'english': 'Italy',
                'jhu': 'Italy',
            },
            'south-korea': {
                'german': 'Südkorea',
                'english': 'South Korea',
                'jhu': 'Korea, South',
            },
        }
    },
    'parents': {
        'communes': {
            'bad-driburg': 'hoexter',
            'brakel': 'hoexter',
            'borgentreich': 'hoexter',
            'beverungen': 'hoexter',
            'hoexter': 'hoexter',
            'marienmuenster': 'hoexter',
            'nieheim': 'hoexter',
            'steinheim': 'hoexter',
            'warburg': 'hoexter',
            'willebadessen': 'hoexter'
        },
    },
    'populations': {
        'communes': {
            'bad-driburg': 19000,
            'brakel': 16000,
            'borgentreich': 8500,
            'beverungen': 13000,
            'hoexter': 29000,
            'marienmuenster': 5000,
            'nieheim': 6000,
            'steinheim': 12500,
            'warburg': 23000,
            'willebadessen': 8000
        },
        'districts': {
            'hoexter': 140500,
        },
        'countries': {
            'germany': 83000000,
            'italy': 60000000,
            'france': 67000000,
            'spain': 47000000,
            'south-korea': 52000000,
        }
    },
    'directories': {
        'raw': {
            'districts': {
                'hoexter': my_directory + '../data/raw/kreis-hoexter/'
            },
        },
        'processed': my_directory + '../data/processed/',
        'published': {
            'plots': my_directory + '../../covidoplot-publisher/assets/plots/',
            'data': my_directory + '../../covidoplot-publisher/_data/'
        },
    },
    'files': {
        'jhu_confirmed': my_directory + '../data/raw/jhu/csse_covid_19_data' \
                                        '/csse_covid_19_time_series' \
                                        '/time_series_covid19_confirmed_global.csv',
        'jhu_deaths': my_directory + '../data/raw/jhu/csse_covid_19_data' \
                                     '/csse_covid_19_time_series' \
                                     '/time_series_covid19_deaths_global.csv',
        'jhu_recovered': my_directory + '../data/raw/jhu/csse_covid_19_data' \
                                        '/csse_covid_19_time_series' \
                                        '/time_series_covid19_recovered_global.csv',
        'raw': {
            'districts': {
                'hoexter': my_directory +
                           '../data/raw/kreis-hoexter/district-district.csv'
            }
        },
    }
}

def plural(key):
    return configuration['plurals'][key]

def get(key):
    keys = filter(None, key.split('.'))
    current = configuration
    for k in keys:
        current = current[k]
    return current

Path(get('directories.processed')).mkdir(parents=True, exist_ok=True)
Path(get('directories.published.plots')).mkdir(parents=True, exist_ok=True)
Path(get('directories.published.data')).mkdir(parents=True, exist_ok=True)
