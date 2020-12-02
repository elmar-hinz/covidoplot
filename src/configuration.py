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
        'white': 'snow',
        'grey': 'lightslategrey',
        'black': 'black',
        'red': 'firebrick',
        'darkred': '#800000',
        'darkerred': '#600000',
        'pink': 'deeppink',
        'orange': 'coral',
        'yellow': 'gold',
        'lightgreen': 'greenyellow',
        'green': 'forestgreen',
        'darkgreen': 'darkgreen',
        'blue': 'cornflowerblue',
        'darkblue': 'navy',
        'purple': 'purple',
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
        # 31.12.2019: https://www.it.nrw/statistik/eckdaten/bevoelkerung-nach-gemeinden-93051?fbclid=IwAR1SODPI0V5GuLr73CwuUO-MVdGjZlIm4Ce5eln3Enyc42yuKXUOVETT9r4
        'communes': {
            'bad-driburg': 18959,
            'brakel': 16137,
            'borgentreich': 8543,
            'beverungen': 13103,
            'hoexter': 28808,
            'marienmuenster': 4902,
            'nieheim': 6084,
            'steinheim': 12528,
            'warburg': 23076,
            'willebadessen': 8111
        },
        'districts': {
            # 31.12.2019: https://www.it.nrw/statistik/eckdaten/bevoelkerung-nach-gemeinden-93051?fbclid=IwAR1SODPI0V5GuLr73CwuUO-MVdGjZlIm4Ce5eln3Enyc42yuKXUOVETT9r4
            'hoexter': 140251,
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
        'imported': my_directory + '../data/imported/',
        # 'processed': my_directory + '../data/processed/',
        'export': {
            'plots': my_directory + '../data/export/plots/',
            'data': my_directory + '../data/export/data/',
        },
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
        'shapefile': 'zip:///' + my_directory + '../data/district-hoexter.shp.zip',
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


Path(get('directories.imported')).mkdir(parents=True, exist_ok=True)
Path(get('directories.export.plots')).mkdir(parents=True, exist_ok=True)
Path(get('directories.export.data')).mkdir(parents=True, exist_ok=True)
Path(get('directories.published.plots')).mkdir(parents=True, exist_ok=True)
Path(get('directories.published.data')).mkdir(parents=True, exist_ok=True)
