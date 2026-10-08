import json

import sys
from pathlib import Path


# 1. Pfad der aktuellen Datei ermitteln
aktuelle_datei = Path(__file__).resolve()

# 2. Zum Überordner springen (ein Verzeichnis nach oben)
ueberordner = aktuelle_datei.parent.parent

# 3. Den Pfad zum Zielordner zusammensetzen
ziel_ordner_pfad = ueberordner / "Temperaturmodellierung"
print(ziel_ordner_pfad)
# 4. Den Zielordner zu den Python-Suchpfaden hinzufügen
sys.path.append(str(ziel_ordner_pfad))

# 5. Datei importieren
import temperaturRechner

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# ============================================================
# GLETSCHERMODELL – VERGANGENHEIT (SCHNELLE VERSION)
#
# CSV:
# Y,M,D,T,TM,Tm,SLP,H,PP,VV,V,VM,VG,RA,SN,TS,FG,t
#
# WICHTIG:
# t wird in JAHREN gemessen.
# Ein Tag entspricht deshalb dt = 1/366 Jahr.
# ============================================================

CSV_DATEI = Path(__file__).resolve().parent / "../../data/data_all.csv"
PARAMETER_DATEI = Path(__file__).resolve().parent / "modell_parameter.json"
ERGEBNIS_DATEI = Path(__file__).resolve().parent / "historie_modell.csv"

START_JAHR = 1955
END_JAHR = 2023

# Anfangsmasse 1955
M0 = 2.160111516e9  # Tonnen

# ------------------------------------------------------------
# Höhenmodell
# ------------------------------------------------------------

STATIONS_HOEHE = 482.0
GLETSCHER_MIN = 2200.0
GLETSCHER_MAX = 3600.0
HOEHEN_SCHRITT = 100.0

HOEHEN = np.arange(
    GLETSCHER_MIN,
    GLETSCHER_MAX + HOEHEN_SCHRITT,
    HOEHEN_SCHRITT
)

LAPSE_RATE = 0.0065  # °C / m
T0 = 2.0

# 1000 * 2000 aus eurer DGL
K_AKK = 1000.0 * 2000.0

# Da t in Jahren gemessen wird:
DT = 1.0 / 366.0

# Für den Plot reicht jeder 7. Tag.
# GERECHNET wird weiterhin mit jedem einzelnen Tag.
PLOT_STEP = 7

# ------------------------------------------------------------
# Startwerte Parameter
# ------------------------------------------------------------

# Nach Korrektur von dt müssen d/c deutlich größer sein als
# bei der alten dt=1-Version.
C_START = 5e-7
D_START = 3e-3
F_START = 1e-1


# ============================================================
# GEMESSENE GLETSCHERMASSEN
# ============================================================
#
# Eure aktuelle data_all.csv enthält KEINE Massenspalte.
# Deshalb stehen hier zunächst die Messwerte, die wir bereits
# aus euren Jahresdaten kennen.
#
# Sobald ihr weitere Werte habt, einfach ergänzen:
#
# 2005: 1.98,
# 2006: ...
#
# Einheit: Milliarden Tonnen
# ============================================================

GEMESSENE_MASSE_MRD_T = {
    1955: 2.160111516,
    1956: 2.170820961,
    1957: 2.1709869675,
    1958: 2.1680597985,
    1959: 2.159420964,
    1960: 2.172950232,
    1961: 2.170134012,
    1962: 2.165496918,
    1963: 2.1602577165,
    1964: 2.130914994,
    1965: 2.157227511,
    1966: 2.166430683,
    1967: 2.17570377,
    1968: 2.187632262,
    1969: 2.181105624,
    1973: 2.17270569,
    1974: 2.17568529,
    1975: 2.1886538115,
    1976: 2.1713738715,
    1977: 2.1863077905,
    1978: 2.2042231905,
    1979: 2.1969099405,
    1980: 2.2101996015,
    1981: 2.2242068145,
    1982: 2.219828955,
    1983: 2.200795395,
    1984: 2.20370811,
    1985: 2.1894148365,
    1986: 2.1735816165,
    1987: 2.174433795,
    1988: 2.171583693,
    1989: 2.1521202705,
    1990: 2.1268659825,
    1991: 2.0959310865,
    1992: 2.0829408825,
    1993: 2.0803193355,
    1994: 2.066717676,
    1995: 2.080039476,
    1996: 2.0734585935,
    1997: 2.071790544,
    1998: 2.050958955,
    1999: 2.04714,
    2000: 2.0418644583,
    2001: 2.0438673303,
    2002: 2.0416313571,
    2003: 2.0084515755,
    2004: 2.0083340535,
    2005: 1.9952697435,
    2006: 1.9710828711,
    2007: 1.9623074013,
    2008: 1.95353489655,
    2009: 1.93832487165,
    2010: 1.92592961955,
    2011: 1.90516934115,
    2012: 1.9025741544,
    2013: 1.890087324,
    2014: 1.8855046419,
    2015: 1.8717942711,
    2016: 1.8647794419,
    2017: 1.8477092271,
    2018: 1.8289600896,
    2019: 1.8187541145,
    2020: 1.809869211,
    2021: 1.8085392285,
    2022: 1.7745182037,
    2023: 1.7470039995
}


