import matplotlib.pyplot as plt
import csv
import datetime

ylabel = 'bestätigte Fälle'
xlabel = '2020'

with open('../data/cleaned/Covid-19-Kreis Höxter.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=';')
    title = next(plots)[0]
    next(plots)                                                        # headers
    rows = []
    for row in plots:
        data = {}
        data['date'] = datetime.datetime.strptime(row[0], '%d.%m.%Y')
        data['cumulated cases'] = row[1]
        data['recovered cases'] = row[2]
        data['current cases'] = row[3]
        rows.append(data)

x = []
cumulated = []
current = []
recovered = []
for data in rows:
    x.append(data['date'].strftime('%d.%m.'))
    cumulated.append(int(data['cumulated cases']))
    current.append((int(data['current cases'])))
    recovered.append((int(data['recovered cases'])))

plt.grid(axis='y', alpha=0.4)
plt.title(title)
plt.plot(x, current, 'o--', label='aktive', color='darkred')
plt.plot(x, cumulated, 'o-', label='alle', color='darkred')
plt.plot(x, recovered, 'o-', label='genesen', color='gray')
plt.legend(title='bestätigte Fälle:')
plt.ylabel(ylabel)
plt.xlabel(xlabel)
plt.show()

