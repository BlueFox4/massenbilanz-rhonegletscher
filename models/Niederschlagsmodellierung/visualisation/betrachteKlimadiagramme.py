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

def niederschlaegeVonJahrMitMonaten(jahreszahl):
    #Lesen der Daten aus Datei
    Tage=[]
    for tagesdaten in daten:
        if int(tagesdaten[0]) == jahreszahl:
            Tage.append(tagesdaten)
    Monatsniederschlaege = []   #erzeugt leeren Vektor
    i=0
    for monatszahl in range(1, 13):
        summe = 0
        while int(Tage[i][1]) == monatszahl:
            try:
                summe += float(Tage[i][8])
            except:
                print(f"Im Jahr {jahreszahl} konnte der Niederschlag des Tages {i} mit dem Wert {Tage[i][8]} nicht zum Monat addiert werden.")
            i+=1
            if i+1 >= len(Tage):
                break
        Monatsniederschlaege.append(summe)
    return(Monatsniederschlaege)


fig, ax = plt.subplots(figsize = (10, 4))
plt.title(f"Tagesniederschläge und Modell: " + r"$y = a*sin(2\pi(x-c)/b)+d$")
plt.subplots_adjust(left = 0.12, bottom = 0.3)
plt.xlim(1, 12)
plt.ylim(0, 250)
plt.xlabel(r"$Monat$")
plt.ylabel(r"Niederschlag in [mm]", rotation = 90)

Monatsniederschlaege = niederschlaegeVonJahrMitMonaten(STARTJAHR)
x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
data, = plt.plot(x,Monatsniederschlaege,'r:',lw = 1)


# x- und y-Position, Länge und Höhe der Slider im Plot festlegen
xyA = plt.axes([0.1, 0.17, 0.8, 0.03])

# Slider-Objekte erzeugen
# Slidername=Slider()
sldJAHR = Slider(xyA, "Jahr",   1955, 2025, valinit = STARTJAHR, valstep = 1)

# Slider Update
def update(val):
    jahr = sldJAHR.val
    Monatsniederschlaege = niederschlaegeVonJahrMitMonaten(jahr)
    data.set_data(x,Monatsniederschlaege)

sldJAHR.on_changed(update)

ax.grid(True)
plt.show()