# ============================================================
# DATEN LADEN
# ============================================================

def lade_daten():
    if not CSV_DATEI.exists():
        raise FileNotFoundError(
            f"{CSV_DATEI.name} fehlt.\n"
            "Lege die Datei in denselben Ordner wie dieses Skript."
        )

    df = pd.read_csv(
        CSV_DATEI,
        na_values=["-", "", "NA", "NaN"]
    )

    benoetigt = ["Y", "M", "D", "T", "PP", "t"]
    fehlt = [x for x in benoetigt if x not in df.columns]

    if fehlt:
        raise ValueError(
            f"Diese Spalten fehlen in data_all.csv: {fehlt}"
        )

    for col in df.columns:
        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

    df = df.dropna(
        subset=["Y", "M", "D"]
    ).copy()

    df["Datum"] = pd.to_datetime(
        dict(
            year=df["Y"].astype(int),
            month=df["M"].astype(int),
            day=df["D"].astype(int)
        ),
        errors="coerce"
    )

    df = (
        df.dropna(subset=["Datum"])
          .sort_values("Datum")
          .drop_duplicates("Datum")
          .reset_index(drop=True)
    )

    # --------------------------------------------------------
    # Temperatur-Lücken
    # --------------------------------------------------------

    temp = df.set_index("Datum")["T"]

    df["T_modell"] = temp.interpolate(
        method="time",
        limit_direction="both"
    ).to_numpy()

    # --------------------------------------------------------
    # Niederschlags-Lücken
    #
    # Nicht linear zwischen Regentagen interpolieren.
    # Fehlende Werte werden mit dem klimatologischen Mittel
    # desselben Kalendertags ersetzt.
    # --------------------------------------------------------

    letztes_jahr = int(df["Y"].max())
    ref_start = max(
        int(df["Y"].min()),
        letztes_jahr - 49
    )

    ref = df[
        (df["Y"] >= ref_start)
        & (df["Y"] <= letztes_jahr)
        & df["PP"].notna()
    ].copy()

    ref["MonatTag"] = (
        ref["Datum"].dt.strftime("%m-%d")
    )

    tag_mittel = (
        ref.groupby("MonatTag")["PP"].mean()
    )

    monat_mittel = (
        ref.groupby("M")["PP"].mean()
    )

    global_mittel = float(
        ref["PP"].mean()
    )

    df["PP_modell"] = df["PP"].copy()

    fehlt_pp = df["PP_modell"].isna()

    # Nur ~466 fehlende Werte -> diese Schleife läuft nur einmal
    for idx in df.index[fehlt_pp]:

        datum = df.at[idx, "Datum"]
        key = datum.strftime("%m-%d")
        monat = df.at[idx, "M"]

        wert = tag_mittel.get(
            key,
            np.nan
        )

        if pd.isna(wert):
            wert = monat_mittel.get(
                monat,
                np.nan
            )

        if pd.isna(wert):
            wert = global_mittel

        df.at[idx, "PP_modell"] = wert

    df["PP_modell"] = (
        df["PP_modell"].clip(lower=0)
    )

    return df


# ============================================================
# EINMALIGE VORBERECHNUNG
# ============================================================

