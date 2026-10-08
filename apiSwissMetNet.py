# -*- coding: utf-8 -*-
"""
Messwerte von Bodenstationen über API
Doku: https://opendatadocs.meteoswiss.ch/a-data-groundbased/a1-automatic-weather-stations
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

cos  = lambda arg : np.cos(np.deg2rad(arg))
sin  = lambda arg : np.sin(np.deg2rad(arg))
acos = lambda arg : np.rad2deg(np.arccos(arg))
asin = lambda arg : np.rad2deg(np.arcsin(arg))

# ### API-Abfrage SwissMetNet
s = 'vad' # Stationsname siehe nachfolgende Liste
url = 'https://raw.githubusercontent.com/markstaler/pv4ing/master/diffStationen.csv'
stat = pd.read_csv(url, sep=';',encoding='utf-8')
bg = stat.loc[stat["Abk"] == s, "Breitengrad"].iloc[0]
lg = stat.loc[stat["Abk"] == s, "Längengrad"].iloc[0]

## Abfrage aller Parameter einer Messstation mit Monatsauflösung
url = 'https://data.geo.admin.ch/ch.meteoschweiz.ogd-smn/' + str(s) + '/ogd-smn_' + str(s) +\
    '_t_historical_2020-2029.csv' # 10-Minutenauflösung
    # '_m.csv' # Beispiel Monatsauflösung

# Laden der csv-Datei mit allen Parametern
df = pd.read_csv(url, delimiter=';')
df['tutc'] = pd.to_datetime(df["reference_timestamp"], format="%d.%m.%Y %H:%M")
df = df.set_index('tutc')  # relevant für resample

## Parameterliste: https://data.geo.admin.ch/ch.meteoschweiz.ogd-smn/ogd-smn_meta_parameters.csv
nied = df['rre150z0'].values # [mm/10min] Niederschlag 10-Min-Auflösung bei _t_hist...
t2m  = df['tre200s0'].values # [°C] Temperatur 10-Min-Auflösung bei _t_hist... 
hGlo = df['gre000z0'].values # [W/m2] Globalstrahlung 10-Min-Auflösung bei _t_hist...
hDif = df['ods000z0'].values # [W/m2] Diffusstrahlung 10-Min-Auflösung bei _t_hist...
# nied = df['rre150m0'].values # [mm/Monat] Niederschlag Monatsauflösung bei _m.csv

print(df)
list(df)
plt.plot(df.index,nied)