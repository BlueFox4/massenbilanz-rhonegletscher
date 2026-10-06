import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

STARTJAHR = 1999

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


fig, ax = plt.subplots(figsize = (10, 4))
plt.title(f"Tagesniederschläge und Modell: " + r"$y = a*sin(2\pi(x-c)/b)+d$")
plt.subplots_adjust(left = 0.12, bottom = 0.3)
plt.xlim(1, 366)
plt.ylim(-2, 50)
plt.xlabel(r"$Monat$")
plt.ylabel(r"Niederschlag in [mm]", rotation = 90)

Monatsniederschlaege = niederschlaegeVonJahr(STARTJAHR)
x = np.arange(1, 366, 1)
data, = plt.plot(x,Monatsniederschlaege,'r:',lw = 1)


# x- und y-Position, Länge und Höhe der Slider im Plot festlegen
xyA = plt.axes([0.1, 0.17, 0.8, 0.03])

# Slider-Objekte erzeugen
# Slidername=Slider()
sldJAHR = Slider(xyA, "Jahr",   1955, 2025, valinit = STARTJAHR, valstep = 1)

# Slider Update
def update(val):
    jahr = sldJAHR.val
    Monatsniederschlaege = niederschlaegeVonJahr(jahr)
    data.set_data(x,Monatsniederschlaege)

sldJAHR.on_changed(update)

ax.grid(True)
plt.show()