import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path
from scipy.interpolate import interp1d
from scipy.integrate import solve_ivp
from matplotlib.widgets import Slider


# ============================================================
# 1. EINSTELLUNGEN
# ============================================================

# CSV liegt im gleichen Ordner wie das Python-Skript
CSV_DATEI = Path(__file__).resolve().parent / "../../data/data_year.csv"
print(CSV_DATEI)

# Höhen in Metern
HOEHE_MESSSTATION = 500
HOEHE_GLETSCHER_MIN = 2200
HOEHE_GLETSCHER_MAX = 3600

HOEHE_GLETSCHER = (
    HOEHE_GLETSCHER_MIN + HOEHE_GLETSCHER_MAX
) / 2

# Temperaturabnahme pro Meter
TEMPERATURGRADIENT = 0.0065

# Bezugstemperatur für Schmelze
T0 = 0

# Anfangsmasse in Tonnen
M0 = 2.197768688e9

# Temperatur für die Schmelzberechnung:
# "Temperatur" = Jahresdurchschnitt
# "Maximaltemperatur" = vereinfachter Schmelzindikator
SCHMELZ_TEMPERATUR = "Maximaltemperatur"


# ============================================================
# 2. CSV-DATEI EINLESEN
# ============================================================

spalten = [
    "Jahr",
    "Temperatur",
    "Maximaltemperatur",
    "Minimaltemperatur",
    "Niederschlag",
    "Windgeschwindigkeit",
    "Regentage",
    "Schneetage",
    "Sturmtage",
    "Nebeltage",
    "Tornadotage",
    "Hageltage",
    "Massenänderung_pro_Fläche",
    "Längenänderung",
    "Länge",
    "Fläche",
    "Durchschnittliche_Masse"
]

if not CSV_DATEI.exists():
    raise FileNotFoundError(
        f"CSV-Datei nicht gefunden: {CSV_DATEI}"
    )

df = pd.read_csv(
    CSV_DATEI,
    names=spalten,
    header=None,
    sep=",",
    na_values=["-", ""],
    encoding="utf-8-sig"
)

# Alle Spalten in Zahlen umwandeln
for spalte in spalten:
    df[spalte] = pd.to_numeric(
        df[spalte],
        errors="coerce"
    )

# Ungültige Jahre entfernen
df = df.dropna(subset=["Jahr"])

# Nach Jahren sortieren
df = df.sort_values("Jahr")

# Doppelte Jahre entfernen
df = df.drop_duplicates(subset="Jahr")

df = df.reset_index(drop=True)

print("CSV erfolgreich eingelesen!")
print("Anzahl der Jahre:", len(df))
print(df.head())


# ============================================================
# 3. FEHLENDE DATEN INTERPOLIEREN
# ============================================================

# Originaldaten behalten, um interpolierte Werte zu erkennen
df_original = df.copy()

klima_spalten = [
    "Temperatur",
    "Maximaltemperatur",
    "Minimaltemperatur",
    "Niederschlag"
]

for spalte in klima_spalten:

    gueltige_daten = df[["Jahr", spalte]].dropna()

    if len(gueltige_daten) < 2:
        print(f"Warnung: Zu wenige Daten für {spalte}")
        continue

    # Nur innerhalb des Messzeitraums interpolieren
    funktion = interp1d(
        gueltige_daten["Jahr"].to_numpy(),
        gueltige_daten[spalte].to_numpy(),
        kind="linear",
        bounds_error=False,
        fill_value=np.nan
    )

    fehlend = df[spalte].isna()

    df.loc[fehlend, spalte] = funktion(
        df.loc[fehlend, "Jahr"].to_numpy()
    )

# Übersicht
print("\nDaten nach Interpolation:")
print(
    df[[
        "Jahr",
        "Temperatur",
        "Maximaltemperatur",
        "Niederschlag"
    ]].to_string(index=False)
)


# ============================================================
# 4. MODELLDATEN VORBEREITEN
# ============================================================

# Nur Jahre verwenden, in denen alle für die
# DGL benötigten Klimadaten verfügbar sind

