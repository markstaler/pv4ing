# -*- coding: utf-8 -*-
# erstellt ein sysntetisches Profil mit einstellbarer Auflösung mit Strahlung und Umgebungstemperatur
#
# ===============----------------------------------------------------------------------
# IMPORT PACKAGES
# ===============
#import sys
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import sqlite3 as sq
import matplotlib.dates as mdates

from bokeh.plotting import figure, show
from bokeh.layouts import column


############## Datenimport über Datenbank (SQLITE) #################################
#Cosmo ab/mit 15.1.2116

tstart = '2017-01-15 00:00:00'
tend   = '2018-01-15 00:00:00'  

#tstart = '2016-06-22 00:00:00'
#tend   = '2016-06-22 23:59:00' 

resolution = 1  # [hours] für die zu speichernden Daten

t0 = dt.datetime.strptime(tstart,'%Y-%m-%d %H:%M:%S')
t1 = dt.datetime.strptime(tend,'%Y-%m-%d %H:%M:%S')

###### COSMO Vorhersagewerte importieren
## ========= COSMO- DATUMS-DEFINITION =============================================================================================
d0 = dt.datetime.strptime('20100101','%Y%m%d')
deltaT0=t0-d0
datumT0 = int(deltaT0.days) + 1 - 1 # Ein Tag früher da COSMO ab 3:00 beginnt und nicht ab 00:00 
deltaT1=t1-d0
datumT1 = int(deltaT1.days) + 2

cosmoDB    = sq.connect('D:/LocalData/nanAuswertung/nanDBs/nanCOSMO.db', detect_types = sq.PARSE_DECLTYPES|sq.PARSE_COLNAMES)
cur = cosmoDB.cursor()

sam = (datumT1 - datumT0) *24
T_2M     = np.zeros(sam)
TOT_PREC = np.zeros(sam)
GLOB     = np.zeros(sam)

tcosmo = (np.arange(0, sam, 1.0) - 0.5 + 3.0 - 24.0) * 3600 # Sekunden. +3 weil Cosmo bei 3:00 beginnt und  -24 weil Export 1 Tag vorher  


for d in range(datumT0, datumT1):
    sql="SELECT WERT FROM faktentabelle WHERE VORLAUFZEIT < 24 AND ORT=1 AND PARAMETER='T_2M' AND DATUM = " + str(d) + " ORDER BY VORLAUFZEIT ASC"
    cur.execute(sql)
    data    = cur.fetchall()
    if data != []:
        data    = np.array(data)
        T_2M[(d-datumT0)*24 : (d-datumT0)*24 + 24] = data[0 : 24,0]

    sql="SELECT WERT FROM faktentabelle WHERE VORLAUFZEIT < 24 AND ORT=1 AND PARAMETER='TOT_PREC' AND DATUM = " + str(d) + " ORDER BY VORLAUFZEIT ASC"
    cur.execute(sql)
    data    = cur.fetchall()
    if data != []:        
        data    = np.array(data)
        TOT_PREC[(d-datumT0)*24 : (d-datumT0)*24 + 24] = data[0 : 24,0]
   
    sql="SELECT WERT FROM faktentabelle WHERE VORLAUFZEIT < 24 AND ORT=1 AND PARAMETER='GLOB' AND DATUM = " + str(d) + " ORDER BY VORLAUFZEIT ASC"
    cur.execute(sql)
    data    = cur.fetchall()
    if data != []:
        data    = np.array(data)
        GLOB[(d-datumT0)*24 : (d-datumT0)*24 + 24] = data[0 : 24,0]
cur.close()
cosmoDB.close() 


