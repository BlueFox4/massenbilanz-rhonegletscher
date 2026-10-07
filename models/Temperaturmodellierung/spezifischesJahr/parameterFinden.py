#Finde für ein beliebiges Jahr die bestmöglichen Parameter a, b, c, d

import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import csv
from datenAusJahr import getJahresdaten

START_A = 10.0
START_B = 365.2425
START_C = 100.0
START_D = 10.0

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
            
besteWerteAllerJahre = [["Jahr", "a", "b", "c", "d"]]
for jahr in range(1955, 2026, 1):
    Tage = getJahresdaten(jahr)
    Tagestemperaturen = []   #erzeugt leeren Vektor
    for tag in Tage:
        Tagestemperaturen.append(tag[3])   # fügt Tagesdurchschnittstemperatur in Tagestemperaturen ein

    bestenWerte = findeBesteAbweichung(START_A, START_B, START_C, START_D, Tagestemperaturen, berechneAbweichung(START_A, START_B, START_C, START_D, Tagestemperaturen))
    besteWerteAllerJahre.append([jahr] + bestenWerte)
    print(f"Für das Jahr {jahr} sind die besten Werte: {bestenWerte}")

with open("models/Temperaturmodellierung/spezifischesJahr/bestenParameter.csv", "w", newline="") as writeToFile:
    writer = csv.writer(writeToFile)
    writer.writerows(besteWerteAllerJahre)