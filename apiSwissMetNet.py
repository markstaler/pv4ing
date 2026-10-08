# -*- coding: utf-8 -*-
"""
Messwerte von Bodenstationen über API
Doku: https://opendatadocs.meteoswiss.ch/a-data-groundbased/a1-automatic-weather-stations
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

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

# # Niederschlag
# years = sorted(df.index.year.unique())
# years = range(1997, 2027)

# colors = plt.cm.YlGn(np.linspace(0.35, 0.9, len(years)))

# plt.figure(figsize=(7, 12))

# for year, color in zip(years, colors):
#     prec = df.loc[df.index.year == year, 'rre150m0'].values

#     # Auf 12 Monate auffüllen
#     if len(prec) < 12:
#         prec = np.pad(prec, (0, 12 - len(prec)), constant_values=np.nan)

#     cum_prec = np.cumsum(prec)

#     plt.plot(np.arange(1, 13), cum_prec, color=color, linewidth=0.8)

#     # Jahreszahl direkt an das Ende der Linie
#     valid = ~np.isnan(cum_prec)

#     if valid.any():
#         last_x = np.where(valid)[0][-1] + 1
#         last_y = cum_prec[valid][-1]

#         plt.text(last_x + 0.1, last_y, str(year), color=color, fontsize=8, va='center')

# plt.xlabel('Monat')
# plt.ylabel('Jahresniederschlag [mm]')
# plt.title('Niederschlag')
# plt.xlim(1, 13)
# plt.grid(which='both', linestyle='--', alpha=0.4)

# plt.savefig('niederschlag.svg', bbox_inches='tight')
# plt.show()