NTBsolar    = sq.connect('D:/LocalData/nanAuswertung/nanDBs/nanDB.db', detect_types = sq.PARSE_DECLTYPES|sq.PARSE_COLNAMES)
cur = NTBsolar.cursor()
sqlstatement = "SELECT TINDEX, GLOBAL_VENT, DIFFUS_VENT, TEMPERATUR, WINDGESCHWINDIGKEIT, NIEDERSCHLAG_MM_H \
FROM nan WHERE TINDEX > DATETIME('" + tstart + "') AND TINDEX < DATETIME('" + tend + "') \
ORDER BY TINDEX ASC"
cur.execute(sqlstatement)
data = cur.fetchall()
#np.save('data.npy',data)
cur.close()
NTBsolar.close()
#data = np.load('data.npy')
dataNP  = np.array(data)
data   = dataNP[:,1:].astype(float)
timeNP  = dataNP[:,0] #Winterzeit
tutc  = np.asarray([dt.datetime.strptime(t,'%Y-%m-%d %H:%M:%S') for t in timeNP])
hGloIn  = data[:,0]
hDif  = data[:,1]
Tamb  = data[:,2]
wind  = data[:,3]
prec  = data[:,4]
del data, dataNP

hGloIn[hGloIn < 0]=0
hGloIn[hGloIn > 1500]=0
hDif[hDif < 0]=0
hDif[hDif > 1500]=0
Tamb[Tamb < -50]=0
Tamb[Tamb > 50]=0


## Prueft Loecher in den IV-Daten
hmin = 5.0
deltat = 60*60 #[s] Zeitschritt ab welchen ein Fehler gezählt wird
eError = np.zeros(tutc.size) 
for i in range(tutc.size-1):
    error = tutc[i+1] - tutc[i]
    if (error.seconds>deltat):
        print(str(i))
        eError[i] = error.total_seconds()/3600.0 # [h]
 
fig, ax = plt.subplots()
plt.plot_date(tutc, eError,'g.',label="Interrupts")
plt.xlabel('Time [-]')
plt.ylabel('Downtime per Interrupt [h]')
leg = plt.legend(loc="best", fancybox=True)
leg.get_frame().set_alpha(0.40)
plt.show()


title = "downtime %3.1f"%(np.sum(eError)) +\
 "h correspond to %3.1f" %(np.sum(eError)/((tutc[-1]-tutc[0]).total_seconds()/3600) * 100.0) + "Proz. of daytime (h>"+str(hmin)+"dg, not night)"
 
fig, ax = plt.subplots()
bins=[1,2,4,6,8,10,12,14,16,18,20,22,24]
hist, bin_edges = np.histogram(eError)
ax.bar(bin_edges[:-1]-0.5, hist, width=1) 
ax.set_ylabel('Cumulated Time per Downtime [h]')
ax.set_ylabel('No. of Interrupt per Downtime Class [1]')
ax.set_title(title)
ax.set_xticks(bin_edges)
#ax.set_xticklabels(bins)
plt.show()
# ======END CHECK DATA QUALITY====


# Fill out hole in radiation data
for i in range(tutc.size-1):
    if (tutc[i+1] - tutc[i]) > dt.timedelta(hours = 1):
        np.put(hGloIn,i,0.0) # Replaces specified elements of an array with given values.
        np.put(hDif,i,0.0)
        np.put(wind,i,0.0)
        np.put(prec,i,0.0)
        np.put(hGloIn,i+1,0.0)
        np.put(hDif,i+1,0.0)
        np.put(wind,i+1,0.0)
        np.put(prec,i+1,0.0)