def vorbereiten(df):

    daten = df[
        (df["Y"] >= START_JAHR)
        & (df["Y"] <= END_JAHR)
    ].copy()

    daten = (
        daten.sort_values("Datum")
             .reset_index(drop=True)
    )

    if daten.empty:
        raise ValueError(
            "Keine Daten im Modellzeitraum vorhanden."
        )

    T_station = (
        daten["T_modell"]
        .to_numpy(dtype=float)
    )

    PP_m = (
        daten["PP_modell"]
        .to_numpy(dtype=float)
        / 1000.0
    )

    # Matrix:
    # Zeilen = Tage
    # Spalten = Höhenbänder
    T_baender = (
        T_station[:, None] - LAPSE_RATE * (HOEHEN[None, :] - STATIONS_HOEHE)
    )

    # --------------------------------------------------------
    # Akkumulation
    # --------------------------------------------------------

    # Anteil der Höhenbänder, in denen T <= 0 ist.
    schnee_anteil = np.mean(
        T_baender <= T0,
        axis=1
    )

    # Der c-Anteil der DGL kann vollständig vorab berechnet werden:
    #
    # c * [1000*2000*PP*Schneeanteil]
    akk_c_koeff = (
        K_AKK
        * PP_m
        * schnee_anteil
    )

    # --------------------------------------------------------
    # Ablation
    # --------------------------------------------------------

    positive_temp = np.maximum(
        T_baender - T0,
        0.0
    )

    # Mittel der positiven Temperatur über ALLE Höhenbänder.
    # Bereiche ohne Schmelze tragen 0 bei.
    schmelz_temp = np.mean(
        positive_temp,
        axis=1
    )

    # d-Anteil:
    abl_d_koeff = schmelz_temp

    # f-Anteil:
    abl_f_koeff = (
        schmelz_temp
        * PP_m
    )

    return (
        daten,
        akk_c_koeff,
        abl_d_koeff,
        abl_f_koeff
    )


# ============================================================
# SEHR SCHNELLE EULER-SIMULATION
#
# DGL:
#
# M' = M * (
#       c*A(t)
#       - d*D(t)
#       - f*F(t)
# )
#
# Euler:
#
# M_(i+1) = M_i + DT * M'_i
#
# Da der Faktor an Tag i nur von Wetter + Parametern abhängt,
# lässt sich die komplette Folge mit np.cumprod berechnen.
# Keine langsame Python-Schleife mehr.
# ============================================================

def simuliere(c, d, f):

    rate = (
        c * AKK_C
        - d * ABL_D
        - f * ABL_F
    )

    # M' hat hier die Einheit Tonnen / Jahr,
    # weil t in Jahren gemessen wird.
    wachstumsfaktor = (
        1.0 + DT * rate
    )

    # Negative Masse verhindern.
    wachstumsfaktor = np.maximum(
        wachstumsfaktor,
        0.0
    )

    # Masse zu Beginn jedes Tages:
    masse = M0 * np.concatenate([
        np.array([1.0]),
        np.cumprod(
            wachstumsfaktor[:-1]
        )
    ])

    # Differentialquotient M'(t)
    bilanz_pro_jahr = (
        masse * rate
    )

    # Tatsächliche Änderung während eines Tages:
    delta_pro_tag = (
        DT * bilanz_pro_jahr
    )

    return (
        masse,
        bilanz_pro_jahr,
        delta_pro_tag,
        rate
    )


# ============================================================
# MESSDATEN
# ============================================================

def messdaten():

    # Falls ihr später eine Massenspalte direkt an data_all.csv
    # anhängt, kann das Programm sie automatisch verwenden.
    moegliche_spalten = [
        "Masse_Mrd_t",
        "Masse_Mrd",
        "Durchschnittliche_Masse"
    ]

    for col in moegliche_spalten:

        if col in DF.columns:

            x = DF[
                ["Datum", col]
            ].dropna()

            if not x.empty:
                return (
                    x["Datum"].to_numpy(),
                    x[col].to_numpy(dtype=float)
                )

    # Aktuell bekannte Jahreswerte:
    jahre = np.array(
        sorted(
            GEMESSENE_MASSE_MRD_T.keys()
        ),
        dtype=int
    )

    werte = np.array(
        [
            GEMESSENE_MASSE_MRD_T[j]
            for j in jahre
        ],
        dtype=float
    )

    datumswerte = pd.to_datetime(
        [f"{j}-01-01" for j in jahre]
    )

    return (
        datumswerte.to_numpy(),
        werte
    )


def rmse_messwerte(masse):

    if len(MESS_DATUM) == 0:
        return np.nan

    # Modellwert am jeweils nächstgelegenen Datum
    modell_serie = pd.Series(
        masse,
        index=DATEN["Datum"]
    )

    fehler = []

    for datum, gemessen in zip(
        pd.to_datetime(MESS_DATUM),
        MESS_MASSE
    ):

        idx = (
            np.abs(
                DATEN["Datum"] - datum
            )
        ).argmin()

        modellwert = (
            masse[idx] / 1e9
        )

        fehler.append(
            modellwert - gemessen
        )

    return float(
        np.sqrt(
            np.mean(
                np.square(fehler)
            )
        )
    )


