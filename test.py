# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 16:51:48 2020

@author: mark
"""

## Daten importieren
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

pd.plotting.register_matplotlib_converters() ## Pandas wird das Datum direkt in einem "Timeseries"-Format importieren, 
# weshalb die Defaulteinstellungen von Matplotlib mit diesem Befehl angepasst werden.

df = pd.read_csv('2017_DataExport15min.csv', delimiter=';', header = 0)
df = df.set_index(pd.DatetimeIndex(df['Time'])) 



hGlo  = df['hGlo'].values    # [W/m2] 
hDif  = df['hDif'].values    # [W/m2]
tAmb  = df['Tamb'].values    # [°C]
pVer  = df['Pload'].values   # [W] Verbrauchsprofil
zapf  = df['Zapfung'].values # [l/15min] Profil für Warmwasserbezug
tutc = df.index

lfStd = np.zeros(tutc.size)
for t in range(tutc.size):
    # berechnet laufender Tag im Jahr
    noDay = (tutc[t] - dt.datetime(tutc[0].year, 1, 1, 0)).days 
    # [h] berechnet laufende Stunde im Tag
    noHou = tutc[t].hour + (tutc[t].minute)/60 + (tutc[t].second)/3600 
    lfStd[t] = noDay*24 + noHou
    
deltaT = lfStd[1] - lfStd[0] # [h]



noHours = 24*4
noDays  = 365
tAmbM  = np.zeros((24*4, 365))
yHours = np.zeros((24*4, 365))
xDays  = np.zeros((24*4, 365))
for i in range(tAmb.size):
    hour = np.mod(lfStd[i],24)
    day  = int(np.floor(lfStd[i]/24))
    hourIndex = int(hour*4)
    dayIndex = int(np.mod(day,365)-1)
    tAmbM[hourIndex, dayIndex] = tAmb[i]
    yHours[hourIndex,dayIndex] = hour
    xDays[hourIndex,dayIndex]  = day
    
fig = plt.figure(4, figsize=(10,8))
plt.contourf(xDays, yHours, tAmbM, 15) # 15 Linien
plt.title('Umgebungstemperatur übers Jahr')
plt.xlabel('Tage im Jahr')
plt.ylabel('Tagesstunde')
plt.grid(which='both', linestyle='--')
plt.show()