################ Datenimport txt-File von METEOSCHWEIZ #############################
#data = np.genfromtxt('data1year.csv', skip_header = 1,  delimiter = ';' )
#t     = data[:,1]
#hDif  = data[:,2]
#hGlo  = data[:,3]
#Tamb1 = data[:,4]
#
#tstart = (31+28+31+30+31+30+31+31+30)*24.0 # Startpunkt 1.10.2009
#tende = hDif.size # Berechnet Ende über die Lände des Messwerte-Array
#deltaT = 1.0; # [h]
#tutc = np.arange(tstart, tstart+tende*deltaT, deltaT) # [h] laufende Stunden im Jahr
#
#
### Eingrenzung der Importdaten für Test-Zwecke
##a = int(0)
##e = int(a + 24)
##hDif  = hDif[a:e]
##hGlo  = hGlo[a:e]
##Tamb1 = Tamb1[a:e]
##tutc  = tutc[a:e]
#
#
## erstellt ein Zeit-Array mit datetime
#start = dt.datetime(2009,1,1,0,0,0)
#tutcDT = []
#for i in range(tutc.size):
#    tutcDT.append(start + dt.timedelta(hours = tutc[i]))
#tutcDT = np.array(tutcDT) # datetime
#
#t0 = tutcDT[0]
#t1 = tutcDT[-1]

################ ENDE Datenimport von METEOSCHWEIZ #############################



### abhier unabhängig welcher Datenimport



################Erzeugen eines Verbrauchsprofil ################################
##### Dieskretisieren auf synt. Zeitreihe tSyn in UTC
samples = int((t1 - t0).total_seconds() ) # fest auf 1 Sekunde auflösung
tSyn = []
for i in range(samples): # erzeugt neuen Datetime - Array
    tSyn.append(t0 + dt.timedelta(seconds = i))
tSyn = np.array(tSyn)

# Erzeugt Time-Array mit Sekunden
timeSec = np.zeros(tutc.size) 
for i in range(tutc.size):
    timeSec[i] = (tutc[i]-t0).total_seconds()
tSynSec = np.zeros(tSyn.size) # erzeugt Time-Array mit Sekunden
for i in range(tSyn.size):
    tSynSec[i] = (tSyn[i]-t0).total_seconds()
hGloSyn = np.interp(tSynSec,timeSec,hGloIn)


##### WEEKDAY + DAY LIGHT SAVING
weekday = np.asarray([tSyn[t].weekday() for t in range(tSyn.size)])
weekday[weekday<5] = 0 # Wochentage
weekday[weekday>0] = 1 # Wochenende an denen alles 1 h später ist
daylight = np.ones(weekday.shape)

daylight[tSyn>dt.datetime(2014,3,30)] = 2 #Sommerzeit
daylight[tSyn>dt.datetime(2014,10,25)] = 1 #Winterzeit

# Time Array in Datetime corrected with day light saving
tSynReal = np.asarray([tSyn[t] + dt.timedelta(hours = daylight[t]) for t in range(tSyn.size)])
# Array with couninous seconds corrected with day light saving and weekend
tSec = tSynSec  + daylight*3600 - weekday*3600
## Array in Seconds a Days. The day corrected with day light saving and weekend
tDay = (np.mod(tSec,24*3600))/3600.0

##### Licht
pLight = np.zeros(tSec.size)
flag0 = 1
flag  = 0
counter = 0
for i in range(pLight.size):
    if (tDay[i] > 6.20) & (tDay[i] < 12) & flag0:
        pLight[i] = 1
        flag = 0
        counter = 0
    if hGloSyn[i] > 200.0:
        flag0 = 0
        couter = 0
    if  (tDay[i] > 12.00) & (tDay[i] < 22.00): # Ausschaltzeit unter der Woche. Wochenende um 1 Stunde nach hinten
        if ((hGloSyn[i] < 200.0) | flag):
            counter = counter + 1
        if (counter > 10*60): ## schaltet erst ein wenn 10 min niedere Strahlung
            flag = 1
            pLight[i] = 1
    if tDay[i]>22.00:
        flag0 = 1
        
pLight = pLight * (2*155.0 + 89.0 + 2*37.0 + 37 + 50) #2xGrekMedium + Badlich + GrekTV-Zimmer + GrekGang +50 für PC/TV...

##### Kaffemaschine 
on1 = 6.30        # [h] morning
duration1 = 1.00  # [h] morning
on2 = 13.00       # [h] morning
duration2 = 1.00  # [h]morning