df_modell = df.dropna(
    subset=[
        "Jahr",
        "Temperatur",
        SCHMELZ_TEMPERATUR,
        "Niederschlag"
    ]
).copy()

if len(df_modell) < 2:
    raise ValueError(
        "Zu wenige gültige Klimadaten für das Modell."
    )

jahre = df_modell["Jahr"].to_numpy(dtype=float)

temperatur_station = df_modell[
    "Temperatur"
].to_numpy(dtype=float)

temperatur_schmelze_station = df_modell[
    SCHMELZ_TEMPERATUR
].to_numpy(dtype=float)

# Niederschlag mm/Jahr -> m/Jahr
niederschlag_mm = df_modell[
    "Niederschlag"
].to_numpy(dtype=float)

niederschlag_m = niederschlag_mm / 1000


# ============================================================
# 5. TEMPERATURKORREKTUR
# ============================================================

hoehenunterschied = (
    HOEHE_GLETSCHER - HOEHE_MESSSTATION
)

temperaturkorrektur = (
    hoehenunterschied * TEMPERATURGRADIENT
)

temperatur_gletscher = (
    temperatur_station - temperaturkorrektur
)

temperatur_schmelze = (
    temperatur_schmelze_station - temperaturkorrektur
)

print("\nMittlere Gletscherhöhe:", HOEHE_GLETSCHER, "m")
print("Temperaturkorrektur:", temperaturkorrektur, "°C")


# ============================================================
# 6. INTERPOLATIONSFUNKTIONEN
# ============================================================

T_interpolation = interp1d(
    jahre,
    temperatur_gletscher,
    kind="linear",
    bounds_error=True
)

T_schmelze_interpolation = interp1d(
    jahre,
    temperatur_schmelze,
    kind="linear",
    bounds_error=True
)

PP_interpolation = interp1d(
    jahre,
    niederschlag_m,
    kind="linear",
    bounds_error=True
)


def T(t):
    return float(T_interpolation(t))


def T_schmelze(t):
    return float(T_schmelze_interpolation(t))


def PP(t):
    return float(PP_interpolation(t))


# ============================================================
# 7. DIFFERENTIALGLEICHUNG
# ============================================================

# M'(t) =
#
# 1000 * 2000 * PP(t) * c * M(t)
#
# -
#
# M(t) * (T(t)-T0) * (d + PP(t)*f)
#
# Der Temperaturüberschuss wird für die Schmelze
# auf mindestens 0 begrenzt.


def massenbilanz(t, M, c, d, f):

    masse = M[0]

    # ------------------------
    # Akkumulation
    # ------------------------

    akk = (
        1000
        * 2000
        * PP(t)
        * c
        * masse
    )

    # ------------------------
    # Ablation
    # ------------------------

    temperaturdifferenz = max(
        T_schmelze(t) - T0,
        0
    )

    abl = (
        masse
        * temperaturdifferenz
        * (d + PP(t) * f)
    )

    # ------------------------
    # Gesamte Massenbilanz
    # ------------------------

    M_prime = akk - abl

    return [M_prime]


# ============================================================
# 8. DGL NUMERISCH LÖSEN
# ============================================================

# Startmasse für das erste Modelljahr bestimmen

startjahr = jahre[0]

messwert_start = df.loc[
    df["Jahr"] == startjahr,
    "Durchschnittliche_Masse"
]

if (
    not messwert_start.empty
    and pd.notna(messwert_start.iloc[0])
):
    startmasse = float(messwert_start.iloc[0]) * 1e9
else:
    startmasse = M0

print("Startjahr:", int(startjahr))
print("Startmasse:", startmasse / 1e9, "Mrd. Tonnen")


def berechnen(c, d, f):

    t_values = np.linspace(
        jahre[0],
        jahre[-1],
        1500
    )

    loesung = solve_ivp(
        massenbilanz,
        [jahre[0], jahre[-1]],
        [startmasse],
        t_eval=t_values,
        args=(c, d, f),
        method="RK45",
        rtol=1e-7,
        atol=1e-4,
        max_step=0.05
    )

    if not loesung.success:
        raise RuntimeError(loesung.message)

    # Kleine numerische negative Werte vermeiden
    M_values = np.maximum(loesung.y[0], 0)

    return loesung.t, M_values


