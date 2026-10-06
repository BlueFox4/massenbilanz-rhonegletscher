import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

STARTJAHR = 1955
ENDJAHR = 2025

with open(f'data/data_all.csv','r') as file: # open braucht den genauen Pfad ab working directory
    daten = file.readlines()[1:]
    for i in range(len(daten)):
        datum = daten[i].split(",")
        for j in range(len(datum)):
            datum[j] = datum[j].strip()
        daten[i] = datum

def niederschlaegeVonJahr(jahreszahl):
    #Lesen der Daten aus Datei
    tage=[]
    for tagesdaten in daten:
        if int(tagesdaten[0]) == jahreszahl:
            tage.append(tagesdaten)
    tagesniederschlaege = []   #erzeugt leeren Vektor
    for tag in tage:
        try:
            y_value = float(tag[8])
        except:
            y_value = np.nan
        tagesniederschlaege.append(y_value)   # fügt den Niederschlagswert des Tages der Liste Tagesniederschlaege hinzu
    return tagesniederschlaege

alleJahre=[]
for jahreszahl in range(STARTJAHR, ENDJAHR+1, 1):
    einJahr = niederschlaegeVonJahr(jahreszahl)
    if len(einJahr) == 365 or len(einJahr) == 366:
        alleJahre.append(einJahr)
        print(jahreszahl)

durchschnittsTagesniederschlag = []
for tageszahl in range(0, 365, 1):
    summe = 0
    anzahl = 0
    for jahr in alleJahre:
        if not np.isnan(jahr[tageszahl]):
            summe += jahr[tageszahl]
            anzahl += 1
            # print(f"Der Niederschlagswert im Jahr {STARTJAHR+i} am Tag {tageszahl} wurde aussortiert")
        # if not(summe):
        #     print(f"Fehler bei Jahr {1955+i} am Tag {tageszahl}")
    # print(summe, anzahl)
    durchschnittsTagesniederschlag.append(summe/anzahl)

fig, ax = plt.subplots(figsize = (10, 4))
plt.title(f"Durchschnitt der Jahre {STARTJAHR} bis {ENDJAHR}   " + r"$y = a*sin(2\pi(x-c)/b)+d$")
plt.subplots_adjust(left = 0.12, bottom = 0.3)
plt.xlim(1, 365)
plt.ylim(0, 20)
plt.xlabel(r"$Tag$")
plt.ylabel(r"Niederschlag in [mm]", rotation = 90)

x2 = np.arange(0, 365, 1)
data, = plt.plot(x2,durchschnittsTagesniederschlag,'r:',lw = 1)

ax.grid(True)
plt.show()