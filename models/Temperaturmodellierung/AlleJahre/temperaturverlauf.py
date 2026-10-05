import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

#Lesen der Daten aus Datei TageslängenDA2025
file =  open('Temperaturmodellierung/AlleJahre/jahrestemperaturen.csv','r')  # open braucht den genauen Pfad ab working directory
Jahre = []   #erzeugt leeren Vektor
for line in file:
    Jahre.append(line.split(","))   # fügt Liste der Jahresdaten in Jahre ein
#Tageslängen = f.readlines()
file.close()
Jahre.pop(0) # Entferne Beschriftung
print (Jahre)

fig, ax = plt.subplots(figsize = (6, 6))
plt.title("Jahresdurchschnittstemperaturen am Rhonegletscher (Messstation)")
plt.xlim(1950, 2030)
plt.ylim(0, 20)
plt.xlabel(r"$Jahr$")
plt.ylabel(r"Temperatur in [°C]", rotation = 90)

jahr = []
jahresdurchschnittstemperatur = []
for i in range(len(Jahre)):
    try:
        x = int(Jahre[i][0])
        y = float(Jahre[i][1])
        jahr.append(x)
        jahresdurchschnittstemperatur.append(y)
    except:
        print(f"Das Jahr {Jahre[i][0]} wurde mit dem Wert {Jahre[i][1]} aussortiert.")
plt.plot(jahr, jahresdurchschnittstemperatur)

plt.show()