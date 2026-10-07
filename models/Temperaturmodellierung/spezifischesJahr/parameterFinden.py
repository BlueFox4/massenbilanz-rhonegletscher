# Finde für ein beliebiges Jahr die bestmöglichen Parameter a, c, d
# b besitzt immer den festen Wert 365.2425

import numpy as np
from scipy.optimize import curve_fit
import csv
from datenAusJahr import getJahresdaten


B = 365.2425

START_A = 10.0
START_C = 100.0
START_D = 10.0


def f(x, a, c, d):
    return a * np.sin(2 * np.pi * (x - c) / B) + d


def findeBesteParameter(y_data):
    if len(y_data) == 0:
        return []
    # x-Werte: 0, 1, 2, ..., 364/365
    x_data = np.arange(len(y_data), dtype=float)

    # In numpy-Array umwandeln
    y_data = np.array(y_data, dtype=float)

    # Fehlende/ungültige Werte entfernen
    gueltig = np.isfinite(y_data)

    x_data = x_data[gueltig]
    y_data = y_data[gueltig]

    # Startwerte für a, c und d
    startwerte = [
        START_A,
        START_C,
        START_D
    ]

    # Optimierung von a, c und d
    parameter, kovarianz = curve_fit(
        f,
        x_data,
        y_data,
        p0=startwerte
    )

    # b wird nicht optimiert und immer fest gesetzt
    a, c, d = parameter

    return [a, B, c, d]


besteWerteAllerJahre = [["Jahr", "a", "b", "c", "d"]]

for jahr in range(1955, 2026):
    tage = getJahresdaten(jahr)

    tagestemperaturen = []

    for tag in tage:
        tagestemperaturen.append(tag[3])

    bestenWerte = findeBesteParameter(tagestemperaturen)

    if len(bestenWerte) == 4:
        besteWerteAllerJahre.append([jahr] + bestenWerte)

        print(
            f"Für das Jahr {jahr} sind die besten Werte: "
            f"a={bestenWerte[0]:.4f}, "
            f"b={bestenWerte[1]:.4f}, "
            f"c={bestenWerte[2]:.4f}, "
            f"d={bestenWerte[3]:.4f}"
        )
    else:
        print(
            f"Für das Jahr {jahr} sind die konnten keine besten Werte ermittelt werden."
        )



with open(
    "models/Temperaturmodellierung/spezifischesJahr/bestenParameter.csv",
    "w",
    newline=""
) as writeToFile:

    writer = csv.writer(writeToFile)
    writer.writerows(besteWerteAllerJahre)