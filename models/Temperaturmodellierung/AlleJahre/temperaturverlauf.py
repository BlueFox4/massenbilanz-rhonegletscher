# ---------------------------------
# WICHTIG: AUSFUEREN MIT: python -m models.Temperaturmodellierung.AlleJahre.temperaturverlauf
# ----------------------------------
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from ..spezifischesJahr.besteParameterEntwicklung import d_func

SINCE = 2014

# Lesen der Daten aus data_year.csv
with open("data/data_year.csv", "r") as file:
    jahre = []

    for line in file:
        jahre.append(line.strip().split(","))
jahre.pop(0)  # Überschrift entfernen

with open(f"models/Temperaturmodellierung/spezifischesJahr/bestenParameter.csv",'r') as file: # open braucht den genauen Pfad ab working directory
    Jahre = file.readlines()
    Jahre.pop(0) # Entferne Beschriftung
    x = []
    d = []
    for jahr in Jahre:
        jahr = jahr.strip().split(",")
        x.append(int(jahr[0]))
        d.append(float(jahr[4]))

x_values = np.array(x)
d_values = np.array(d)


# Diagramm erstellen
fig, ax = plt.subplots(figsize=(6, 6))

plt.title("Jahresdurchschnittstemperaturen am Rhonegletscher (Messstation)")
plt.xlim(1955, 2026)
plt.ylim(0, 20)
plt.xlabel(r"$Jahr$")
plt.ylabel(r"Temperatur in [°C]", rotation=90)


# Messdaten aus CSV
jahreszahlen = []
jahresdurchschnittstemperatur = []

for i in range(len(jahre)):
    x = int(jahre[i][0])
    jahreszahlen.append(x)
    try:
        y = float(jahre[i][1])

        jahresdurchschnittstemperatur.append(y)

    except:
        jahresdurchschnittstemperatur.append(np.nan)
        print(
            f"Das Jahr {jahre[i][0]} wurde "
            f"mit dem Wert {jahre[i][1]} aussortiert."
        )


# Messdaten zeichnen
plt.plot(
    jahreszahlen,
    jahresdurchschnittstemperatur,
    "g.",
    label="Messdaten (tatsächliche Jahresmittel)"
)


# Modell berechnen
y_model1 = []

for jahreszahl in jahreszahlen:
    y_model1.append(d_func(jahreszahl+1, 1994))
# Modell berechnen
y_model2 = []

for jahreszahl in jahreszahlen:
    y_model2.append(d_func(jahreszahl+1, 2014))


# Modell zeichnen
plt.plot(

    
    jahreszahlen,
    y_model1,
    label=f"Modell ab {1994} (Ausgleichsgerade)"
)
# Modell zeichnen
plt.plot(
    jahreszahlen,
    y_model2,
    label=f"Modell ab {2014} (Ausgleichsgerade)"
)

#Modell Werte (A-Parameter Zeichnen)
# Messdaten zeichnen
plt.plot(
    x_values,
    d_values,
    "r.",
    label="Modelldaten (d-Wert bei Sinus-Funktion)"
)

plt.legend()
plt.show()