# ============================================================
# DATEN EINLESEN / VORBEREITEN
# ============================================================

DF = lade_daten()

(
    DATEN,
    AKK_C,
    ABL_D,
    ABL_F
) = vorbereiten(DF)

MESS_DATUM, MESS_MASSE = messdaten()

print(
    f"Daten: {DATEN['Datum'].min().date()} "
    f"bis {DATEN['Datum'].max().date()}"
)

print(
    f"Anzahl Modell-Tage: {len(DATEN)}"
)

print(
    f"Höhenbänder: "
    f"{HOEHEN.astype(int).tolist()}"
)

print(
    f"Euler-Zeitschritt: dt = 1/366 = {DT:.8f} Jahre"
)

print(
    f"Gemessene Massenpunkte im Plot: {len(MESS_MASSE)}"
)


# ============================================================
# ERSTE BERECHNUNG
# ============================================================

masse, bilanz, delta_tag, rate = simuliere(
    C_START,
    D_START,
    F_START
)

# Plot wird bewusst ausgedünnt.
# Berechnung bleibt täglich.
PLOT_IDX = np.arange(
    0,
    len(DATEN),
    PLOT_STEP
)

PLOT_DATUM = (
    DATEN["Datum"]
    .iloc[PLOT_IDX]
)


# ============================================================
# PLOT
# ============================================================

fig, (ax_m, ax_b) = plt.subplots(
    2,
    1,
    figsize=(13, 8),
    sharex=True
)

plt.subplots_adjust(
    bottom=0.29,
    hspace=0.25
)

# ------------------------------------------------------------
# Masse
# ------------------------------------------------------------

linie_m, = ax_m.plot(
    PLOT_DATUM,
    masse[PLOT_IDX] / 1e9,
    linewidth=1.8,
    label="Modellierte Masse"
)

# Gemessene Werte
mess_plot = ax_m.scatter(
    MESS_DATUM,
    MESS_MASSE,
    s=45,
    marker="o",
    zorder=5,
    label="Gemessene Masse"
)

# Gestrichelte Verbindung nur zur Orientierung
if len(MESS_MASSE) >= 2:
    ax_m.plot(
        MESS_DATUM,
        MESS_MASSE,
        linestyle="--",
        linewidth=1,
        alpha=0.6
    )

ax_m.set_ylabel(
    "Masse [Mrd. t]"
)

ax_m.set_title(
    "Gletschermodell – Vergangenheit"
)

ax_m.grid(True)
ax_m.legend()


# ------------------------------------------------------------
# Massenbilanz
# ------------------------------------------------------------

# M' ist wegen t in Jahren in Tonnen/Jahr.
bilanz_30 = (
    pd.Series(bilanz)
    .rolling(
        30,
        center=True,
        min_periods=1
    )
    .mean()
    .to_numpy()
)

linie_b, = ax_b.plot(
    PLOT_DATUM,
    bilanz_30[PLOT_IDX] / 1e6,
    linewidth=1.5,
    label="M'(t), 30-Tage-Mittel"
)

ax_b.axhline(
    0,
    linewidth=1
)

ax_b.set_xlabel(
    "Datum"
)

ax_b.set_ylabel(
    "M'(t) [Mio. t/Jahr]"
)

ax_b.grid(True)
ax_b.legend()


info_text = ax_m.text(
    0.01,
    0.02,
    "",
    transform=ax_m.transAxes,
    va="bottom"
)


# ============================================================
# SLIDER
# ============================================================

ax_c = plt.axes(
    [0.18, 0.18, 0.59, 0.025]
)

ax_d = plt.axes(
    [0.18, 0.125, 0.59, 0.025]
)

ax_f = plt.axes(
    [0.18, 0.07, 0.59, 0.025]
)


slider_c = Slider(
    ax_c,
    "log10(c)",
    -10,
    -4,
    valinit=np.log10(C_START),
    valstep=0.05
)

slider_d = Slider(
    ax_d,
    "log10(d)",
    -6,
    -0.5,
    valinit=np.log10(D_START),
    valstep=0.05
)

slider_f = Slider(
    ax_f,
    "log10(f)",
    -5,
    1,
    valinit=np.log10(F_START),
    valstep=0.05
)


# ------------------------------------------------------------
# Buttons
# ------------------------------------------------------------

