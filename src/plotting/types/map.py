import geopandas
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from configuration import get as c
from configuration import plural as p
from .lib.commons import save, mapsize
from .lib.colors import green, yellow, red, darkgreen

colors = [darkgreen, green, yellow, red]
cmap = ListedColormap(colors)
bins = [0, 35, 50]

def get_color(value):
    if value is None:
        return 'grey'
    color = colors[0]
    for i in range(len(bins)):
        if( value > bins[i]):
            color = colors[i + 1]
        else:
            break
    return color


# For now this is hardcoded to Kreis Höxter
# May be extended to extract district maps from
# a common shapefile by district name.
def plot(district_df, cdf, type, child_type, key):

    # load data
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
    meta = district_df[district_df['date'] == date]
    if meta['STI-LZG'].notnull().bool():
        total_incidence = meta['STI-LZG']
        total_incidence_source = 'LZG NRW, amtlich'
    elif meta['STI-RKI'].notnull().bool():
        total_incidence = meta['STI-RKI']
        total_incidence_source = 'RKI, vorläufig'
    elif meta['STI-Kreis'].notnull().bool():
        total_incidence = meta['STI-Kreis']
        total_incidence_source = 'Kreis, vorläufig'
    else:
        total_incidence = None
    if total_incidence is not None:
        total_incidence = float(total_incidence)

    # load map
    file = c('files.shapefile')
    communes = geopandas.read_file(file)
    communes['Name'] = communes['GN']

    # create layer dataframes
    communes = communes.set_index('GN').join(df.set_index('commune'))
    communes['helper'] = 0
    district = communes.dissolve(by='helper')
    shadow = district.copy()
    shadow = shadow.translate(xoff=7000, yoff=2000)

    # create figure objects
    figure = plt.figure()
    axes = plt.axes()

    # start plotting

    # shadow
    if total_incidence is not None:
        shadow.plot(
            color=get_color(total_incidence),
            ax=axes,
            alpha=0.3,
        )
        shadow.boundary.plot(ax=axes, color='#aaa', linewidth=0.1)

    # communes
    district.plot(ax=axes, color='white')  # white background for alpha
    communes.plot(
        ax=axes,
        column='last_weeks_incidence',
        legend=False,
        scheme="user_defined",
        cmap=cmap,
        classification_kwds={'bins': [0, 35, 50]},
        alpha=0.88,
    )
    district.boundary.plot(ax=axes, color='#ddd', linewidth=0.3)

    # style
    figure.set_size_inches(mapsize)
    if total_incidence is not None:
        bbox_props = dict(boxstyle="round,pad=0.45",
                          fc="white",
                          # ec="black",
                          ec=get_color(total_incidence),
                          lw=0.3,
                          alpha=0.7
                          )
        plt.annotate(
            ('Kreis Höxter: ' +
             str(total_incidence).replace('.', ',') +
             ' (' + total_incidence_source + ')'),
            xy=(0.65, 0.78),
            xycoords='figure fraction',
            ha='center',
            bbox=bbox_props,
            size=10.5,
            color='#666',
            #color=get_color(total_incidence),
            fontfamily='sans-serif',
            fontweight='bold',
            fontstyle='italic',
        )

    bbox_props = dict(boxstyle="round,pad=0.35",
                      fc="#484848", ec="white",
                      lw=0.2, alpha=1)
    communes.apply(
        lambda x: axes.annotate(
            # ugly, but works for now
            text=x.Name + ': ' + str(x.last_weeks_incidence).replace('.', ','),
            size=9.5,
            xy=x.geometry.centroid.coords[0],
            ha='center',
            bbox=bbox_props,
            color='white',
            fontfamily='sans-serif',
            fontweight='bold',
            fontstyle='italic',
        ),
        axis=1)
    plt.suptitle('7-Tage-Inzidenzen im Kreis Höxter', fontsize=18)
    day = date.strftime("%d.%m.%Y")
    axes.set_title(label='je 100.000 Einwohnern am ' + day, fontsize=16)
    plt.axis('off')

    # go
    save(type, key,  'last_weeks_incidence-map')
