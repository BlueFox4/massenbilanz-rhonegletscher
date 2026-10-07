import sys
import calendar
import time
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons


# ============================================================
# EIGENE DATEIEN IMPORTIEREN
# ============================================================

aktuelle_datei = Path(__file__).resolve()
ueberordner = aktuelle_datei.parent.parent

# Temperaturmodell
temperatur_ordner = ueberordner / "Temperaturmodellierung"

if str(temperatur_ordner) not in sys.path:
    sys.path.append(str(temperatur_ordner))

import temperaturRechner as TR


# Niederschlagsmodell
niederschlag_ordner = ueberordner / "Niederschlagsmodellierung"

if str(niederschlag_ordner) not in sys.path:
    sys.path.append(str(niederschlag_ordner))

import niederschlagsrechner as pp_calc


# ============================================================
# DATEI
# ============================================================

CSV_DATEI = aktuelle_datei.parent / "../../data/data_all.csv"


# ============================================================
# KALIBRIERTE PARAMETER
# ============================================================

C_STANDARD = 1.4125375446227554e-06
D_STANDARD = 0.005623413251903491
F_STANDARD = 4.4668359215096345

T0 = 2.0


# ============================================================
# NEUER TEMPERATURFAKTOR
#
# Aufruf:
# TR.erhalteTemperatur(t, hoehe, since, faktor)
#
# Falls ihr einen anderen sinnvollen Wertebereich habt,
# müsst ihr nur diese drei Konstanten ändern.
# ============================================================

TEMP_FAKTOR_STANDARD = 1.0
TEMP_FAKTOR_MIN = 0.0
TEMP_FAKTOR_MAX = 3.0


# ============================================================
# MODELLZEITRAUM
# ============================================================

START_JAHR = 1955
LETZTES_HISTORISCHES_JAHR = 2023
ERSTES_ZUKUNFTSJAHR = 2024
END_JAHR = 2100

M_START = 2160111516.0  # Tonnen

DT = 1.0 / 366.0

TEMPERATUR_SINCE = 1994
NIEDERSCHLAG_SINCE = 1994


# ============================================================
# HÖHENMODELL
#
# HIER KANN DIE SCHRITTWEITE GEÄNDERT WERDEN.
#
# Beispiele:
#   200.0 -> weniger Höhenstufen, schneller
#   100.0 -> bisheriger Standard
#    50.0 -> mehr Höhenstufen, genauer aufgelöst
#    25.0 -> noch feinere Auflösung
# ============================================================

STATIONS_HOEHE = 482.0

GLETSCHER_MIN = 2200.0
GLETSCHER_MAX = 3600.0

HOEHEN_SCHRITT_M = 100.0

LAPSE_RATE = 0.0065


def erstelle_hoehen():

    if HOEHEN_SCHRITT_M <= 0:
        raise ValueError(
            "HOEHEN_SCHRITT_M muss größer als 0 sein."
        )

    hoehen = np.arange(
        GLETSCHER_MIN,
        GLETSCHER_MAX + 1e-9,
        HOEHEN_SCHRITT_M,
        dtype=float
    )

    # 3600 m immer als oberste Grenze ergänzen,
    # auch wenn die Schrittweite nicht exakt aufgeht.
    if hoehen[-1] < GLETSCHER_MAX:
        hoehen = np.append(
            hoehen,
            GLETSCHER_MAX
        )

    return hoehen


HOEHEN = erstelle_hoehen()

# 1000 * 2000 aus eurer DGL
K_AKK = 1000.0 * 2000.0


# ============================================================
# GEMESSENE GLETSCHERMASSEN
# Einheit: Milliarden Tonnen
# ============================================================

GEMESSENE_MASSE_MRD_T = {
    1955: 2.16011516,
    1960: 2.172950232,
    1965: 2.157227511,
    1969: 2.181105624,
    1975: 2.1886538115,
    1980: 2.2101996015,
    1985: 2.1894148365,
    1990: 2.1268659825,
    1995: 2.080039476,
    1999: 2.04714,
    2000: 2.0401059444,
    2001: 2.0427764404,
    2002: 2.0397951428,
    2003: 1.995555434,
    2004: 1.995398738,
    2010: 1.92592961955,
    2015: 1.8717942711,
    2020: 1.809869211
}


# ============================================================
# CSV EINLESEN
# ============================================================

