# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 17:14:42 2021

@author: mark
"""
import datetime as dt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

lg = 9.4727 # [grad] Längengrad
bg = 47.1733 # [grad] Breitengrad

cos  = lambda arg : np.cos(np.deg2rad(arg))
sin  = lambda arg : np.sin(np.deg2rad(arg))
acos = lambda arg : np.rad2deg(np.arccos(arg))
asin = lambda arg : np.rad2deg(np.arcsin(arg))


## Daten importieren
df = pd.read_csv('2017_DataExport15min.csv', delimiter=';', decimal='.', header = 0)
df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S' ) 
df = df.set_index(['Time']) # Datetime als Index definieren
df = df.resample('30T').mean() # Die Daten werden "resampled" zu 30 min Werte

hGlo  = df['hGlo'].values    # [W/m2] 
hDif  = df['hDif'].values    # [W/m2]
tAmb  = df['Tamb'].values    # [°C]
pVer  = df['Pload'].values   # [W] Verbrauchsprofil
zapf  = df['Zapfung'].values # [l/15min] Profil für Warmwasserbezug

zDif = df.index - dt.datetime(df.index[0].year, 1, 1, 0)
lfStd = zDif.total_seconds().values/3600 
# lfStd = np.array(lfStd0) # Umwandeln in ein Numpy-Array um später Sonnenstand, usw. berechnen zu können

deltaT = lfStd[1] - lfStd[0] # [h] Auflösung
tutc = df.index

dekl = 23.45*cos(360/(365*24) * (lfStd - 173*24))
omega = 15*np.mod(lfStd,24) + lg - 180  # [grad] Stundenwinkel
h = asin(sin(dekl)*sin(bg) + cos(dekl)*cos(bg)*cos(omega)) #[grad]
azi = acos((sin(h)*sin(bg) - sin(dekl))/cos(h)/cos(bg))*np.sign(omega)

plt.plot(azi,h)

neig = 30
aziFl = 0
al = 0.2
hDir = hGlo - hDif
cosTheta = cos(neig)*sin(h) + sin(neig)*cos(h)*cos(azi - aziFl)
cosTheta[cosTheta<0] = 0
hDifFl = hDif*(1 + cos(neig))/2
hAlbFl = hGlo*al*(1 - cos(neig))/2
hDirFl = hDir/np.maximum(sin(h), sin(5))*cosTheta
hFl = hDirFl + hDifFl + hAlbFl