coffee = np.zeros(tDay.size)
coffee[tDay>on1]=1
coffee[tDay>on1+duration1]=0
coffee[tDay>on2]=1
coffee[tDay>on2+duration2]=0

coffeePWM = np.zeros(coffee.size)
counter = 0
for i in range(coffeePWM.size):
    counter = counter +1
    if counter<10: # 10 sec ontime
        coffeePWM[i] = 1
    if counter>200: #Reset counter: 200 sec total time
        counter = 0
coffee = coffee * coffeePWM * 1200

##### Kühlschrank
eAnual = 200 # [kWh] Aunnual consumption
pComp  = 130 # [W] Compressor Power
cycle  = 60  # [min] total Cycle time of Intervall

fridge = np.zeros(tSyn.size)
on = int(cycle*60*(eAnual/8.760)/pComp)
counter = 0
for i in range(fridge.size):
    counter = counter + 1
    if counter < on:
        fridge[i] = pComp
    if counter > cycle*60:
        counter = 0

##### Kochen
startL1    = 10.0  #[h] start cooking Lunch heat plate 1
upHeatL1   = 10/60 #[h] heating Up with constant power
keepHeatL1 = 1.70  #[h] keep heat

startL2    = 11.0  #[h] start cooking  Lunch heat plate 2 
upHeatL2   = 6/60  #[h] heating Up with constant power
keepHeatL2 = 0.80  #[h] keep heat

startL3    = 11.5  #[h] start cooking  Lunch heat plate 2 
upHeatL3   = 6/60  #[h] heating Up with constant power
keepHeatL3 = 0.90  #[h] keep heat

startD1    = 18.30 #[h] start cooking  Dinner heat plate 1
upHeatD1   = 6/60  #[h] heating Up with constant power
keepHeatD1 = 0.5   #[h] keep heat

cookUpHeatL1 = np.zeros(tDay.size)
cookKeepHeatL1 = np.zeros(tDay.size)
cookUpHeatL1[tDay>startL1] = 1
cookUpHeatL1[tDay>startL1+upHeatL1] = 0
cookKeepHeatL1[tDay>startL1+upHeatL1] = 1
cookKeepHeatL1[tDay>startL1+upHeatL1+keepHeatL1] = 0

cookUpHeatL2 = np.zeros(tDay.size)
cookKeepHeatL2 = np.zeros(tDay.size)
cookUpHeatL2[tDay>startL2] = 1
cookUpHeatL2[tDay>startL2+upHeatL2] = 0
cookKeepHeatL2[tDay>startL2+upHeatL2] = 1
cookKeepHeatL2[tDay>startL2+upHeatL2+keepHeatL2] = 0

cookUpHeatL3 = np.zeros(tDay.size)
cookKeepHeatL3 = np.zeros(tDay.size)
cookUpHeatL3[tDay>startL3] = 1
cookUpHeatL3[tDay>startL3+upHeatL3] = 0
cookKeepHeatL3[tDay>startL3+upHeatL3] = 1
cookKeepHeatL3[tDay>startL3+upHeatL3+keepHeatL3] = 0

cookUpHeatD1 = np.zeros(tDay.size)
cookKeepHeatD1 = np.zeros(tDay.size)
cookUpHeatD1[tDay>startD1] = 1
cookUpHeatD1[tDay>startD1+upHeatD1] = 0
cookKeepHeatD1[tDay>startD1+upHeatD1] = 1
cookKeepHeatD1[tDay>startD1+upHeatD1+keepHeatD1] = 0

PWM1 = np.zeros(tDay.size)
counter = 0
for i in range(PWM1.size): # Stufe 4
    counter = counter +1
    if counter<10: # sec ontime
        PWM1[i] = 1
    if counter>46: #total sec time: Reset counter
        counter = 0

