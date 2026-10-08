import numpy as np
import matplotlib.pyplot as plt
from spezifischesJahr.datenAusJahr import getAlleMonate
from temperaturRechner import erhalteTemperatur

#12 Punkte pro Jahr
x = []
y_daten = []
y_modell = []
alleMonate= getAlleMonate()
for monat in alleMonate:
    x.append(monat[0])
    y_daten.append(monat[1])
    y_modell.append(erhalteTemperatur(monat[0], 482, 1994, 2025, 1))

print(x)

# Diagramm erstellen
fig, ax = plt.subplots(figsize=(10, 4))

plt.title("Temperaturverlauf Modell vs Realität (482m)")
plt.xlim(1994, 2023)
plt.ylim(-5, 25)
plt.xlabel(r"$Jahr$")
plt.ylabel(r"Temperatur in [°C]", rotation=90)

# Messdaten zeichnen
plt.plot(
    x,
    y_daten,
    label="Gemessene Monatstemperaturen"
)
plt.plot(
    x, 
    y_modell,
    label="Modellierter Temperaturverlauf"
)

plt.show()