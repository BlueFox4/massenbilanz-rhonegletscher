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

def leseBesteParameter(jahr):
    file =  open(f"models/Niederschlagsmodellierung/parameterBerechnung/bestenParameter.csv",'r')
    alleBestenParameter = file.readlines()
    alleBestenParameter.pop(0)
    for bestenParameter in alleBestenParameter:
        bestenParameter = bestenParameter[:-1].split(",")
        if int(bestenParameter[0]) == jahr:
            return ([float(bestenParameter[1]), float(bestenParameter[2]), float(bestenParameter[3]), float(bestenParameter[4])])
    print(f"Konnte das Jahr {jahr} nicht finden.")

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
            y_value = float(tag[8])
        except:
            y_value = None
        Tagesniederschlaege.append(y_value)   # fügt den Niederschlagswert des Tages der Liste Tagesniederschlaege hinzu
    if len(Tagesniederschlaege) < 365:
        print(f"Anzahl Tage beträgt nur {len(Tagesniederschlaege)}. Das Jahr wird aussortiert.")
        return None
    return(Tagesniederschlaege)

Tagesniederschlaege = niederschlaegeVonJahr(STARTJAHR)

fig, ax = plt.subplots(figsize = (10, 4))
plt.title(f"Tagesniederschläge und Modell: " + r"$y = a*sin(2\pi(x-c)/b)+d$")
plt.subplots_adjust(left = 0.12, bottom = 0.3)
plt.xlim(1, 366)
plt.ylim(-5, 50)
plt.xlabel(r"$Tag$")
plt.ylabel(r"Niederschlag in [mm]", rotation = 90)

[optimales_a, optimales_b, optimales_c, optimales_d] = leseBesteParameter(STARTJAHR)
x = np.arange(0, 365, 0.1)
y, = plt.plot(x, f(x, optimales_a, optimales_b, optimales_c, optimales_d), 'b-', lw = 1)
x2 = np.arange(0, 365, 1)
data, = plt.plot(x2,Tagesniederschlaege,'r:',lw = 1)


# x- und y-Position, Länge und Höhe der Slider im Plot festlegen
xyA = plt.axes([0.1, 0.17, 0.8, 0.03])

# Slider-Objekte erzeugen
# Slidername=Slider()
sldJAHR = Slider(xyA, "Jahr",   1955, 2025, valinit = STARTJAHR, valstep = 1)

# Slider Update
def update(val):
    jahr = sldJAHR.val
    [optimales_a, optimales_b, optimales_c, optimales_d] = leseBesteParameter(jahr)
    print([optimales_a, optimales_b, optimales_c, optimales_d])
    y.set_data(x, f(x, optimales_a, optimales_b, optimales_c, optimales_d))
    Tagesniederschlaege = niederschlaegeVonJahr(jahr)
    data.set_data(x2,Tagesniederschlaege)

sldJAHR.on_changed(update)

ax.grid(True)
plt.show()