PWM2 = np.zeros(tDay.size) # Stufe 5
counter = 0
for i in range(PWM2.size):
    counter = counter +1
    if counter<18: # sec ontime
        PWM2[i] = 1
    if counter>47: #total sec time: Reset counter
        counter = 0
        
PWM3 = np.zeros(tDay.size) # Stufe 6
counter = 0
for i in range(PWM3.size):
    counter = counter +1
    if counter<27: # sec ontime
        PWM3[i] = 1
    if counter>48: #total sec time: Reset counter
        counter = 0        

cook =  (cookUpHeatL1+cookKeepHeatL1*PWM1)*1700 + (cookUpHeatL2+cookKeepHeatL2*PWM3)*1030 + (cookUpHeatL3+cookKeepHeatL3*PWM2)*1030 + (cookUpHeatD1+cookKeepHeatD1*PWM2)*1030

#### BASE LOAD
base = np.ones(tSynReal.size) * 100.0


#### RESUSLTS LOAD PROFIL ##
load = pLight + coffee + fridge + cook + base
consumption = (np.sum(load)/3600)/1000/3.0 # [kWh/a]
print("1s Gesamtverbrauch  [kWh]: " + str(consumption))

#fig, ax = plt.subplots(figsize = (12,6))
a=int(5*3600)
e=int(23*3600)
plt.plot_date(tSynReal[a:e], pLight[a:e],'y-', linewidth=0.3, label = 'Licht')
plt.plot_date(tSynReal[a:e], coffee[a:e],'k-', linewidth=0.3, label = 'Kaffee')
plt.plot_date(tSynReal[a:e], fridge[a:e],'b-', linewidth=0.3, label = 'Kuehlen')
plt.plot_date(tSynReal[a:e], cook[a:e],'r-',   linewidth=0.3, label = 'Kochen')
plt.plot_date(tSynReal[a:e], base[a:e],'b--',  linewidth=0.3, label = 'Grundlast')
plt.plot_date(tSynReal[a:e], hGloSyn[a:e]*4,'g-', linewidth=0.3, label = 'Globalstrahlung x 4')
plt.legend()
specformatter = mdates.DateFormatter('%H:%M')
ax.xaxis.set_major_formatter(specformatter)
plt.ylabel('Leistung  [W]')
plt.savefig('loadProfile.pdf', bbox_inches = 'tight')
plt.show()
    


###### Dieskretisieren auf synt. Zeitreihe tSyn in UTC
anzTage = np.ceil((t1 - t0).total_seconds() / 3600 /24)
samples = int(anzTage / resolution * 24)
tSyn = []
for i in range(samples): # erzeugt neuen Datetime - Array
    tSyn.append(t0 + dt.timedelta(seconds = i*resolution*3600))
tSyn = np.array(tSyn)
tSynInt = np.zeros(tSyn.size) # erzeugt Time-Array mit Sekunden von Zieldaten (resolution)
for i in range(tSynInt.size):
    tSynInt[i] = (tSyn[i] - t0).total_seconds()

tutcInt = np.zeros(tutc.size) # erzeugt Time-Array mit Sekunden von Ausgangsdaten
for i in range(tutc.size):
    tutcInt[i] = (tutc[i] - t0).total_seconds()


# Interpolieren nimmt Wert aus der Kurve unabhängig von den Vor- oder Nachwerten. Soll nich verwendet werden.
# Über Cumsum wird das Mittel gebildet (energetisch)
# Der Strahlungswert gilt ab dem Zeitpunkt für die Dauer von Resolution
deltaT = np.diff(tutcInt)
deltaT = np.append(deltaT,0)

loadCS = np.cumsum(load/3600/resolution)
loadCSint = np.interp(tSynInt, tSynSec, loadCS)
load = np.diff(loadCSint)
load = np.append(load,0)

hGloCS = np.cumsum(hGloIn*deltaT/3600/resolution)
hGloCSint = np.interp(tSynInt,tutcInt,hGloCS)
hGlo = np.diff(hGloCSint)
hGlo = np.append(hGlo,0)

