import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

STARTJAHR = 1955
ENDJAHR = 2025

file =  open(f'data/data_all.csv','r')  # open braucht den genauen Pfad ab working directory
daten = file.readlines()
daten.pop(0) # Entferne Beschriftung
for i in range(len(daten)):
    daten[i]=daten[i][:-1].split(",")
file.close()

def f(x, a, b, c , d):
    return a*np.sin(2*np.pi*(x-c)/b)+d

def berechneAbweichung(a, b, c, d, y_data):
    abweichung=0
    for i in range(len(y_data)):
        if not(y_data[i]):
            continue
        abweichung += np.square(y_data[i]-f(i, a, b, c, d))
    return abweichung

def findeBesteAbweichung(a, b, c, d, y_data, aktuelleAbweichung):
    besteAbweichungWert = aktuelleAbweichung
    while True:
        besteAbweichung = 0 #aktuelleAbweichung
        a_plus_Abweichung = berechneAbweichung(a+0.01, b, c, d, y_data)
        if a_plus_Abweichung < besteAbweichungWert:
            besteAbweichungWert = a_plus_Abweichung
            besteAbweichung=1
        a_minus_Abweichung = berechneAbweichung(a-0.01, b, c, d, y_data)
        if a_minus_Abweichung < besteAbweichungWert:
            besteAbweichungWert = a_minus_Abweichung
            besteAbweichung=2
        # b_plus_Abweichung = berechneAbweichung(a, b+0.01, c, d, y_data)
        # if b_plus_Abweichung < besteAbweichungWert:
        #     besteAbweichungWert = b_plus_Abweichung
        #     besteAbweichung=3
        # b_minus_Abweichung = berechneAbweichung(a, b+0.01, c, d, y_data)
        # if b_minus_Abweichung < besteAbweichungWert:
        #     besteAbweichungWert = b_minus_Abweichung
        #     besteAbweichung=4
        c_plus_Abweichung = berechneAbweichung(a, b, c+0.01, d, y_data)
        if c_plus_Abweichung < besteAbweichungWert:
            besteAbweichungWert = c_plus_Abweichung
            besteAbweichung=5
        c_minus_Abweichung = berechneAbweichung(a, b, c-0.01, d, y_data)
        if c_minus_Abweichung < besteAbweichungWert:
            besteAbweichungWert = c_minus_Abweichung
            besteAbweichung=6
        d_plus_Abweichung = berechneAbweichung(a, b, c, d+0.01, y_data)
        if d_plus_Abweichung < besteAbweichungWert:
            besteAbweichungWert = d_plus_Abweichung
            besteAbweichung=7
        d_minus_Abweichung = berechneAbweichung(a, b, c, d-0.01, y_data)
        if d_minus_Abweichung < besteAbweichungWert:
            besteAbweichungWert = d_minus_Abweichung
            besteAbweichung=8
        if besteAbweichung == 0: #keine Verbesserung
            return([a, b, c, d])
        else:
            a = (a + 0.01) if besteAbweichung == 1 else (a - 0.01) if besteAbweichung == 2 else a
            # b = (b + 0.01) if besteAbweichung == 3 else (b - 0.01) if besteAbweichung == 4 else b
            c = (c + 0.01) if besteAbweichung == 5 else (c - 0.01) if besteAbweichung == 6 else c
            d = (d + 0.01) if besteAbweichung == 7 else (d - 0.01) if besteAbweichung == 8 else d

def niederschlaegeVonJahr(jahreszahl):
    #Lesen der Daten aus Datei
    Tage=[]
    for tagesdaten in daten:
        if int(tagesdaten[0]) == jahreszahl:
            Tage.append(tagesdaten)
    Tagesniederschlaege = []   #erzeugt leeren Vektor
    for tag in Tage:
        try:
            y_value = float(tag[8])
        except:
            y_value = None
        Tagesniederschlaege.append(y_value)   # fügt den Niederschlagswert des Tages der Liste Tagesniederschlaege hinzu
    return(Tagesniederschlaege)

alleJahre=[]
for jahr in range(STARTJAHR, ENDJAHR, 1):
    alleJahre.append(niederschlaegeVonJahr(jahr))
durchschnittsTagesniederschlag = []
for tag in range(0, 366, 1):
    summe=0
    anzahl=0
    for jahr in alleJahre:
        try:
            summe+=jahr[tag]
            anzahl+=1
        except:
            pass
    durchschnittsTagesniederschlag.append(summe/anzahl)
#Erstelle flacheren Graph durch jeden Punkt als Durchschnitt von den 5 umliegenden
# flacheDurchschnittsTagesniederschlag = []
# for i in range(366):
#     flacheDurchschnittsTagesniederschlag.append((durchschnittsTagesniederschlag[i-2]+durchschnittsTagesniederschlag[i-1]+durchschnittsTagesniederschlag[i]+durchschnittsTagesniederschlag[(i+1)%365]+durchschnittsTagesniederschlag[(i+2)%365])/5)
# durchschnittsTagesniederschlag=flacheDurchschnittsTagesniederschlag

fig, ax = plt.subplots(figsize = (10, 4))
plt.title(f"Durchschnitt der Jahre {STARTJAHR} bis {ENDJAHR}   " + r"$y = a*sin(2\pi(x-c)/b)+d$")
plt.subplots_adjust(left = 0.12, bottom = 0.3)
plt.xlim(1, 365)
plt.ylim(0, 10)
plt.xlabel(r"$Tag$")
plt.ylabel(r"Niederschlag in [mm]", rotation = 90)

# [optimales_a, optimales_b, optimales_c, optimales_d] = findeBesteAbweichung(11.4, 365.25, 105, 15.86, durchschnittsTagesniederschlag, berechneAbweichung(11.4, 365.25, 105, 15.86, durchschnittsTagesniederschlag))
# x = np.arange(0, 366, 0.1)
# y, = plt.plot(x, f(x, optimales_a, optimales_b, optimales_c, optimales_d), 'b-', lw = 1)
x2 = np.arange(0, 366, 1)
data, = plt.plot(x2,durchschnittsTagesniederschlag,'r:',lw = 1)

# # x- und y-Position, Länge und Höhe der Slider im Plot festlegen
# xyA = plt.axes([0.1, 0.17, 0.8, 0.03])
# xyB = plt.axes([0.1, 0.12, 0.8, 0.03])
# xyC = plt.axes([0.1, 0.07, 0.8, 0.03])
# xyD = plt.axes([0.1, 0.02, 0.8, 0.03])

# # Slider-Objekte erzeugen
# # Slidername=Slider()
# sldA = Slider(xyA, "a",   0.0, 14.0, valinit = optimales_a, valstep = 0.1)
# sldB = Slider(xyB, "b",   0.0,  400.0, valinit = optimales_b, valstep = 0.1)
# sldC = Slider(xyC, "c", 0, 365.0, valinit = optimales_c, valstep = 1.0)
# sldD = Slider(xyD, "d", 10.0, 20.0, valinit = optimales_d, valstep = 0.01)

# # Slider Update
# def update(val):
#     a = sldA.val
#     b = sldB.val
#     c = sldC.val
#     d = sldD.val
#     y.set_data(x, f(x, a, b, c, d))
    
# # Änderungen abfragen
# sldA.on_changed(update)
# sldB.on_changed(update)
# sldC.on_changed(update)
# sldD.on_changed(update)

ax.grid(True)
plt.show()
update(0)