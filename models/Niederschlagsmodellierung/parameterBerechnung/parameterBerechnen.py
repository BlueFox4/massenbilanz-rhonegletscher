#Finde für ein beliebiges Jahr die bestmöglichen Parameter a, b, c, d

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import csv


file =  open(f'data/data_all.csv','r')  # open braucht den genauen Pfad ab working directory
daten = file.readlines()
daten.pop(0) # Entferne Beschriftung
for i in range(len(daten)):
    daten[i]=daten[i][:-1].split(",")
file.close()

def f(x, a, b, c , d):
    return a*np.sin(2*np.pi*(x-c)/b)+d

def niederschlaegeVonJahr(jahreszahl):
    #Lesen der Daten aus Datei
    Tage=[]
    for tagesdaten in daten:
        if int(tagesdaten[0]) == jahreszahl:
            Tage.append(tagesdaten)
    Tagesniederschlaege = []   #erzeugt leeren Vektor
    for tag in Tage:
        try:
            y_value = float(tag[4])
        except:
            y_value = None
        Tagesniederschlaege.append(y_value)   # fügt den Niederschlagswert des Tages der Liste Tagesniederschlaege hinzu
    if len(Tagesniederschlaege) < 365:
        print(f"Anzahl Tage beträgt nur {len(Tagesniederschlaege)}. Das Jahr wird aussortiert.")
        return None
    return(Tagesniederschlaege)

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
            
besteWerteAllerJahre = [["Jahr", "a", "b", "c", "d"]]
for jahr in range(1955, 2026, 1):
    tagesniederschlaege = niederschlaegeVonJahr(jahr)
    if not(tagesniederschlaege):
        print(f"Die Datei mit dem Jahr {jahr} konnte nicht gelesen werden.")
        continue
    bestenWerte = findeBesteAbweichung(11, 365.24, 102, 16.15, tagesniederschlaege, berechneAbweichung(11, 365.24, 102, 16.15, tagesniederschlaege))
    besteWerteAllerJahre.append([jahr] + bestenWerte)
    print(f"Für das Jahr {jahr} sind die besten Werte: {bestenWerte}")

with open("models/Niederschlagsmodellierung/parameterBerechnung/bestenParameter.csv", "w", newline="") as writeToFile:
    writer = csv.writer(writeToFile)
    writer.writerows(besteWerteAllerJahre)