hDifCS = np.cumsum(hDif*deltaT/3600/resolution)
hDifCSint = np.interp(tSynInt,tutcInt,hDifCS)
hDif = np.diff(hDifCSint)
hDif = np.append(hDif,0)

Tamb = np.interp(tSynInt,tutcInt,Tamb)

windCS = np.cumsum(wind*deltaT/3600/resolution)
windCSint = np.interp(tSynInt,tutcInt,windCS)
wind = np.diff(windCSint)
wind = np.append(wind,0)

precCS = np.cumsum(prec*deltaT/3600/resolution)
precCSint = np.interp(tSynInt,tutcInt,precCS)
prec = np.diff(precCSint)
prec = np.append(prec,0)

TambCOSMO = np.interp(tSynInt,tcosmo, T_2M)
hGloCOSMO = np.interp(tSynInt,tcosmo, GLOB)
precCOSMO = np.interp(tSynInt,tcosmo, TOT_PREC)

plt.plot(tSyn, hGlo, 'b-')
plt.plot(tSyn, hGloCOSMO, 'r-')
plt.plot(tutc, hGloIn, 'k.')
plt.ylabel('Globalstrahlung')
plt.show()

plt.plot(tSyn, hDif, 'b-')
plt.ylabel('Diffusstrahlung')
plt.show()


plt.plot(tSyn, Tamb, 'b-')
plt.plot(tSyn, TambCOSMO, 'r-')
plt.ylabel('Temperatur')
plt.show()

plt.plot(tSyn, load, 'b-')
plt.ylabel('Last')
plt.show()

plt.plot(tSyn, wind, 'b-')
plt.ylabel('wind')
plt.show()

plt.plot(tSyn, prec, 'b-')
plt.plot(tSyn, precCOSMO, 'r-')
plt.ylabel('Niederschlag')
plt.show()

print('Import discretize...')


### Daten in csv-Datei exportieren
fn = open('DataExport15min.csv','w')
fn.write('Time;hGlo;hDif;Tamb;Pload;Wind;Niederschlag; hGloCOSMO; TambCOSMO; NiederCOSMO\n')
for i in range(tSyn.size):
    fn.write(str(tSyn[i])+';'+\
    str(hGlo[i])+';'+\
    str(hDif[i])+';'+\
    str(Tamb[i])+';'+\
    str(load[i])+';'+\
    str(wind[i])+';'+\
    str(prec[i])+';'+\
    str(hGloCOSMO[i])+';'+\
    str(TambCOSMO[i])+';'+\
    str(precCOSMO[i])+'\n')
fn.close()

print("Congratulation Simulation done !!!")


# Darstellung über Bokeh
fig1 = figure(title='Datenexport Strahlung', 
             x_axis_label='Zeit', 
             y_axis_label='Globalstrahlung [°C]', 
             x_axis_type='datetime', 
             plot_width=1400, plot_height=400 )
fig1.line(tSyn, hGlo, legend='gemessen', line_color = 'blue', line_width=1)
fig1.circle(tSyn, hGloCOSMO, legend='COSMO', fill_color = 'orange', line_color = 'blue', size=4)
show(fig1)

fig2 = figure(title='Datenexport Niederschlag', 
#             x_range=fig1.x_range, y_range=fig1.y_range, 
             x_axis_label='Zeit', 
             y_axis_label='Niederschlag [°C]', 
             x_axis_type='datetime', 
             plot_width=1400, plot_height=400 )
fig2.line(tSyn, prec, legend='gemessen', line_color = 'blue', line_width=1)
fig2.circle(tSyn, precCOSMO, legend='COSMO', fill_color = 'orange', line_color = 'blue', size=4)


#p = gridplot([[fig1, fig2]], toolbar_location=None)
show(column(fig1, fig2))