ax_save = plt.axes(
    [0.80, 0.07, 0.16, 0.07]
)

button_save = Button(
    ax_save,
    "Parameter\nspeichern"
)

ax_reset = plt.axes(
    [0.80, 0.155, 0.16, 0.05]
)

button_reset = Button(
    ax_reset,
    "Zurücksetzen"
)


def aktuelle_parameter():

    return (
        10 ** slider_c.val,
        10 ** slider_d.val,
        10 ** slider_f.val
    )


# ============================================================
# UPDATE
# ============================================================

def aktualisieren(_=None):

    c, d, f = aktuelle_parameter()

    masse, bilanz, delta_tag, rate = simuliere(
        c,
        d,
        f
    )

    # Nur y-Daten ändern -> viel schneller
    linie_m.set_ydata(
        masse[PLOT_IDX] / 1e9
    )

    bilanz_30 = (
        pd.Series(bilanz)
        .rolling(
            30,
            center=True,
            min_periods=1
        )
        .mean()
        .to_numpy()
    )

    linie_b.set_ydata(
        bilanz_30[PLOT_IDX] / 1e6
    )

    # Grenzen direkt berechnen statt relim() über alle Artists
    y_mass = masse / 1e9

    alle_mass = np.concatenate([
        y_mass,
        MESS_MASSE
    ])

    ymin = float(np.nanmin(alle_mass))
    ymax = float(np.nanmax(alle_mass))

    rand = max(
        (ymax - ymin) * 0.08,
        0.005
    )

    ax_m.set_ylim(
        ymin - rand,
        ymax + rand
    )

    yb = bilanz_30 / 1e6
    bmax = max(
        abs(float(np.nanmin(yb))),
        abs(float(np.nanmax(yb))),
        0.01
    )

    ax_b.set_ylim(
        -1.08 * bmax,
        1.08 * bmax
    )

    fehler = rmse_messwerte(
        masse
    )

    info_text.set_text(
        f"c={c:.3e}   "
        f"d={d:.3e}   "
        f"f={f:.3e}\n"
        f"M({END_JAHR})="
        f"{masse[-1] / 1e9:.6f} Mrd. t   "
        f"RMSE={fehler:.5f} Mrd. t"
    )

    fig.canvas.draw_idle()


# ============================================================
# SPEICHERN
# ============================================================

def speichern(_):

    c, d, f = aktuelle_parameter()

    masse, bilanz, delta_tag, rate = simuliere(
        c,
        d,
        f
    )

    fehler = rmse_messwerte(
        masse
    )

    parameter = {
        "c": c,
        "d": d,
        "f": f,

        "dt_jahre": DT,

        "start_jahr": START_JAHR,
        "end_jahr": END_JAHR,

        "startmasse_tonnen": M0,
        "endmasse_tonnen": float(
            masse[-1]
        ),

        "rmse_mrd_t": fehler,

        "stations_hoehe_m": STATIONS_HOEHE,
        "gletscher_min_m": GLETSCHER_MIN,
        "gletscher_max_m": GLETSCHER_MAX,
        "hoehen_schritt_m": HOEHEN_SCHRITT,

        "lapse_rate_C_pro_m": LAPSE_RATE,
        "T0_C": T0
    }

    PARAMETER_DATEI.write_text(
        json.dumps(
            parameter,
            indent=2
        ),
        encoding="utf-8"
    )

    ausgabe = DATEN[
        [
            "Datum",
            "t",
            "T_modell",
            "PP_modell"
        ]
    ].copy()

    ausgabe[
        "Masse_t"
    ] = masse

    ausgabe[
        "Massenbilanz_t_pro_Jahr"
    ] = bilanz

    ausgabe[
        "Massenänderung_t_pro_Tag"
    ] = delta_tag

    ausgabe.to_csv(
        ERGEBNIS_DATEI,
        index=False
    )

    print(
        "\nParameter gespeichert:"
    )

    print(
        json.dumps(
            parameter,
            indent=2
        )
    )


def reset(_):

    slider_c.set_val(
        np.log10(C_START)
    )

    slider_d.set_val(
        np.log10(D_START)
    )

    slider_f.set_val(
        np.log10(F_START)
    )


slider_c.on_changed(
    aktualisieren
)

slider_d.on_changed(
    aktualisieren
)

slider_f.on_changed(
    aktualisieren
)

button_save.on_clicked(
    speichern
)

button_reset.on_clicked(
    reset
)

aktualisieren()

plt.show()
