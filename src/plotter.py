import matplotlib.pyplot as plt
import datetime
import csv
import json
import os
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import numpy as np
import time

config = {
    'name of district': 'Kreis Höxter',
    'population of district': 140500,
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
    'populations': {
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
    'source_path': '../data/cleaned/district-',
    'target_path_plots': '../../covidoplot-publisher/assets/plots/',
    'target_path_data': '../../covidoplot-publisher/_data/'
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
    def calc_table(rows, population):
        columns = {
            'date': [],
            'active cases': [],
            'recovered cases': [],
            'died cases': [],
            'cumulated cases': [],
            'relative cumulated cases': [],
            'relative active cases': [],
            'difference': [],
        }
        day_before = 0
        for row in rows:
            columns['date'].append(row['date'])
            columns['cumulated cases'].append(row['cumulated cases'])
            columns['recovered cases'].append(row['recovered cases'])
            columns['died cases'].append(row['died cases'])
            active_cases = int(
                row['cumulated cases']
                - row['recovered cases']
                - row['died cases'])
            columns['active cases'].append(active_cases)
            columns['relative cumulated cases'].append(
                row['cumulated cases'] / population * 100000)
            columns['relative active cases'].append(
                active_cases / population * 100000)
            columns['difference'].append( row['cumulated cases'] - day_before )
            day_before = row['cumulated cases']

        return columns

    data = {}
    data['district'] = calc_table(in_data['district'], config['population of district'])
    data['communes'] = {}
    for commune in config['communes']:
        data['communes'][commune] = calc_table(
            in_data['communes'][commune],
            config['populations'][commune]
        )
    return data

def write(data):
    def write(data, relative_directory, filename):
        directory = config['target_path_data'] + relative_directory
        path = directory + '/' + filename + '.json'
        try:
            os.mkdir(config['target_path_data'])
        except FileExistsError:
            pass

        try:
            os.mkdir(directory)
        except FileExistsError:
            pass

        with open(path, 'w') as outfile:
            json.dump(data, outfile)


    def prepare_data(data):
        prepared_data = []
        for i in range(len(data['date'])):
            prepared_data.append({
                'cumulated': data['cumulated cases'][i],
                'recovered': data['recovered cases'][i],
                'died': data['died cases'][i],
                'active': data['active cases'][i],
                'date': data['date'][i].strftime('%a %d.%m.'),
            })
        return prepared_data

    write(prepare_data(data['district']), '', 'hoexter-district')
    for key, title in config['communes'].items():
        write(prepare_data(data['communes'][key]), 'hoexter', key)

def plot(data):
    def write(title):
        try:
            os.mkdir(config['target_path_plots'])
        except FileExistsError:
            pass
        path = config['target_path_plots'] + title + '.png'
        plt.savefig(path)
        time.sleep(0.3)
        plt.clf()
        time.sleep(0.1)
        plt.close()
        time.sleep(0.1)


    def style(ax):
        majorDate = mdates.DateFormatter('%d.%m.')
        ax.xaxis.set_major_formatter(majorDate)
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3, linestyle='dashdot')

    def plot_summary(data, title):
        width = 0.66
        ylabel = 'bestätigte Fälle'
        xlabel = '2020'
        fig, ax = plt.subplots()
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        style(ax)
        ax.bar(
            data['date'],
            data['cumulated cases'],
            width,
            label='alle Fälle',
            color='dodgerblue',
        )
        ax.bar(
            data['date'],
            data['difference'],
            width,
            label='neue Fälle',
            color='orange',
        )
        ax.plot(
            data['date'],
            data['active cases'],
            label='erkrankt',
            color='firebrick'
        )
        ax.plot(
            data['date'],
            data['recovered cases'],
            label='wieder gesund',
            color='forestgreen'
        )
        ax.plot(
            data['date'],
            data['died cases'],
            label='verstorben',
            color='black'
        )
        ax.legend(loc='upper left')
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    def plot_stack(data, title):
        ylabel = 'bestätigte Fälle'
        xlabel = '2020'
        labels = ["erkrankt", "verstorben", "wieder gesund"]
        fig, ax = plt.subplots()
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        style(ax)
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

    def plot_compare_communes_relatively(communes, title):
        ylabel = 'bestätigte Fälle je 100.000 Einwohnern'
        xlabel = '2020'
        fig, ax = plt.subplots()
        style(ax)
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        for key, columns in communes.items():
            plt.plot(
                columns['date'],
                columns['relative cumulated cases'],
                '-',
                label=config['communes'][key])
        ax.legend(loc='upper left')
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    def plot_compare_communes_absolutely(communes, title):
        ylabel = 'bestätigte Fälle'
        xlabel = '2020'
        fig, ax = plt.subplots()
        style(ax)
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
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

    def plot_compare_communes_relatively_for_active_cases(communes, title):
        ylabel = 'aktive Fälle je 100.000 Einwohnern'
        xlabel = '2020'
        fig, ax = plt.subplots()
        style(ax)
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        for key, columns in communes.items():
            plt.plot(
                columns['date'],
                columns['relative active cases'],
                '-',
                label=config['communes'][key])
        ax.legend(loc='upper left')
        plt.title(title)
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    plot_summary(data['district'], config['name of district'])
    write('district-hoexter-summary')

    plot_stack(data['district'], config['name of district'])
    write('district-hoexter-stacked')

    plot_compare_communes_absolutely(
        data['communes'],
        'Bestätigte Fälle im ' + config['name of district'] + ' im absoluten '
                                                              'Vergleich'
    )
    write('district-hoexter-compared-communes-absolutely')
    plot_compare_communes_relatively(
        data['communes'],
        'Bestätigte Fälle im ' + config['name of district'] + ' im relativen '
                                                              'Vergleich'
    )
    write('district-hoexter-compared-communes-relatively')
    plot_compare_communes_relatively_for_active_cases(
        data['communes'],
        'Aktive Fälle im ' + config['name of district'] + ' im relativen '
                                                          'Vergleich'
    )
    write('district-hoexter-compared-communes-relatively-for-active-cases')
    for key, title in config['communes'].items():
        plot_stack(data['communes'][key], title)
        write(key + '-stacked')

data = calc(read())
write(data)
plot(data)
