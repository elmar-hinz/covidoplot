import geopandas
import pandas as pd
import matplotlib.pyplot as plt
from configuration import get as c
from configuration import plural as p
from .lib.commons import save

# For now this is hardcoded to Kreis Höxter
# May be extended to extract district maps from
# a common shapefile by district name.
def plot(cdf, type, child_type, key):

    # load date
    def get_latest_incidences():
        incidences = list()
        for k, v in c('names')[p(child_type)].items():
            incidences.append((v, cdf.loc[(k, 'last_weeks_incidence')][-1]))
        return incidences

    df = pd.DataFrame(
        columns=['commune', 'last_weeks_incidence'],
        data=get_latest_incidences(),
    )
    df['last_weeks_incidence'] = round(df['last_weeks_incidence'], 1)
    date = cdf.keys()[-1]  # last date

    # load map
    file = c('files.shapefile')
    geoframe = geopandas.read_file(file)
    geoframe['Name'] = geoframe['GN']

    # join
    geoframe = geoframe.set_index('GN').join(df.set_index('commune'))

    # figure
    figure = plt.figure()
    axes = plt.axes()
    geoframe.plot(
        ax=axes,
        column='last_weeks_incidence',
        legend=False,
        scheme="quantiles",
        cmap='OrRd',
    )

    # style
    figure.set_size_inches(9, 9)
    bbox_props = dict(boxstyle="round,pad=0.3", fc="white", ec="#111", lw=0.1)
    geoframe.apply(
        lambda x: axes.annotate(
            text=x.Name + ': ' + str(x.last_weeks_incidence),
            xy=x.geometry.centroid.coords[0],
            ha='center',
            bbox=bbox_props,
            color='#111',
            fontfamily='sans-serif',
        ),
        axis=1)
    plt.suptitle('7-Tage-Inzidenzen im Kreis Höxter', fontsize=18)
    day = date.strftime("%d.%m.%Y")
    axes.set_title(label='je 100.000 Einwohnern am ' + day, fontsize=16)
    plt.axis('off')

    # go
    save(type, key,  'last_weeks_incidence-map')
