from urllib.request import urlopen
import geopandas
import pandas as pd
from configuration import get as c
import pathlib
import datetime
from lib import write_imported_dataframe

cache = c('files.cache.rki_kreis_hoexter')

url = "https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services" \
      "/RKI_COVID19/FeatureServer/0/query?where=IdLandkreis%20%3D%20'05762" \
      "'&outFields=IdBundesland,Bundesland,Landkreis,Altersgruppe," \
      "Geschlecht,AnzahlFall,AnzahlTodesfall,ObjectId,Meldedatum," \
      "IdLandkreis,Datenstand,NeuerFall,NeuerTodesfall,Refdatum,NeuGenesen," \
      "AnzahlGenesen,IstErkrankungsbeginn&returnGeometry=false&outSR=4326&f" \
      "=json"

data_download_interval_in_minutes = 600

def load():

    def download():
        with urlopen(url) as reader:
            content = reader.read().decode('utf-8')
            with open(cache, 'w') as writer:
                writer.write(content)

    def read_df():
        data = geopandas.read_file(cache)
        data['Refdatum'] = pd.to_datetime(data['Refdatum'], unit='ms')
        data['Meldedatum'] = pd.to_datetime(data['Meldedatum'], unit='ms')
        return data

    try:
        mtime = pathlib.Path(cache).stat().st_mtime
        last = datetime.datetime.fromtimestamp(mtime)
        now = datetime.datetime.now()
        if (now - last) > datetime.timedelta(
                minutes=data_download_interval_in_minutes):
            download()
    except Exception as e:
        print('did not exist')
        download()
    finally:
        return read_df()

def calc(hx):
    collection = pd.DataFrame(columns=[
        'Jahr', 'Monat', 'Altersgruppe', 'Anzahl'])
    for year in range(2020, 2023):
        for month in range(1, 13):
            m = hx[(hx['Refdatum'].dt.month == month)
                   & (hx['Refdatum'].dt.year == year)]
            x = m.groupby(['Altersgruppe', 'AnzahlFall']).size().reset_index(
                name='size')
            y = x['AnzahlFall'] * x['size']
            x['product'] = x['AnzahlFall'] * x['size']
            ages = x.groupby(['Altersgruppe'])['product'].agg(
                Anzahl='sum').reset_index()
            ages = ages[ages['Altersgruppe'] != 'unbekannt']
            ages['Jahr'] = year
            ages['Monat'] = month
            collection = pd.concat([collection, ages])
    return collection

def run():
    data = load()
    collection = calc(data)
    write_imported_dataframe(collection, 'district-hoexter-ages')
