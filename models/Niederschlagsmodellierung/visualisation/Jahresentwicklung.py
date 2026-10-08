import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------------------------- #
# Jahresdaten holen und darauf basierend eine Approximation der Regentage in der Zukunft bilden #
# --------------------------------------------------------------------------------------------- #

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
        #print(
        #    f"Das Jahr {daten[0]} wurde mit dem "
        #    f"Niederschlagswert {daten[4]} aussortiert."
        #)

    # Regentage
    try:
        jahresregentage.append(float(daten[6]))
    except ValueError:
        jahresregentage.append(np.nan)
        #print(
        #    f"Das Jahr {daten[0]} wurde mit dem "
        #    f"Regentage-Wert {daten[6]} aussortiert."
        #)

    # Schneetage
    try:
        jahresschneetage.append(float(daten[7]))
    except ValueError:
        jahresschneetage.append(np.nan)
        #print(
        #    f"Das Jahr {daten[0]} wurde mit dem "
        #    f"Schneetage-Wert {daten[7]} aussortiert."
        #)


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
fit_pp_days = np.polyfit(
    jahr_gueltig,
    niederschlagstage_gueltig,
    1
)

#print(f"Niederschlagstage - Ausgleichsgeraden-Funktion: y = {fit_pp_days[0]:.6f}x + {fit_pp_days[1]:.6f}")


fit_pp_days_line = np.polyval(
    fit_pp_days,
    jahr_gueltig
)



# ----------------------------------------------------------------------------- #
# Tagesdaten für monatliche Kumulierung und darauf basierender Ausgleichsgerade #
# ----------------------------------------------------------------------------- #


days = []
with open("data/data_all.csv") as file:
    entries = file.readlines()
    for entry in entries:
        days.append([e.strip() for e in entry.split(",")])
days = np.array(days)

years = days.T[0][1:]
months = days.T[1][1:]
pp = days.T[8][1:]

cumulated_months_pp = {}
for i, y in enumerate(years):
    key = float(int(y) + (int(months[i])-1)/12)
    current_pp = pp[i]
    if current_pp == "nan":
        current_pp = 0
    if key in cumulated_months_pp:
        cumulated_months_pp[key] += float(current_pp)
    else:
        cumulated_months_pp[key] = float(current_pp)

# Ausgleichsgerade erstellen
fit_monthly_pp = np.polyfit(list(cumulated_months_pp.keys()), list(cumulated_months_pp.values()), 1)
#print(f"Monatsniederschlag - Ausgleichsgeraden-Funktion: y = {fit_monthly_pp[0]:.6f}x + {fit_monthly_pp[1]:.6f}")
fit_monthly_pp_line = np.polyval(fit_monthly_pp, list(cumulated_months_pp.keys()))


# --------------------------------------------- #
# Funktionen für andere Programme bereitstellen #
# --------------------------------------------- #

# Für die Ausgleichsgerade der Niederschlagstage
def fit_pp_days_func(t, since):
    x = jahr_gueltig
    y = niederschlagstage_gueltig
    return np.polynomial.Polynomial.fit(x[x >= since], y[x >= since], deg=1)(t)

# Für die Ausgleichsgerade der monatlichen Niederschlagshöhe
def fit_monthly_pp_func(t, since):
    x = np.array(list(cumulated_months_pp.keys()))
    y = np.array(list(cumulated_months_pp.values()))
    return np.polynomial.Polynomial.fit(x[x >= since], y[x >= since], deg=1)(t)


# ------------------ # 
# Diagramm erstellen #
# ------------------ #

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize=(6, 6))

    ax.set_title("Niederschlag am Rhonegletscher")
    ax.set_xlim(1955, 2023)
    ax.set_ylim(0, 1500)

    ax.set_xlabel("Jahr")
    ax.set_ylabel("Niederschlagstage")

    ax2 = ax.twinx()
    ax2.set_ylabel("Niederschlag [mm]")


    # Jahresniederschlag
    ax2.plot(
        jahr,
        jahresniederschlag,
        "-.",
        label="Jahresniederschlag",
        color="black"
    )

    # Niederschlagstage
    ax.plot(
        jahr,
        niederschlagstage,
        ".",
        label="Niederschlagstage",
        color="cadetblue"
    )

    # Ausgleichsgerade Niederschlagstage
    ax.plot(
        jahr_gueltig,
        fit_pp_days_line,
        "-",
        linewidth=1.5,
        label=f"y = {fit_pp_days[0]:.6f}x + {fit_pp_days[1]:.6f}",
        color="cadetblue"
    )

    # Monatliche Niederschläge
    ax2.plot(
        cumulated_months_pp.keys(),
        cumulated_months_pp.values(),
        ".",
        label="Monatliche Niederschläge",
        color="orchid"
    )

    # Ausgleichsgerade Monatsniederschlag
    ax2.plot(
        cumulated_months_pp.keys(),
        fit_monthly_pp_line,
        "-",
        linewidth=1.5,
        label=f"y = {fit_monthly_pp[0]:.6f}x + {fit_monthly_pp[1]:.6f}",
        color="orchid"
    )

    ax.legend(frameon=False)
    ax2.legend(frameon=False)

    plt.show()