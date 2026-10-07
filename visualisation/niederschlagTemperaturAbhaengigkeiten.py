import numpy as np
import matplotlib.pyplot as plt


def getAlleDaten():
    with open("data/data_all.csv", "r") as file:
        daten = file.readlines()[1:]

    alleTage = []

    for zeile in daten:
        werte = zeile.strip().split(",")
        alleTage.append(np.asarray(werte, dtype=float))

    return alleTage


# Alle Daten einlesen
alleTage = getAlleDaten()


# Dictionary:
# Temperatur -> Liste aller Niederschlagswerte bei dieser Temperatur
niederschlagTemperaturDictionary = {}

for tag in alleTage:
    niederschlag = tag[8]
    temperatur = np.floor(tag[3])

    # Tage ohne Niederschlagswert überspringen
    if np.isnan(niederschlag):
        continue

    # Falls die Temperatur noch nicht im Dictionary ist,
    # eine leere Liste anlegen
    if temperatur not in niederschlagTemperaturDictionary:
        niederschlagTemperaturDictionary[temperatur] = []

    # Niederschlag zur entsprechenden Temperatur hinzufügen
    niederschlagTemperaturDictionary[temperatur].append(niederschlag)


# x und y für den Plot erstellen
x = []
y = []
y_anzahlen_der_daten_fuer_temperatur = []

# Keys von klein nach groß durchlaufen
for temperatur in sorted(niederschlagTemperaturDictionary):
    niederschlaege = niederschlagTemperaturDictionary[temperatur]

    x.append(temperatur)
    y.append(np.mean(niederschlaege))
    y_anzahlen_der_daten_fuer_temperatur.append(len(niederschlaege)/1000)


# Plot erstellen
fig, ax = plt.subplots(figsize=(10, 4))

ax.set_title("Abhängigkeit des Niederschlags von der Temperatur")
ax.set_xlabel(r"Temperatur in [$^\circ$C]")
ax.set_ylabel("Durchschnittlicher Niederschlag in [mm]")

ax.set_xlim(-15, 30)
ax.set_ylim(0, 3)

ax.grid(True)

ax.plot(x, y, "r-", label="Niederschlag bei Temperatur")
ax.plot(x, y_anzahlen_der_daten_fuer_temperatur, "b-", label="Anzahl der Vorkomnisse bei dieser Temperatur in Tsd.")

ax.legend()

plt.subplots_adjust(left=0.12, bottom=0.3)
plt.show()