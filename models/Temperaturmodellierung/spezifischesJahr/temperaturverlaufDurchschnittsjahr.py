import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

STARTJAHR = 1955
ENDJAHR = 2025

def f(x, a, b, c , d):
    return a*np.sin(2*np.pi*(x-c)/b)+d

def tagestemperaturenVonJahr(jahr):
    #Lesen der Daten aus Datei
    try:
        file =  open(f'Temperaturmodellierung/spezifischesJahr/daten/klimadaten_67200_{jahr}.csv','r')  # open braucht den genauen Pfad ab working directory
    except:
        print(f"ERROR: Jahr {jahr} konnte nicht gefunden werden.")
        Tagestemperaturen = []
        for i in range(366):
            Tagestemperaturen.append(None)
        return(Tagestemperaturen)
    Tage = file.readlines()
    Tagestemperaturen = []   #erzeugt leeren Vektor
    Tage.pop(0) # Entferne Beschriftung
    for tag in Tage:
        try:
            y_value = float(tag.split(";")[4])
        except:
            y_value = None
        Tagestemperaturen.append(y_value)   # fügt Liste der Jahresdaten in Jahre ein
    file.close()
    if len(Tagestemperaturen) != 365 and len(Tagestemperaturen) != 366:
        print(f"ERROR: Jahr hat nicht richtige Menge an Tagen; Jahr: {jahr}")
    return(Tagestemperaturen)

alleJahre=[]
for jahr in range(STARTJAHR, ENDJAHR, 1):
    alleJahre.append(tagestemperaturenVonJahr(jahr))
durchschnittsTagestemperatur = []
for tag in range(0, 366, 1):
    summe=0
    anzahl=0
    for jahr in alleJahre:
        try:
            summe+=jahr[tag]
            anzahl+=1
        except:
            pass
    durchschnittsTagestemperatur.append(summe/anzahl)

fig, ax = plt.subplots(figsize = (10, 4))
plt.title(f"Durchschnitt der Jahre {STARTJAHR} bis {ENDJAHR}   " + r"$y = a*sin(2\pi(x-c)/b)+d$")
plt.subplots_adjust(left = 0.12, bottom = 0.3)
plt.xlim(1, 365)
plt.ylim(-10, 30)
plt.xlabel(r"$Tag$")
plt.ylabel(r"Temperatur in [°C]", rotation = 90)

x = np.arange(0, 366, 0.1)
y, = plt.plot(x, f(x, 10, 365.25, 100, 10), 'b-', lw = 1)
x2 = np.arange(0, 366, 1)
data, = plt.plot(x2,durchschnittsTagestemperatur,'r:',lw = 1)

# x- und y-Position, Länge und Höhe der Slider im Plot festlegen
xyA = plt.axes([0.1, 0.17, 0.8, 0.03])
xyB = plt.axes([0.1, 0.12, 0.8, 0.03])
xyC = plt.axes([0.1, 0.07, 0.8, 0.03])
xyD = plt.axes([0.1, 0.02, 0.8, 0.03])

# Slider-Objekte erzeugen
# Slidername=Slider()
sldA = Slider(xyA, "a",   0.0, 14.0, valinit = 10, valstep = 0.1)
sldB = Slider(xyB, "b",   0.0,  400.0, valinit = 365.25, valstep = 0.1)
sldC = Slider(xyC, "c", 0, 365.0, valinit = 100, valstep = 1.0)
sldD = Slider(xyD, "d", 10.0, 14.0, valinit = 10, valstep = 0.01)

# Slider Update
def update(val):
    a = sldA.val
    b = sldB.val
    c = sldC.val
    d = sldD.val
    y.set_data(x, f(x, a, b, c, d))
    
# Änderungen abfragen
sldA.on_changed(update)
sldB.on_changed(update)
sldC.on_changed(update)
sldD.on_changed(update)

ax.grid(True)
plt.show()
update()