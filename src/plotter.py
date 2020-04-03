import matplotlib.pyplot as plt
import datetime
import csv
import os
import matplotlib.dates as mdates
import numpy as np

config = {
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
    'source_path': '../data/cleaned/district-',
    'target_path': '../../covidoplot-publisher/assets/plots/'
}


def read():
    def read_file(path):
        data = []
        with open(path, 'r') as csvfile:
            table = csv.reader(csvfile, delimiter=';')
            next(table)  # headers
            for row in table:
                day = {}
                day['date'] = datetime.datetime.strptime(row[0], '%d.%m.%Y')
                day['cumulated cases'] = int(row[1])
                day['recovered cases'] = int(row[2])
                day['died cases'] = int(row[3])
                data.append(day)
        return data

    data = {}
    data['communes'] = {}
    for commune in config['communes']:
        path = config['source_path'] + commune + '.csv'
        data['communes'][commune] = read_file(path)
    path = config['source_path'] + 'district' + '.csv'
    data['district'] = read_file(path)
    return data

def calc(in_data):
    def calc_table(rows):
        columns = {
            'date': [],
            'active cases': [],
            'recovered cases': [],
            'died cases': [],
            'cumulated cases': [],
            'percent since one day': [],
        }
        for row in rows:
            columns['date'].append(row['date'])
            columns['cumulated cases'].append(row['cumulated cases'])
            columns['recovered cases'].append(row['recovered cases'])
            columns['died cases'].append(row['died cases'])
            columns['active cases'].append(row['cumulated cases'] - row['recovered cases'])
            columns['percent since one day'].append(np.nan)

        return columns

    data = {}
    data['district'] = calc_table(in_data['district'])
    data['communes'] = {}
    for commune in config['communes']:
        data['communes'][commune] = calc_table(in_data['communes'][commune])
    return data


def plot(data):
    def write(title):
        try:
            os.mkdir(config['target_path'])
        except FileExistsError:
            pass
        path = config['target_path'] + title + '.png'
        plt.savefig(path)
        plt.close()

    def format_dates(ax):
        majorDate = mdates.DateFormatter('%d.%m.')
        ax.xaxis.set_major_formatter(majorDate)
        plt.xticks(rotation=45)

    def plot_stack(data, title):
        ylabel = 'bestätigte Fälle'
        xlabel = '2020'
        labels = ["Aktive Fälle", "Verstorbene Fälle", "Genesene Fälle"]
        fig, ax = plt.subplots()
        format_dates(ax)
        ax.stackplot(
            data['date'],
            data['active cases'],
            data['died cases'],
            data['recovered cases'],
            labels=labels)
        ax.legend(loc='upper left')
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    def plot_compare_communes(communes, title):
        ylabel = 'bestätigte Fälle'
        xlabel = '2020'
        fig, ax = plt.subplots()
        format_dates(ax)
        for key, columns in communes.items():
            plt.plot(
                columns['date'],
                columns['cumulated cases'],
                '-',
                label=config['communes'][key])
        ax.legend(loc='upper left')
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    plot_stack(data['district'], 'Kreis Höxter')
    write('district-hoexter-stacked')
    plot_compare_communes(data['communes'], 'Gemeinden im Kreis Höxter')
    write('district-hoexter-compared-communes')
    for key, title in config['communes'].items():
        plot_stack(data['communes'][key], title)
        write(key + '-stacked')

data = calc(read())
plot(data)
