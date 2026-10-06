import numpy as np
import matplotlib.pyplot as plt


# Daten aus CSV-Datei einlesen
with open("data/data_year.csv", "r") as file:
    jahre = [line.strip().split(",") for line in file]

# Kopfzeile entfernen
jahre.pop(0)


# Daten vorbereiten
jahr = []
jahresniederschlag = []
jahresregentage = []
jahresschneetage = []

for daten in jahre:
    jahr.append(int(daten[0]))

    # Jahresniederschlag
    try:
        jahresniederschlag.append(float(daten[4]))
    except ValueError:
        jahresniederschlag.append(np.nan)
        print(
            f"Das Jahr {daten[0]} wurde mit dem "
            f"Niederschlagswert {daten[4]} aussortiert."
        )

    # Regentage
    try:
        jahresregentage.append(float(daten[6]))
    except ValueError:
        jahresregentage.append(np.nan)
        print(
            f"Das Jahr {daten[0]} wurde mit dem "
            f"Regentage-Wert {daten[6]} aussortiert."
        )

    # Schneetage
    try:
        jahresschneetage.append(float(daten[7]))
    except ValueError:
        jahresschneetage.append(np.nan)
        print(
            f"Das Jahr {daten[0]} wurde mit dem "
            f"Schneetage-Wert {daten[7]} aussortiert."
        )


# Regentage und Schneetage zu Niederschlagstagen zusammenfassen
niederschlagstage = (
    np.array(jahresregentage) +
    np.array(jahresschneetage)
)


# Nur vollständige Werte für die Ausgleichsgerade verwenden
gueltige_werte = ~np.isnan(niederschlagstage)

jahr_gueltig = np.array(jahr)[gueltige_werte]
niederschlagstage_gueltig = niederschlagstage[gueltige_werte]


# Lineare Ausgleichsgerade berechnen
ausgleichsgerade = np.polyfit(
    jahr_gueltig,
    niederschlagstage_gueltig,
    1
)

ausgleichsgerade_werte = np.polyval(
    ausgleichsgerade,
    jahr_gueltig
)


# Diagramm erstellen
fig, ax = plt.subplots(figsize=(6, 6))

ax.set_title("Niederschlag am Rhonegletscher")
ax.set_xlim(1955, 2023)
ax.set_ylim(0, 1500)

ax.set_xlabel("Jahr")
ax.set_ylabel("Niederschlagstage")

# Jahresniederschlag
ax.plot(
    jahr,
    jahresniederschlag,
    "r.",
    label="Jahresniederschlag"
)

# Niederschlagstage
ax.plot(
    jahr,
    niederschlagstage,
    "g.",
    label="Niederschlagstage"
)

# Ausgleichsgerade
ax.plot(
    jahr_gueltig,
    ausgleichsgerade_werte,
    "b-",
    linewidth=1.5,
    label="Ausgleichsgerade"
)

ax.legend()

plt.show()