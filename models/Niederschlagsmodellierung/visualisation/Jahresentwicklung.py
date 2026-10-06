import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

#Lesen der Daten aus Datei TageslängenDA2025
file =  open('data/data_year.csv','r')  # open braucht den genauen Pfad ab working directory
Jahre = []   #erzeugt leeren Vektor
for line in file:
    Jahre.append(line.split(","))   # fügt Liste der Jahresdaten in Jahre ein
file.close()
Jahre.pop(0) # Entferne Beschriftung

#Lege Ploteigenschaften fest
fig, ax = plt.subplots(figsize = (6, 6))
plt.title("Jahresniederschlag am Rhonegletscher")
plt.xlim(1955, 2023)
plt.ylim(200, 1500)
plt.xlabel(r"$Jahr$")
plt.ylabel(r"Gesamtjahresniederschlag in [mm]", rotation = 90)

jahr = [] # x-Achsen Werte
jahresniederschlag = [] # y-Achsen Werte
for i in range(len(Jahre)):
    try:
        x = int(Jahre[i][0]) # einzelner x-Wert
        y = float(Jahre[i][4]) # einzelner y-Wert; 4-->PP-->Gesamtniederschlag
        jahr.append(x)
        jahresniederschlag.append(y)
    except:
        print(f"Das Jahr {Jahre[i][0]} wurde mit dem Wert {Jahre[i][4]} aussortiert.")
plt.plot(jahr, jahresniederschlag, "r.")

plt.show()