def lade_rohdaten():

    if not CSV_DATEI.exists():
        raise FileNotFoundError(
            f"{CSV_DATEI} wurde nicht gefunden.\n"
            "Lege data_all.csv in denselben Ordner wie dieses Skript."
        )

    df = pd.read_csv(
        CSV_DATEI,
        na_values=["-", "", "NA", "NaN"]
    )

    benoetigt = [
        "Y",
        "M",
        "D",
        "T",
        "PP"
    ]

    fehlt = [
        spalte
        for spalte in benoetigt
        if spalte not in df.columns
    ]

    if fehlt:
        raise ValueError(
            f"In data_all.csv fehlen diese Spalten: {fehlt}"
        )

    for spalte in benoetigt:
        df[spalte] = pd.to_numeric(
            df[spalte],
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

    return df


rohdaten = lade_rohdaten()


# ============================================================
# ZEITACHSE 1955–2100
# ============================================================

tage = pd.date_range(
    f"{START_JAHR}-01-01",
    f"{END_JAHR}-12-31",
    freq="D"
)

anzahl_tage = len(tage)

jahre_tag = tage.year.to_numpy()
tag_im_jahr = tage.dayofyear.to_numpy() - 1

t_werte = (
    jahre_tag
    + tag_im_jahr / 366.0
)

historisch_maske = (
    jahre_tag <= LETZTES_HISTORISCHES_JAHR
)

zukunft_maske = (
    jahre_tag >= ERSTES_ZUKUNFTSJAHR
)


# ============================================================
# JAHRESINDIZES
# ============================================================

jahre_eindeutig, start_idx = np.unique(
    jahre_tag,
    return_index=True
)

end_idx = np.r_[
    start_idx[1:] - 1,
    len(jahre_tag) - 1
]

anzahl_pro_jahr = np.diff(
    np.r_[
        start_idx,
        len(jahre_tag)
    ]
)

plot_datum_jahr = pd.to_datetime(
    [
        f"{jahr}-07-01"
        for jahr in jahre_eindeutig
    ]
)

hist_jahr_maske = (
    jahre_eindeutig <= LETZTES_HISTORISCHES_JAHR
)

index_2023 = int(
    np.where(
        jahre_eindeutig
        == LETZTES_HISTORISCHES_JAHR
    )[0][0]
)

zukunft_plot_idx = np.arange(
    index_2023,
    len(jahre_eindeutig)
)


# ============================================================
# HISTORISCHEN NIEDERSCHLAG FÜR DIE DGL AUFBEREITEN
# ============================================================

def historischer_niederschlag_vollstaendig():

    df = rohdaten[
        (rohdaten["Datum"] >= pd.Timestamp(f"{START_JAHR}-01-01"))
        & (rohdaten["Datum"] <= pd.Timestamp(f"{LETZTES_HISTORISCHES_JAHR}-12-31"))
    ][["Datum", "PP"]].copy()

    df["MonatTag"] = (
        df["Datum"].dt.strftime("%m-%d")
    )

    gueltig = df.dropna(
        subset=["PP"]
    ).copy()

    tag_mittel = (
        gueltig.groupby(
            "MonatTag"
        )["PP"].mean()
    )

    monat_mittel = (
        gueltig.groupby(
            gueltig["Datum"].dt.month
        )["PP"].mean()
    )

    global_mittel = float(
        gueltig["PP"].mean()
    )

    voll = pd.DataFrame({
        "Datum": pd.date_range(
            f"{START_JAHR}-01-01",
            f"{LETZTES_HISTORISCHES_JAHR}-12-31",
            freq="D"
        )
    })

    voll = voll.merge(
        df[["Datum", "PP"]],
        on="Datum",
        how="left"
    )

    voll["MonatTag"] = (
        voll["Datum"].dt.strftime("%m-%d")
    )

    voll["Monat"] = (
        voll["Datum"].dt.month
    )

    fehlend = int(
        voll["PP"].isna().sum()
    )

    voll["PP"] = voll["PP"].fillna(
        voll["MonatTag"].map(
            tag_mittel
        )
    )

    voll["PP"] = voll["PP"].fillna(
        voll["Monat"].map(
            monat_mittel
        )
    )

    voll["PP"] = voll["PP"].fillna(
        global_mittel
    )

    voll["PP"] = (
        voll["PP"].clip(lower=0)
    )

    print(
        f"Historischer Niederschlag: "
        f"{fehlend} fehlende Tageswerte "
        f"wurden klimatologisch ergänzt."
    )

    return voll


hist_pp_voll = (
    historischer_niederschlag_vollstaendig()
)

hist_pp_mm = (
    hist_pp_voll["PP"]
    .to_numpy(dtype=float)
)


# ============================================================
# GEMESSENER JAHRESNIEDERSCHLAG FÜR DEN GRAPHEN
#
# Komplette fehlende Jahre werden NICHT als Messwerte erfunden.
# Bei ausreichender Datenabdeckung wird die klimatologisch
# vervollständigte Jahressumme angezeigt.
# ============================================================

def gemessener_niederschlag_jahr():

    hist_raw = rohdaten[
        (rohdaten["Datum"] >= pd.Timestamp(f"{START_JAHR}-01-01"))
        & (rohdaten["Datum"] <= pd.Timestamp(f"{LETZTES_HISTORISCHES_JAHR}-12-31"))
    ][["Datum", "PP"]].copy()

    hist_raw["Jahr"] = (
        hist_raw["Datum"].dt.year
    )

    anzahl_messungen = (
        hist_raw.groupby("Jahr")["PP"]
        .count()
    )

    voll = hist_pp_voll.copy()

    voll["Jahr"] = (
        voll["Datum"].dt.year
    )

    jahressumme = (
        voll.groupby("Jahr")["PP"]
        .sum()
    )

    werte = np.full(
        len(jahre_eindeutig),
        np.nan,
        dtype=float
    )

    for i, jahr in enumerate(
        jahre_eindeutig
    ):

        if jahr > LETZTES_HISTORISCHES_JAHR:
            continue

        # Nur als Messjahr anzeigen, wenn der Großteil
        # des Jahres tatsächlich gemessen wurde.
        if anzahl_messungen.get(
            jahr,
            0
        ) >= 300:

            werte[i] = jahressumme.get(
                jahr,
                np.nan
            )

    return werte


pp_mess_jahr = (
    gemessener_niederschlag_jahr()
)


# ============================================================
# NIEDERSCHLAGSMODELL 1955–2100
#
# Das Modell wird jetzt AUCH in die Vergangenheit extrapoliert.
# Diese Kurve wird im Diagramm komplett gestrichelt gezeichnet.
# ============================================================

print(
    "Berechne Niederschlagsmodell 1955–2100 ..."
)

start_zeit = time.time()

PP_modell_tag_m = np.empty(
    anzahl_tage,
    dtype=float
)

alle_jahr_monate = pd.DataFrame({
    "Jahr": tage.year,
    "Monat": tage.month
}).drop_duplicates()


for _, zeile in alle_jahr_monate.iterrows():

    jahr = int(
        zeile["Jahr"]
    )

    monat = int(
        zeile["Monat"]
    )

    tage_monat = calendar.monthrange(
        jahr,
        monat
    )[1]

    datum_mitte = pd.Timestamp(
        jahr,
        monat,
        min(15, tage_monat)
    )

    t_monat = (
        jahr
        + (datum_mitte.dayofyear - 1) / 366.0
    )

    pp_monat_mm = (
        pp_calc.erhalteNiederschlagMonatlicherTrend(
            t_monat,
            NIEDERSCHLAG_SINCE
        )
    )

    if pp_monat_mm is None:
        raise ValueError(
            f"Niederschlagsmodell liefert "
            f"für {jahr}-{monat:02d} None."
        )

    pp_monat_mm = max(
        float(pp_monat_mm),
        0.0
    )

    pp_tag_m = (
        pp_monat_mm
        / tage_monat
        / 1000.0
    )

    maske = (
        (tage.year == jahr)
        & (tage.month == monat)
    )

    PP_modell_tag_m[
        maske
    ] = pp_tag_m


print(
    f"Niederschlagsmodell fertig: "
    f"{time.time() - start_zeit:.2f} Sekunden"
)


# ============================================================
# NIEDERSCHLAG FÜR DIE DGL
#
# Vergangenheit: Messwerte
# Zukunft: Modell
# ============================================================

PP_DGL_tag_m = (
    PP_modell_tag_m.copy()
)

PP_DGL_tag_m[
    historisch_maske
] = (
    hist_pp_mm / 1000.0
)


# Jahresniederschlag des MODELLS
pp_modell_jahr = np.add.reduceat(
    PP_modell_tag_m * 1000.0,
    start_idx
)


# ============================================================
# GEMESSENE TEMPERATUR AUF 2900 m
# ============================================================

def gemessene_temperatur_2900_jahr():

    df = rohdaten[
        (rohdaten["Datum"] >= pd.Timestamp(f"{START_JAHR}-01-01"))
        & (rohdaten["Datum"] <= pd.Timestamp(f"{ERSTES_ZUKUNFTSJAHR}-12-31"))
    ][["Datum", "T"]].copy()

    df = df.dropna(
        subset=["T"]
    )

    df["Jahr"] = (
        df["Datum"].dt.year
    )

    df["T_2900"] = (
        df["T"]
        - LAPSE_RATE
        * (2900.0 - STATIONS_HOEHE)
    )

    gruppiert = df.groupby(
        "Jahr"
    )["T_2900"]

    mittel = gruppiert.mean()
    anzahl = gruppiert.count()

    mess_jahre_temp = np.arange(
        START_JAHR,
        ERSTES_ZUKUNFTSJAHR + 1
    )

    werte = np.full(
        len(mess_jahre_temp),
        np.nan,
        dtype=float
    )

    for i, jahr in enumerate(
        mess_jahre_temp
    ):

        # Nur Jahresmittel anzeigen, wenn genügend
        # Messwerte vorhanden sind.
        if anzahl.get(
            jahr,
            0
        ) >= 300:

            werte[i] = mittel.get(
                jahr,
                np.nan
            )

    daten = pd.to_datetime(
        [
            f"{jahr}-07-01"
            for jahr in mess_jahre_temp
        ]
    )

    return daten, werte


mess_temp_datum, mess_temp_2900 = (
    gemessene_temperatur_2900_jahr()
)


# ============================================================
# TEMPERATURMODELL
# ============================================================

T_station = None
T_baender = None
T_2900_modell = None
temp_modell_jahr = None

A_TERM = None
D_TERM = None
F_TERM = None

AKTUELLER_TEMP_FAKTOR = None


def berechne_temperatur_und_dgl_terme(
    faktor,
    ausgabe=True
):
    """
    Führt das Temperaturmodell mit dem neuen Faktor aus:

        TR.erhalteTemperatur(
            t,
            STATIONS_HOEHE,
            TEMPERATUR_SINCE,
            faktor
        )

    und berechnet danach alle temperaturabhängigen
    Terme der DGL neu.
    """

    global T_station
    global T_baender
    global T_2900_modell
    global temp_modell_jahr

    global A_TERM
    global D_TERM
    global F_TERM

    global AKTUELLER_TEMP_FAKTOR

    if ausgabe:
        print(
            f"Berechne Temperaturmodell mit Faktor "
            f"{faktor:.3f} ..."
        )

    start = time.time()

    neue_station = np.empty(
        anzahl_tage,
        dtype=float
    )

    # Nur EIN externer Temperaturmodell-Aufruf pro Tag.
    for i, t in enumerate(t_werte):

        neue_station[i] = TR.erhalteTemperatur(
            float(t),
            STATIONS_HOEHE,
            TEMPERATUR_SINCE,
            # float(faktor)
        )

    hoehenkorrektur = (
        LAPSE_RATE
        * (
            HOEHEN
            - STATIONS_HOEHE
        )
    )

    neue_baender = (
        neue_station[:, None]
        - hoehenkorrektur[None, :]
    )

    # Die Kurve bei genau 2900 m braucht nicht zwingend
    # eine Höhenstufe bei 2900 m.
    neue_T_2900 = (
        neue_station
        - LAPSE_RATE
        * (2900.0 - STATIONS_HOEHE)
    )

    neues_temp_jahr = (
        np.add.reduceat(
            neue_T_2900,
            start_idx
        )
        / anzahl_pro_jahr
    )

    schnee_anteil = np.mean(
        neue_baender <= T0,
        axis=1
    )

    positive_temperatur = np.maximum(
        neue_baender - T0,
        0.0
    )

    schmelztemperatur = np.mean(
        positive_temperatur,
        axis=1
    )

    neues_A = (
        K_AKK
        * PP_DGL_tag_m
        * schnee_anteil
    )

    neues_D = (
        schmelztemperatur
    )

    neues_F = (
        schmelztemperatur
        * PP_DGL_tag_m
    )

    # Erst nach erfolgreicher Berechnung ersetzen
    T_station = neue_station
    T_baender = neue_baender
    T_2900_modell = neue_T_2900
    temp_modell_jahr = neues_temp_jahr

    A_TERM = neues_A
    D_TERM = neues_D
    F_TERM = neues_F

    AKTUELLER_TEMP_FAKTOR = float(
        faktor
    )

    if ausgabe:
        print(
            f"Temperatur + DGL-Terme fertig: "
            f"{time.time() - start:.2f} Sekunden"
        )


# Initiale Berechnung
berechne_temperatur_und_dgl_terme(
    TEMP_FAKTOR_STANDARD
)


# ============================================================
# SCHNELLE MASSENSIMULATION
# ============================================================

def simuliere(c, d, f):

    rate = (
        c * A_TERM
        - d * D_TERM
        - f * F_TERM
    )

    euler_faktor = (
        1.0
        + DT * rate
    )

    euler_faktor = np.maximum(
        euler_faktor,
        0.0
    )

    masse = (
        M_START
        * np.concatenate([
            [1.0],
            np.cumprod(
                euler_faktor[:-1]
            )
        ])
    )

    bilanz = (
        masse * rate
    )

    delta_tag = (
        DT * bilanz
    )

    masse_jahr = (
        masse[end_idx]
        / 1e9
    )

    bilanz_jahr = (
        np.add.reduceat(
            delta_tag,
            start_idx
        )
        / 1e9
    )

    return (
        masse,
        bilanz,
        delta_tag,
        masse_jahr,
        bilanz_jahr
    )


# ============================================================
# GEMESSENE MASSEN
# ============================================================

mess_jahre = np.array(
    sorted(
        GEMESSENE_MASSE_MRD_T.keys()
    ),
    dtype=int
)

mess_masse = np.array(
    [
        GEMESSENE_MASSE_MRD_T[jahr]
        for jahr in mess_jahre
    ],
    dtype=float
)

mess_datum = pd.to_datetime(
    [
        f"{jahr}-07-01"
        for jahr in mess_jahre
    ]
)


# ============================================================
# ERSTE SIMULATION
# ============================================================

(
    masse,
    bilanz,
    delta_tag,
    masse_jahr,
    bilanz_jahr
) = simuliere(
    C_STANDARD,
    D_STANDARD,
    F_STANDARD
)


# ============================================================
# DIAGRAMM
# ============================================================

fig, ax_masse = plt.subplots(
    figsize=(20, 11)
)

plt.subplots_adjust(
    left=0.07,
    right=0.70,
    bottom=0.30,
    top=0.91
)

ax_bilanz = ax_masse.twinx()

ax_temp = ax_masse.twinx()
ax_temp.spines["right"].set_position(
    ("axes", 1.10)
)

ax_pp = ax_masse.twinx()
ax_pp.spines["right"].set_position(
    ("axes", 1.21)
)


# ============================================================
# FARBEN
# ============================================================

FARBE_MASSE = "tab:blue"
FARBE_BILANZ = "tab:red"

# Messung und Modell jeweils GLEICHE Farbe
FARBE_TEMP = "tab:orange"
FARBE_PP = "tab:green"


# ============================================================
# MASSE UND BILANZ
# Vergangenheit durchgezogen, Zukunft gestrichelt
# ============================================================

linie_masse_hist, = ax_masse.plot(
    plot_datum_jahr[
        hist_jahr_maske
    ],
    masse_jahr[
        hist_jahr_maske
    ],
    linewidth=3,
    color=FARBE_MASSE,
    linestyle="-",
    label="Gletschermasse"
)

linie_masse_zukunft, = ax_masse.plot(
    plot_datum_jahr[
        zukunft_plot_idx
    ],
    masse_jahr[
        zukunft_plot_idx
    ],
    linewidth=3,
    color=FARBE_MASSE,
    linestyle="--"
)


linie_bilanz_hist, = ax_bilanz.plot(
    plot_datum_jahr[
        hist_jahr_maske
    ],
    bilanz_jahr[
        hist_jahr_maske
    ],
    linewidth=2.1,
    color=FARBE_BILANZ,
    linestyle="-",
    label="Massenbilanz"
)

linie_bilanz_zukunft, = ax_bilanz.plot(
    plot_datum_jahr[
        zukunft_plot_idx
    ],
    bilanz_jahr[
        zukunft_plot_idx
    ],
    linewidth=2.1,
    color=FARBE_BILANZ,
    linestyle="--"
)


# ============================================================
# TEMPERATUR
#
# Messwerte: durchgezogen
# Modell: über den GESAMTEN Zeitraum gestrichelt
# ============================================================

linie_temp_mess, = ax_temp.plot(
    mess_temp_datum,
    mess_temp_2900,
    linewidth=2.2,
    color=FARBE_TEMP,
    linestyle="-",
    label="Temperatur Messung 2900 m"
)

linie_temp_modell, = ax_temp.plot(
    plot_datum_jahr,
    temp_modell_jahr,
    linewidth=2.2,
    color=FARBE_TEMP,
    linestyle="--",
    label="Temperatur Modell 2900 m"
)


# ============================================================
# NIEDERSCHLAG
#
# Messwerte: durchgezogen
# Modell: über 1955–2100 gestrichelt
# ============================================================

linie_pp_mess, = ax_pp.plot(
    plot_datum_jahr,
    pp_mess_jahr,
    linewidth=1.8,
    color=FARBE_PP,
    linestyle="-",
    label="Niederschlag Messung"
)

linie_pp_modell, = ax_pp.plot(
    plot_datum_jahr,
    pp_modell_jahr,
    linewidth=1.8,
    color=FARBE_PP,
    linestyle="--",
    label="Niederschlag Modell"
)


# ============================================================
# GEMESSENE GLETSCHERMASSE
# ============================================================

messpunkte = ax_masse.scatter(
    mess_datum,
    mess_masse,
    s=45,
    color="black",
    zorder=10,
    label="Gemessene Gletschermasse"
)


# ============================================================
# ZUKUNFTSGRENZE
# ============================================================

grenze = pd.Timestamp(
    f"{ERSTES_ZUKUNFTSJAHR}-01-01"
)

ax_masse.axvline(
    grenze,
    color="black",
    linestyle=":",
    linewidth=1.6,
    alpha=0.75
)

ax_masse.text(
    grenze,
    0.98,
    "  Zukunft ab 2024",
    transform=ax_masse.get_xaxis_transform(),
    va="top",
    fontsize=10
)


# ============================================================
# ACHSEN
# ============================================================

ax_masse.set_title(
    "Gletschermodell 1955–2100",
    fontsize=19
)

ax_masse.set_xlabel(
    "Jahr",
    fontsize=13
)

ax_masse.set_ylabel(
    "Gletschermasse [Mrd. t]",
    color=FARBE_MASSE,
    fontsize=12
)

ax_bilanz.set_ylabel(
    "Massenbilanz [Mrd. t/Jahr]",
    color=FARBE_BILANZ,
    fontsize=12
)

ax_temp.set_ylabel(
    "Temperatur auf 2900 m [°C]",
    color=FARBE_TEMP,
    fontsize=12
)

ax_pp.set_ylabel(
    "Niederschlag [mm/Jahr]",
    color=FARBE_PP,
    fontsize=12
)

ax_masse.tick_params(
    axis="y",
    colors=FARBE_MASSE
)

ax_bilanz.tick_params(
    axis="y",
    colors=FARBE_BILANZ
)

ax_temp.tick_params(
    axis="y",
    colors=FARBE_TEMP
)

ax_pp.tick_params(
    axis="y",
    colors=FARBE_PP
)

ax_masse.grid(
    True,
    alpha=0.3
)

ax_bilanz.axhline(
    0,
    color=FARBE_BILANZ,
    linewidth=1,
    linestyle=":",
    alpha=0.5
)


# ============================================================
# LEGENDE
# ============================================================

ax_masse.legend(
    [
        linie_masse_hist,
        linie_bilanz_hist,
        linie_temp_mess,
        linie_temp_modell,
        linie_pp_mess,
        linie_pp_modell,
        messpunkte
    ],
    [
        "Gletschermasse",
        "Massenbilanz",
        "Temperatur Messung",
        "Temperatur Modell",
        "Niederschlag Messung",
        "Niederschlag Modell",
        "Gemessene Gletschermasse"
    ],
    loc="upper left",
    fontsize=9
)


# ============================================================
# INFOTEXT
# ============================================================

info_text = ax_masse.text(
    0.01,
    0.02,
    "",
    transform=ax_masse.transAxes,
    fontsize=10,
    verticalalignment="bottom"
)


# ============================================================
# SLIDER
# ============================================================

ax_c = plt.axes([
    0.10,
    0.205,
    0.54,
    0.023
])

slider_c = Slider(
    ax_c,
    "c",
    0.0,
    5.0e-6,
    valinit=C_STANDARD,
    valfmt="%.3e"
)


ax_d = plt.axes([
    0.10,
    0.155,
    0.54,
    0.023
])

slider_d = Slider(
    ax_d,
    "d",
    0.0,
    0.02,
    valinit=D_STANDARD,
    valfmt="%.6f"
)


ax_f = plt.axes([
    0.10,
    0.105,
    0.54,
    0.023
])

slider_f = Slider(
    ax_f,
    "f",
    0.0,
    10.0,
    valinit=F_STANDARD,
    valfmt="%.4f"
)


ax_temp_faktor = plt.axes([
    0.10,
    0.055,
    0.54,
    0.023
])

slider_temp_faktor = Slider(
    ax_temp_faktor,
    "Temp.-Faktor",
    TEMP_FAKTOR_MIN,
    TEMP_FAKTOR_MAX,
    valinit=TEMP_FAKTOR_STANDARD,
    valstep=0.01,
    valfmt="%.2f"
)


# ============================================================
# BUTTONS
# ============================================================

ax_reset = plt.axes([
    0.72,
    0.055,
    0.12,
    0.05
])

button_reset = Button(
    ax_reset,
    "Berechnete Modellwerte"
)

ax_save = plt.axes([
    0.86,
    0.055,
    0.11,
    0.05
])

button_save = Button(
    ax_save,
    "CSV speichern"
)


# ============================================================
# GRAPHEN EIN-/AUSBLENDEN
# ============================================================

ax_graphen = plt.axes([
    0.72,
    0.12,
    0.25,
    0.205
])

ax_graphen.set_title(
    "Graphen anzeigen",
    fontsize=10,
    loc="left"
)

check_graphen = CheckButtons(
    ax_graphen,
    [
        "Gletschermasse",
        "Massenbilanz",
        "Temperatur Modell",
        "Temperatur Messung",
        "Niederschlag Modell",
        "Niederschlag Messung",
        "Messdaten Masse"
    ],
    [
        True,
        True,
        True,
        True,
        True,
        True,
        True
    ]
)


# ============================================================
# RMSE
# ============================================================

def berechne_rmse(
    masse_jahr
):

    fehler = []

    for jahr, gemessen in zip(
        mess_jahre,
        mess_masse
    ):

        idx = np.where(
            jahre_eindeutig
            == jahr
        )[0]

        if len(idx) == 0:
            continue

        modellwert = (
            masse_jahr[
                idx[0]
            ]
        )

        fehler.append(
            modellwert
            - gemessen
        )

    if len(fehler) == 0:
        return np.nan

    return float(
        np.sqrt(
            np.mean(
                np.square(
                    fehler
                )
            )
        )
    )


# ============================================================
# ACHSEN ANPASSEN
# ============================================================

def achsen_anpassen(
    masse_jahr,
    bilanz_jahr
):

    alle_massen = np.concatenate([
        masse_jahr,
        mess_masse
    ])

    ymin = float(
        np.nanmin(
            alle_massen
        )
    )

    ymax = float(
        np.nanmax(
            alle_massen
        )
    )

    rand = max(
        (ymax - ymin) * 0.08,
        0.03
    )

    ax_masse.set_ylim(
        max(0, ymin - rand),
        ymax + rand
    )

    bmax = max(
        abs(
            float(
                np.nanmin(
                    bilanz_jahr
                )
            )
        ),
        abs(
            float(
                np.nanmax(
                    bilanz_jahr
                )
            )
        ),
        0.001
    )

    ax_bilanz.set_ylim(
        -1.15 * bmax,
        1.15 * bmax
    )


# ============================================================
# ACHSENSICHTBARKEIT
# ============================================================

def aktualisiere_achsensichtbarkeit():

    masse_sichtbar = (
        linie_masse_hist.get_visible()
        or linie_masse_zukunft.get_visible()
        or messpunkte.get_visible()
    )

    ax_masse.yaxis.set_visible(
        masse_sichtbar
    )

    bilanz_sichtbar = (
        linie_bilanz_hist.get_visible()
        or linie_bilanz_zukunft.get_visible()
    )

    ax_bilanz.yaxis.set_visible(
        bilanz_sichtbar
    )

    ax_bilanz.spines["right"].set_visible(
        bilanz_sichtbar
    )

    temp_sichtbar = (
        linie_temp_modell.get_visible()
        or linie_temp_mess.get_visible()
    )

    ax_temp.yaxis.set_visible(
        temp_sichtbar
    )

    ax_temp.spines["right"].set_visible(
        temp_sichtbar
    )

    pp_sichtbar = (
        linie_pp_modell.get_visible()
        or linie_pp_mess.get_visible()
    )

    ax_pp.yaxis.set_visible(
        pp_sichtbar
    )

    ax_pp.spines["right"].set_visible(
        pp_sichtbar
    )


# ============================================================
# GRAPHEN SCHALTEN
# ============================================================

def graph_sichtbarkeit(
    label
):

    if label == "Gletschermasse":

        sichtbar = not (
            linie_masse_hist.get_visible()
        )

        linie_masse_hist.set_visible(
            sichtbar
        )

        linie_masse_zukunft.set_visible(
            sichtbar
        )


    elif label == "Massenbilanz":

        sichtbar = not (
            linie_bilanz_hist.get_visible()
        )

        linie_bilanz_hist.set_visible(
            sichtbar
        )

        linie_bilanz_zukunft.set_visible(
            sichtbar
        )


    elif label == "Temperatur Modell":

        linie_temp_modell.set_visible(
            not linie_temp_modell.get_visible()
        )


    elif label == "Temperatur Messung":

        linie_temp_mess.set_visible(
            not linie_temp_mess.get_visible()
        )


    elif label == "Niederschlag Modell":

        linie_pp_modell.set_visible(
            not linie_pp_modell.get_visible()
        )


    elif label == "Niederschlag Messung":

        linie_pp_mess.set_visible(
            not linie_pp_mess.get_visible()
        )


    elif label == "Messdaten Masse":

        messpunkte.set_visible(
            not messpunkte.get_visible()
        )


    aktualisiere_achsensichtbarkeit()

    fig.canvas.draw_idle()


check_graphen.on_clicked(
    graph_sichtbarkeit
)


# ============================================================
# SCHNELLES UPDATE FÜR c, d UND f
# ============================================================

def aktualisieren(
    _=None
):

    c = slider_c.val
    d = slider_d.val
    f = slider_f.val

    (
        masse,
        bilanz,
        delta_tag,
        masse_jahr,
        bilanz_jahr
    ) = simuliere(
        c,
        d,
        f
    )

    linie_masse_hist.set_ydata(
        masse_jahr[
            hist_jahr_maske
        ]
    )

    linie_bilanz_hist.set_ydata(
        bilanz_jahr[
            hist_jahr_maske
        ]
    )

    linie_masse_zukunft.set_ydata(
        masse_jahr[
            zukunft_plot_idx
        ]
    )

    linie_bilanz_zukunft.set_ydata(
        bilanz_jahr[
            zukunft_plot_idx
        ]
    )

    achsen_anpassen(
        masse_jahr,
        bilanz_jahr
    )

    rmse = berechne_rmse(
        masse_jahr
    )

    idx_2023 = np.where(
        jahre_eindeutig
        == LETZTES_HISTORISCHES_JAHR
    )[0][0]

    masse_2023 = (
        masse_jahr[
            idx_2023
        ]
    )

    info_text.set_text(
        f"c = {c:.3e}   "
        f"d = {d:.6f}   "
        f"f = {f:.4f}   "
        f"Temp.-Faktor = {AKTUELLER_TEMP_FAKTOR:.2f}\n"
        f"Höhenschritt = {HOEHEN_SCHRITT_M:g} m "
        f"({len(HOEHEN)} Höhenstufen)   |   "
        f"M(1955) = {M_START / 1e9:.4f} Mrd. t   |   "
        f"M(2023) = {masse_2023:.4f} Mrd. t   |   "
        f"M(2100) = {masse[-1] / 1e9:.4f} Mrd. t   |   "
        f"RMSE = {rmse:.4f} Mrd. t"
    )

    fig.canvas.draw_idle()


# ============================================================
# TEMPERATURFAKTOR
#
# WICHTIG:
# Der Slider selbst löst NICHT bei jeder kleinen Bewegung
# die teure 53.000-Tage-Berechnung aus.
#
# Erst beim LOSLASSEN der Maus wird neu gerechnet.
# ============================================================

def temperaturfaktor_losgelassen(
    event
):

    neuer_faktor = float(
        slider_temp_faktor.val
    )

    if np.isclose(
        neuer_faktor,
        AKTUELLER_TEMP_FAKTOR
    ):
        return

    print()
    print(
        f"Temperaturfaktor geändert: "
        f"{AKTUELLER_TEMP_FAKTOR:.2f} "
        f"-> {neuer_faktor:.2f}"
    )

    berechne_temperatur_und_dgl_terme(
        neuer_faktor
    )

    # Temperaturmodell-Kurve aktualisieren
    linie_temp_modell.set_ydata(
        temp_modell_jahr
    )

    # Danach Masse und Bilanz mit den neuen
    # Temperaturwerten aktualisieren
    aktualisieren()


fig.canvas.mpl_connect(
    "button_release_event",
    temperaturfaktor_losgelassen
)


# ============================================================
# RESET
# ============================================================

def reset(
    _
):

    slider_c.set_val(
        C_STANDARD
    )

    slider_d.set_val(
        D_STANDARD
    )

    slider_f.set_val(
        F_STANDARD
    )

    slider_temp_faktor.set_val(
        TEMP_FAKTOR_STANDARD
    )

    # Temperaturfaktor explizit anwenden,
    # da sein Slider absichtlich keinen on_changed-Callback hat.
    if not np.isclose(
        AKTUELLER_TEMP_FAKTOR,
        TEMP_FAKTOR_STANDARD
    ):

        berechne_temperatur_und_dgl_terme(
            TEMP_FAKTOR_STANDARD
        )

        linie_temp_modell.set_ydata(
            temp_modell_jahr
        )

    aktualisieren()


# ============================================================
# CSV SPEICHERN
# ============================================================

def speichern(
    _
):

    c = slider_c.val
    d = slider_d.val
    f = slider_f.val

    (
        masse,
        bilanz,
        delta_tag,
        masse_jahr,
        bilanz_jahr
    ) = simuliere(
        c,
        d,
        f
    )

    phase = np.where(
        historisch_maske,
        "Vergangenheit",
        "Zukunft"
    )

    df_tag = pd.DataFrame({
        "Datum": tage,
        "Phase": phase,
        "t": t_werte,
        "Masse_t": masse,
        "Masse_Mrd_t": masse / 1e9,
        "Massenbilanz_t_pro_Jahr": bilanz,
        "Massenänderung_t_pro_Tag": delta_tag,
        "TemperaturModell_Station_C": T_station,
        "TemperaturModell_2900m_C": T_2900_modell,
        "Niederschlag_DGL_mm_pro_Tag":
            PP_DGL_tag_m * 1000.0,
        "Niederschlag_Modell_mm_pro_Tag":
            PP_modell_tag_m * 1000.0,
        "Temperaturfaktor":
            AKTUELLER_TEMP_FAKTOR
    })

    df_jahr = pd.DataFrame({
        "Jahr": jahre_eindeutig,
        "Phase": np.where(
            hist_jahr_maske,
            "Vergangenheit",
            "Zukunft"
        ),
        "Masse_Mrd_t": masse_jahr,
        "Massenbilanz_Mrd_t_pro_Jahr": bilanz_jahr,
        "TemperaturModell_2900m_C":
            temp_modell_jahr,
        "NiederschlagModell_mm_pro_Jahr":
            pp_modell_jahr,
        "NiederschlagMessung_mm_pro_Jahr":
            pp_mess_jahr,
        "Temperaturfaktor":
            AKTUELLER_TEMP_FAKTOR,
        "Hoehenschritt_m":
            HOEHEN_SCHRITT_M
    })

    ausgabe_ordner = (
        aktuelle_datei.parent
    )

    df_tag.to_csv(
        ausgabe_ordner
        / "gletschermodell_1955_2100_taeglich.csv",
        index=False
    )

    df_jahr.to_csv(
        ausgabe_ordner
        / "gletschermodell_1955_2100_jaehrlich.csv",
        index=False
    )

    print(
        "Aktuelle Simulation gespeichert."
    )


# ============================================================
# EVENTS
# ============================================================

slider_c.on_changed(
    aktualisieren
)

slider_d.on_changed(
    aktualisieren
)

slider_f.on_changed(
    aktualisieren
)

button_reset.on_clicked(
    reset
)

button_save.on_clicked(
    speichern
)


# ============================================================
# START
# ============================================================

aktualisieren()

print()
print("Gletschermodell 1955–2100 bereit.")
print(
    f"Höhenschritt: "
    f"{HOEHEN_SCHRITT_M:g} m "
    f"-> {len(HOEHEN)} Höhenstufen"
)
print(
    "Temperaturmodell und Niederschlagsmodell "
    "werden über den gesamten Zeitraum gestrichelt dargestellt."
)
print(
    "Der Temperaturfaktor wird beim Loslassen "
    "des Sliders neu berechnet."
)

plt.show()