# ============================================================
# 9. PARAMETER
# ============================================================

c_start = 1e-8
d_start = 0.01
f_start = 0.01

t_modell, M_modell = berechnen(
    c_start,
    d_start,
    f_start
)


# ============================================================
# 10. GEMESSENE GLETSCHERMASSE
# ============================================================

df_messung = df.dropna(
    subset=["Durchschnittliche_Masse"]
).copy()

mess_jahre = df_messung[
    "Jahr"
].to_numpy(dtype=float)

# Einheit: Milliarden Tonnen
mess_masse = df_messung[
    "Durchschnittliche_Masse"
].to_numpy(dtype=float)


# ============================================================
# 11. DIAGRAMME ERSTELLEN
# ============================================================

fig, ax1 = plt.subplots(
    1,
    1,
    figsize=(12, 9),
)

plt.subplots_adjust(
    bottom=0.32
)


# ----------------------------
# Diagramm 1: Gletschermasse
# ----------------------------

linie, = ax1.plot(
    t_modell,
    M_modell / 1e9,
    linewidth=1,
    label="DGL-Modell"
)

ax1.scatter(
    mess_jahre,
    mess_masse,
    color="red",
    s=25,
    label="Gemessene Masse"
)

ax1.set_ylabel("Masse [Mrd. t]")
ax1.set_title("Gletschermasse M(t)")
ax1.grid(True)
ax1.legend()


# # ----------------------------
# # Diagramm 2: Temperatur
# # ----------------------------

# ax2.plot(
#     jahre,
#     temperatur_station,
#     label="Messstation (500 m)",
#     color="orange"
# )

# ax2.plot(
#     jahre,
#     temperatur_gletscher,
#     label="Gletscher (2900 m)",
#     color="blue"
# )

# ax2.axhline(
#     0,
#     color="black",
#     linestyle="--",
#     linewidth=1
# )

# ax2.set_ylabel("Temperatur [°C]")
# ax2.set_title("Jahresdurchschnittstemperatur")
# ax2.grid(True)
# ax2.legend()


# # ----------------------------
# # Diagramm 3: Niederschlag
# # ----------------------------

# ax3.plot(
#     jahre,
#     niederschlag_mm,
#     color="green",
#     marker="o",
#     markersize=3
# )

# ax3.set_xlabel("Jahr")
# ax3.set_ylabel("Niederschlag [mm/Jahr]")
# ax3.set_title("Jahresniederschlag der Messstation")
# ax3.grid(True)


# ============================================================
# 12. SLIDER
# ============================================================

ax_c = plt.axes([
    0.20, 0.17, 0.65, 0.025
])

ax_d = plt.axes([
    0.20, 0.11, 0.65, 0.025
])

ax_f = plt.axes([
    0.20, 0.05, 0.65, 0.025
])


slider_c = Slider(
    ax_c,
    "c",
    0,
    5e-8,
    valinit=c_start,
    valfmt="%.2e"
)

slider_d = Slider(
    ax_d,
    "d",
    0,
    0.1,
    valinit=d_start,
    valfmt="%.4f"
)

slider_f = Slider(
    ax_f,
    "f",
    0,
    0.1,
    valinit=f_start,
    valfmt="%.4f"
)


# ============================================================
# 13. SLIDER-AKTUALISIERUNG
# ============================================================

def update(val):

    c = slider_c.val
    d = slider_d.val
    f = slider_f.val

    t_neu, M_neu = berechnen(
        c, d, f
    )

    linie.set_xdata(t_neu)
    linie.set_ydata(M_neu / 1e9)

    ax1.relim()
    ax1.autoscale_view()

    fig.canvas.draw_idle()


slider_c.on_changed(update)
slider_d.on_changed(update)
slider_f.on_changed(update)


# ============================================================
# 14. AUSGABE
# ============================================================

plt.show()