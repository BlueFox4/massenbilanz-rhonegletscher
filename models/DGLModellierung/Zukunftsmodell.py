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
# KALIBRIERTE STANDARDWERTE
# ============================================================

C_STANDARD = 1.4125375446227554e-06
D_STANDARD = 0.005623413251903491
F_STANDARD = 4.4668359215096345


T0 = 2.0


# ============================================================
# TEMPERATURFAKTOR
# ============================================================

TEMP_FAKTOR_STANDARD = 1.0
TEMP_FAKTOR_MIN = 0.0
TEMP_FAKTOR_MAX = 3.0


# ============================================================
# ZEITRAUM
# ============================================================

START_JAHR = 1955
LETZTES_HISTORISCHES_JAHR = 2023
ERSTES_ZUKUNFTSJAHR = 2024
END_JAHR = 2100

M_START = 2160111516.0  # Tonnen

# Eure t-Achse ist in Jahren.
DT = 1.0 / 366.0

TEMPERATUR_SINCE = 1994
TEMPERATUR_UNTIL = 2024
NIEDERSCHLAG_SINCE = 1994


# ============================================================
# HÖHENMODELL
# ============================================================

STATIONS_HOEHE = 482.0

GLETSCHER_MIN = 2200.0
GLETSCHER_MAX = 3600.0

HOEHEN_SCHRITT_M = 100.0

LAPSE_RATE = 0.0065

K_AKK = 1000.0 * 2000.0


def erstelle_hoehen():

    if HOEHEN_SCHRITT_M <= 0:
        raise ValueError(
            "HOEHEN_SCHRITT_M muss > 0 sein."
        )

    hoehen = np.arange(
        GLETSCHER_MIN,
        GLETSCHER_MAX + 1e-9,
        HOEHEN_SCHRITT_M,
        dtype=float
    )

    if hoehen[-1] < GLETSCHER_MAX:
        hoehen = np.append(
            hoehen,
            GLETSCHER_MAX
        )

    return hoehen


HOEHEN = erstelle_hoehen()


# ============================================================
# GEMESSENE GLETSCHERMASSEN
# Mrd. Tonnen
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
# CSV EINLESEN
# ============================================================

def lade_rohdaten():

    if not CSV_DATEI.exists():
        raise FileNotFoundError(
            f"{CSV_DATEI} wurde nicht gefunden."
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
            f"Fehlende CSV-Spalten: {fehlt}"
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
# HISTORISCHE DGL-DATEN
#
# GANZ WICHTIG:
# Hier werden NUR die tatsächlich vorhandenen CSV-Tage benutzt.
# Komplett fehlende Jahre werden NICHT künstlich ergänzt.
#
# Genau so bleibt die Rechnung mit den kalibrierten Parametern
# vergleichbar.
# ============================================================

hist_df = rohdaten[
    (rohdaten["Datum"] >= pd.Timestamp(f"{START_JAHR}-01-01"))
    & (rohdaten["Datum"] <= pd.Timestamp(f"{LETZTES_HISTORISCHES_JAHR}-12-31"))
][
    ["Datum", "T", "PP"]
].copy()

hist_df = (
    hist_df.sort_values("Datum")
           .reset_index(drop=True)
)


# ============================================================
# EINZELNE FEHLENDE PP-WERTE AUF VORHANDENEN TAGEN ERGÄNZEN
# ============================================================

hist_df["MonatTag"] = (
    hist_df["Datum"].dt.strftime("%m-%d")
)

gueltig_pp = hist_df.dropna(
    subset=["PP"]
).copy()

pp_tag_mittel = (
    gueltig_pp.groupby(
        "MonatTag"
    )["PP"].mean()
)

pp_monat_mittel = (
    gueltig_pp.groupby(
        gueltig_pp["Datum"].dt.month
    )["PP"].mean()
)

pp_global = float(
    gueltig_pp["PP"].mean()
)

hist_df["Monat"] = (
    hist_df["Datum"].dt.month
)

fehlende_pp = int(
    hist_df["PP"].isna().sum()
)

hist_df["PP"] = hist_df["PP"].fillna(
    hist_df["MonatTag"].map(
        pp_tag_mittel
    )
)

hist_df["PP"] = hist_df["PP"].fillna(
    hist_df["Monat"].map(
        pp_monat_mittel
    )
)

hist_df["PP"] = hist_df["PP"].fillna(
    pp_global
)

hist_df["PP"] = hist_df["PP"].clip(
    lower=0
)

print(
    f"Historische DGL: {len(hist_df)} vorhandene Tage, "
    f"{fehlende_pp} einzelne PP-Lücken ergänzt."
)


# ============================================================
# ZUKUNFTSACHSE
# ============================================================

future_dates = pd.date_range(
    f"{ERSTES_ZUKUNFTSJAHR}-01-01",
    f"{END_JAHR}-12-31",
    freq="D"
)


# ============================================================
# DGL-ZEITACHSE:
#
# Vergangenheit = nur vorhandene CSV-Tage
# Zukunft      = jeder Kalendertag
# ============================================================

dgl_dates = pd.DatetimeIndex(
    list(hist_df["Datum"])
    + list(future_dates)
)

n_hist = len(hist_df)
n_future = len(future_dates)
n_dgl = len(dgl_dates)

dgl_jahre = dgl_dates.year.to_numpy()
dgl_tag_im_jahr = dgl_dates.dayofyear.to_numpy() - 1

dgl_t = (
    dgl_jahre
    + dgl_tag_im_jahr / 366.0
)

dgl_hist_maske = np.arange(
    n_dgl
) < n_hist

dgl_future_maske = ~dgl_hist_maske


# ============================================================
# NIEDERSCHLAGSMODELL 1955–2100 FÜR DEN VERGLEICHSGRAPHEN
# UND FÜR DIE ZUKUNFT DER DGL
# ============================================================

alle_tage = pd.date_range(
    f"{START_JAHR}-01-01",
    f"{END_JAHR}-12-31",
    freq="D"
)

alle_jahre = alle_tage.year.to_numpy()

print(
    "Berechne Niederschlagsmodell 1955–2100 ..."
)

start_zeit = time.time()

pp_modell_alle_tag_m = np.empty(
    len(alle_tage),
    dtype=float
)

jahr_monate = pd.DataFrame({
    "Jahr": alle_tage.year,
    "Monat": alle_tage.month
}).drop_duplicates()


for _, row in jahr_monate.iterrows():

    jahr = int(
        row["Jahr"]
    )

    monat = int(
        row["Monat"]
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
        (alle_tage.year == jahr)
        & (alle_tage.month == monat)
    )

    pp_modell_alle_tag_m[
        maske
    ] = pp_tag_m


print(
    f"Niederschlagsmodell fertig: "
    f"{time.time() - start_zeit:.2f} s"
)


# ============================================================
# DGL-NIEDERSCHLAG
#
# Historie: echte CSV-Werte
# Zukunft: Modell
# ============================================================

PP_DGL_m = np.empty(
    n_dgl,
    dtype=float
)

PP_DGL_m[
    :n_hist
] = (
    hist_df["PP"]
    .to_numpy(dtype=float)
    / 1000.0
)

# Zukunft aus dem vollständigen Modellarray herausziehen
future_mask_alle = (
    alle_tage.year >= ERSTES_ZUKUNFTSJAHR
)

PP_DGL_m[
    n_hist:
] = pp_modell_alle_tag_m[
    future_mask_alle
]


# ============================================================
# JAHRESWERTE NIEDERSCHLAG
# ============================================================

jahre_plot = np.arange(
    START_JAHR,
    END_JAHR + 1
)

plot_datum_jahr = pd.to_datetime(
    [
        f"{jahr}-07-01"
        for jahr in jahre_plot
    ]
)

# Modell
pp_modell_jahr = []

for jahr in jahre_plot:

    maske = (
        alle_tage.year == jahr
    )

    pp_modell_jahr.append(
        np.sum(
            pp_modell_alle_tag_m[
                maske
            ]
            * 1000.0
        )
    )

pp_modell_jahr = np.array(
    pp_modell_jahr
)


# Messung
pp_mess_jahr = np.full(
    len(jahre_plot),
    np.nan
)

for i, jahr in enumerate(
    jahre_plot
):

    if jahr > LETZTES_HISTORISCHES_JAHR:
        continue

    gruppe = hist_df[
        hist_df["Datum"].dt.year
        == jahr
    ]

    # komplette fehlende Jahre bleiben Lücken
    if len(gruppe) >= 300:

        pp_mess_jahr[i] = (
            gruppe["PP"].sum()
        )


# ============================================================
# GEMESSENE TEMPERATUR AUF 2900 m
# ============================================================

temp_mess_datum = []
temp_mess_jahr = []

for jahr in range(
    START_JAHR,
    ERSTES_ZUKUNFTSJAHR + 1
):

    gruppe = rohdaten[
        rohdaten["Datum"].dt.year
        == jahr
    ].dropna(
        subset=["T"]
    )

    if len(gruppe) >= 300:

        T_2900 = (
            gruppe["T"].to_numpy(dtype=float)
            - LAPSE_RATE
            * (2900.0 - STATIONS_HOEHE)
        )

        temp_mess_datum.append(
            pd.Timestamp(
                f"{jahr}-07-01"
            )
        )

        temp_mess_jahr.append(
            float(
                np.mean(T_2900)
            )
        )


temp_mess_datum = pd.DatetimeIndex(
    temp_mess_datum
)

temp_mess_jahr = np.array(
    temp_mess_jahr,
    dtype=float
)


# ============================================================
# TEMPERATURMODELL + DGL-TERME
#
# WICHTIG:
# Der Temperaturfaktor wird innerhalb der Temperaturfunktion
# verarbeitet, genauer im zeitabhängigen d-Parameter der
# Sinusfunktion.
#
# Deshalb darf NICHT mehr einfach
#
#     T_neu = T_basis * faktor
#
# gerechnet werden.
#
# Bei jeder Faktoränderung wird erhalteTemperatur(...) erneut
# mit since, until und factor aufgerufen.
#
# Die Trennung zwischen Vergangenheit und Zukunft liegt jetzt
# vollständig im Temperaturmodell selbst.
#
# Zur Beschleunigung wird die externe Funktion trotzdem nur
# EINMAL pro Tag auf Stationshöhe aufgerufen. Die Temperaturen
# der Höhenbänder werden danach mit NumPy aus dem bekannten
# Höhengradienten berechnet.
# ============================================================

T_station_dgl = None
T_baender_dgl = None
TEMP_MODELL_JAHR = None

A_TERM = None
D_TERM = None
F_TERM = None

AKTUELLER_TEMP_FAKTOR = None


def berechne_temperatur_und_terme(faktor):
    """
    Berechnet bei jeder Änderung des Temperaturfaktors
    die Temperaturfunktion vollständig neu.

    Das Temperaturmodell bekommt direkt:
        since = TEMPERATUR_SINCE
        until = TEMPERATUR_UNTIL
        factor = aktueller Sliderwert

    Die Trennung zwischen Vergangenheit und Zukunft wird
    ausschließlich von erhalteTemperatur(...) behandelt.

    Anschließend werden die temperaturabhängigen DGL-Terme
    A_TERM, D_TERM und F_TERM neu berechnet.
    """

    global T_station_dgl
    global T_baender_dgl
    global TEMP_MODELL_JAHR

    global A_TERM
    global D_TERM
    global F_TERM

    global AKTUELLER_TEMP_FAKTOR

    faktor = float(faktor)

    print(
        f"Berechne Temperaturmodell mit Faktor "
        f"{faktor:.2f} ..."
    )

    start_zeit = time.time()

    # --------------------------------------------------------
    # 1. Temperatur auf Stationshöhe für alle DGL-Tage
    #
    # Der Faktor wird IN der Temperaturfunktion verarbeitet.
    # --------------------------------------------------------

    station_dgl = np.empty(
        n_dgl,
        dtype=float
    )

    for i, t in enumerate(dgl_t):

        # Vergangenheit/Zukunft wird vollständig im Temperaturmodell behandelt.
        station_dgl[i] = TR.erhalteTemperatur(
            float(t),
            STATIONS_HOEHE,
            TEMPERATUR_SINCE,
            TEMPERATUR_UNTIL,
            faktor
        )

    # --------------------------------------------------------
    # 2. Temperaturen der Höhenbänder
    #
    # Nur die Stations-Temperatur muss teuer neu berechnet
    # werden. Der lineare Höhengradient bleibt unabhängig
    # vom Faktor und kann schnell per NumPy angewendet werden.
    # --------------------------------------------------------

    hoehenkorrektur = (
        LAPSE_RATE
        * (
            HOEHEN
            - STATIONS_HOEHE
        )
    )

    baender_dgl = (
        station_dgl[:, None]
        - hoehenkorrektur[None, :]
    )

    # --------------------------------------------------------
    # 3. Temperaturabhängige DGL-Terme
    # --------------------------------------------------------

    schnee_anteil = np.mean(
        baender_dgl <= T0,
        axis=1
    )

    positive_temp = np.maximum(
        baender_dgl - T0,
        0.0
    )

    schmelztemperatur = np.mean(
        positive_temp,
        axis=1
    )

    neues_A = (
        K_AKK
        * PP_DGL_m
        * schnee_anteil
    )

    neues_D = (
        schmelztemperatur
    )

    neues_F = (
        schmelztemperatur
        * PP_DGL_m
    )

    # --------------------------------------------------------
    # 4. Jahreskurve des Temperaturmodells auf 2900 m
    #
    # Für die Darstellung genügen 12 repräsentative
    # Monatswerte pro Jahr.
    # --------------------------------------------------------

    temp_jahreswerte = []

    for jahr in jahre_plot:

        monatswerte = []

        for monat in range(
            1,
            13
        ):

            tage_monat = calendar.monthrange(
                int(jahr),
                monat
            )[1]

            datum = pd.Timestamp(
                int(jahr),
                monat,
                min(15, tage_monat)
            )

            t = (
                jahr
                + (
                    datum.dayofyear - 1
                ) / 366.0
            )

            T_2900 = TR.erhalteTemperatur(
                float(t),
                2900.0,
                TEMPERATUR_SINCE,
                TEMPERATUR_UNTIL,
                faktor
            )

            monatswerte.append(
                T_2900
            )

        temp_jahreswerte.append(
            np.mean(
                monatswerte
            )
        )

    # --------------------------------------------------------
    # Erst nach erfolgreicher Berechnung globale Werte ersetzen
    # --------------------------------------------------------

    T_station_dgl = station_dgl
    T_baender_dgl = baender_dgl

    A_TERM = neues_A
    D_TERM = neues_D
    F_TERM = neues_F

    TEMP_MODELL_JAHR = np.array(
        temp_jahreswerte,
        dtype=float
    )

    AKTUELLER_TEMP_FAKTOR = faktor

    print(
        f"Temperaturmodell fertig: "
        f"{time.time() - start_zeit:.2f} s"
    )


# Beim Programmstart einmal mit dem Standardfaktor berechnen
berechne_temperatur_und_terme(
    TEMP_FAKTOR_STANDARD
)


# ============================================================
# MASSENSIMULATION
#
# Ein Euler-Schritt PRO VORHANDENER HISTORISCHER CSV-ZEILE.
#
# Genau dadurch werden komplett fehlende Jahre nicht
# künstlich in die historische Kalibrierung hineingerechnet.
# ============================================================

def simuliere(
    c,
    d,
    f
):

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

    return (
        masse,
        bilanz,
        delta_tag
    )


# ============================================================
# MASSENWERTE PRO JAHR FÜR RMSE / AUSGABE
# ============================================================

def jahresendmassen(
    masse
):

    werte = {}

    # Historie: letzter wirklich vorhandener Datensatz des Jahres
    hist_masse = masse[
        :n_hist
    ]

    hist_dates = hist_df[
        "Datum"
    ].to_numpy()

    hist_years = hist_df[
        "Datum"
    ].dt.year.to_numpy()

    for jahr in np.unique(
        hist_years
    ):

        idx = np.where(
            hist_years == jahr
        )[0]

        werte[int(jahr)] = (
            hist_masse[
                idx[-1]
            ]
            / 1e9
        )

    # Zukunft: letzter Kalendertag des Jahres
    future_masse = masse[
        n_hist:
    ]

    future_years = future_dates.year.to_numpy()

    for jahr in np.unique(
        future_years
    ):

        idx = np.where(
            future_years == jahr
        )[0]

        werte[int(jahr)] = (
            future_masse[
                idx[-1]
            ]
            / 1e9
        )

    return werte


# ============================================================
# RMSE
# ============================================================

mess_jahre = np.array(
    sorted(
        GEMESSENE_MASSE_MRD_T.keys()
    ),
    dtype=int
)

mess_masse = np.array(
    [
        GEMESSENE_MASSE_MRD_T[
            jahr
        ]
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


def berechne_rmse(
    masse
):

    # Statt Jahresende nehmen wir wie beim alten Modell
    # den Modellwert, dessen Datum dem Messjahr am nächsten liegt.
    fehler = []

    hist_dates_np = hist_df[
        "Datum"
    ].to_numpy(
        dtype="datetime64[ns]"
    )

    hist_masse = masse[
        :n_hist
    ] / 1e9

    for jahr, gemessen in zip(
        mess_jahre,
        mess_masse
    ):

        ziel = np.datetime64(
            f"{jahr}-07-01"
        )

        if jahr <= LETZTES_HISTORISCHES_JAHR:

            differenz = np.abs(
                hist_dates_np
                - ziel
            )

            idx = int(
                np.argmin(
                    differenz
                )
            )

            modell = (
                hist_masse[idx]
            )

        else:
            continue

        fehler.append(
            modell
            - gemessen
        )

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
# ERSTE SIMULATION
# ============================================================

masse, bilanz, delta_tag = simuliere(
    C_STANDARD,
    D_STANDARD,
    F_STANDARD
)


# ============================================================
# PLOT-DATEN DER MASSE
#
# Wieder feiner statt nur 1 Punkt/Jahr.
# Jeder 7. Berechnungsschritt reicht für eine glatte Darstellung.
# ============================================================

PLOT_SCHRITT = 7

hist_plot_dates = pd.DatetimeIndex(
    hist_df["Datum"]
)[::PLOT_SCHRITT]

hist_plot_idx = np.arange(
    0,
    n_hist,
    PLOT_SCHRITT
)

future_plot_dates = future_dates[
    ::PLOT_SCHRITT
]

future_plot_idx = (
    n_hist
    + np.arange(
        0,
        n_future,
        PLOT_SCHRITT
    )
)


# ============================================================
# JÄHRLICHE MASSENBILANZ
# ============================================================

def bilanz_jahr_werte(
    delta_tag
):

    jahre = []
    werte = []

    # Historisch nur vorhandene Daten
    hist_delta = delta_tag[
        :n_hist
    ]

    hist_years = hist_df[
        "Datum"
    ].dt.year.to_numpy()

    for jahr in np.unique(
        hist_years
    ):

        maske = (
            hist_years == jahr
        )

        jahre.append(
            int(jahr)
        )

        werte.append(
            np.sum(
                hist_delta[
                    maske
                ]
            )
            / 1e9
        )

    # Zukunft
    future_delta = delta_tag[
        n_hist:
    ]

    future_years = future_dates.year.to_numpy()

    for jahr in np.unique(
        future_years
    ):

        maske = (
            future_years == jahr
        )

        jahre.append(
            int(jahr)
        )

        werte.append(
            np.sum(
                future_delta[
                    maske
                ]
            )
            / 1e9
        )

    return (
        np.array(
            jahre
        ),
        np.array(
            werte
        )
    )


bilanz_jahre, bilanz_jahr = (
    bilanz_jahr_werte(
        delta_tag
    )
)

bilanz_plot_dates = pd.to_datetime(
    [
        f"{jahr}-07-01"
        for jahr in bilanz_jahre
    ]
)

bilanz_hist_maske = (
    bilanz_jahre
    <= LETZTES_HISTORISCHES_JAHR
)

# 2023 mit in Zukunftslinie aufnehmen
idx_bilanz_2023 = np.where(
    bilanz_jahre
    == LETZTES_HISTORISCHES_JAHR
)[0]

if len(
    idx_bilanz_2023
) > 0:

    bilanz_zukunft_idx = np.arange(
        idx_bilanz_2023[0],
        len(
            bilanz_jahre
        )
    )

else:
    bilanz_zukunft_idx = np.where(
        bilanz_jahre
        >= ERSTES_ZUKUNFTSJAHR
    )[0]


# ============================================================
# DIAGRAMM
# ============================================================

fig, ax_masse = plt.subplots(
    figsize=(20, 11)
)

fig.canvas.manager.set_window_title(
    "Gletschermodell Rhonegletscher"
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
FARBE_TEMP = "tab:orange"
FARBE_PP = "tab:green"


# ============================================================
# MASSE: FEIN AUFGELÖST
# ============================================================

linie_masse_hist, = ax_masse.plot(
    hist_plot_dates,
    masse[
        hist_plot_idx
    ] / 1e9,
    color=FARBE_MASSE,
    linewidth=2.5,
    linestyle="-",
    label="Gletschermasse"
)

linie_masse_zukunft, = ax_masse.plot(
    future_plot_dates,
    masse[
        future_plot_idx
    ] / 1e9,
    color=FARBE_MASSE,
    linewidth=2.5,
    linestyle="--"
)


# ============================================================
# BILANZ
# ============================================================

linie_bilanz_hist, = ax_bilanz.plot(
    bilanz_plot_dates[
        bilanz_hist_maske
    ],
    bilanz_jahr[
        bilanz_hist_maske
    ],
    color=FARBE_BILANZ,
    linewidth=2.0,
    linestyle="-",
    label="Massenbilanz"
)

linie_bilanz_zukunft, = ax_bilanz.plot(
    bilanz_plot_dates[
        bilanz_zukunft_idx
    ],
    bilanz_jahr[
        bilanz_zukunft_idx
    ],
    color=FARBE_BILANZ,
    linewidth=2.0,
    linestyle="--"
)


# ============================================================
# TEMPERATUR
# Messung = durchgezogen
# Modell  = überall gestrichelt
# gleiche Farbe
# ============================================================

linie_temp_mess, = ax_temp.plot(
    temp_mess_datum,
    temp_mess_jahr,
    color=FARBE_TEMP,
    linewidth=2.0,
    linestyle="-",
    label="Temperatur Messung"
)

linie_temp_modell, = ax_temp.plot(
    plot_datum_jahr,
    TEMP_MODELL_JAHR,
    color=FARBE_TEMP,
    linewidth=2.0,
    linestyle="--",
    label="Temperatur Modell"
)


# ============================================================
# NIEDERSCHLAG
# Messung = durchgezogen
# Modell  = überall gestrichelt
# gleiche Farbe
# ============================================================

linie_pp_mess, = ax_pp.plot(
    plot_datum_jahr,
    pp_mess_jahr,
    color=FARBE_PP,
    linewidth=1.8,
    linestyle="-",
    label="Niederschlag Messung"
)

linie_pp_modell, = ax_pp.plot(
    plot_datum_jahr,
    pp_modell_jahr,
    color=FARBE_PP,
    linewidth=1.8,
    linestyle="--",
    label="Niederschlag Modell"
)


# ============================================================
# GEMESSENE MASSE
# ============================================================

messpunkte = ax_masse.scatter(
    mess_datum,
    mess_masse,
    s=45,
    color="black",
    zorder=2,
    label="Gemessene Masse"
)


# ============================================================
# ZUKUNFTSGRENZE
# ============================================================

grenze = pd.Timestamp(
    "2024-01-01"
)

ax_masse.axvline(
    grenze,
    color="black",
    linestyle=":",
    linewidth=1.7,
    alpha=0.8
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
    r"Gletschermodell 1955–2100"
    "\n"
    r"$M'(t)=M(t)\,\left[PP(t)\,c-\left(T(t)-T_0\right)\left(d+PP(t)\,f\right)\right]$",
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
    linestyle=":",
    linewidth=1,
    alpha=0.5
)


# ============================================================
# LEGENDE
# ============================================================

legende = ax_masse.legend(
    [
        linie_masse_hist,
        linie_bilanz_hist,
        linie_temp_modell,
        linie_temp_mess,
        linie_pp_modell,
        linie_pp_mess,
        messpunkte
    ],
    [
        "Gletschermasse",
        "Massenbilanz",
        "Modelltemperatur 2900 m",
        "Gemessene Temperatur 2900 m",
        "Niederschlagsmodell",
        "Gemessener Niederschlag",
        "Gemessene Masse"
    ],
    loc="upper left",
    fontsize=9
)

legende.set_zorder(100)


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
    0.10,   # links
    0.035,  # weiter nach unten
    0.54,   # Breite
    0.023   # Höhe
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
    0.75,
    0.025,
    0.12,
    0.05
])

button_reset = Button(
    ax_reset,
    "Berechnete Modellwerte"
)

ax_save = plt.axes([
    0.89,
    0.025,
    0.11,
    0.05
])

button_save = Button(
    ax_save,
    "CSV speichern"
)


# ============================================================
# GRAPHEN-AUSWAHL
# ============================================================

ax_graphen = plt.axes([
    0.75,
    0.07,
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
# UPDATE
# ============================================================

def aktualisieren(
    _=None
):

    global masse
    global bilanz
    global delta_tag

    global bilanz_jahre
    global bilanz_jahr
    global bilanz_plot_dates
    global bilanz_hist_maske
    global bilanz_zukunft_idx

    masse, bilanz, delta_tag = simuliere(
        slider_c.val,
        slider_d.val,
        slider_f.val
    )

    # Masse fein aufgelöst
    linie_masse_hist.set_ydata(
        masse[
            hist_plot_idx
        ] / 1e9
    )

    linie_masse_zukunft.set_ydata(
        masse[
            future_plot_idx
        ] / 1e9
    )

    # Bilanz neu aggregieren
    bilanz_jahre, bilanz_jahr = (
        bilanz_jahr_werte(
            delta_tag
        )
    )

    bilanz_plot_dates = pd.to_datetime(
        [
            f"{jahr}-07-01"
            for jahr in bilanz_jahre
        ]
    )

    bilanz_hist_maske = (
        bilanz_jahre
        <= LETZTES_HISTORISCHES_JAHR
    )

    idx_2023 = np.where(
        bilanz_jahre
        == LETZTES_HISTORISCHES_JAHR
    )[0]

    if len(idx_2023) > 0:

        bilanz_zukunft_idx = np.arange(
            idx_2023[0],
            len(
                bilanz_jahre
            )
        )

    else:

        bilanz_zukunft_idx = np.where(
            bilanz_jahre
            >= ERSTES_ZUKUNFTSJAHR
        )[0]


    linie_bilanz_hist.set_data(
        bilanz_plot_dates[
            bilanz_hist_maske
        ],
        bilanz_jahr[
            bilanz_hist_maske
        ]
    )

    linie_bilanz_zukunft.set_data(
        bilanz_plot_dates[
            bilanz_zukunft_idx
        ],
        bilanz_jahr[
            bilanz_zukunft_idx
        ]
    )


    # Achse Masse
    ymin = min(
        np.nanmin(
            masse / 1e9
        ),
        np.nanmin(
            mess_masse
        )
    )

    ymax = max(
        np.nanmax(
            masse / 1e9
        ),
        np.nanmax(
            mess_masse
        )
    )

    rand = max(
        0.03,
        0.08 * (
            ymax - ymin
        )
    )

    ax_masse.set_ylim(
        max(
            0,
            ymin - rand
        ),
        ymax + rand
    )


    # Achse Bilanz
    bmax = max(
        abs(
            np.nanmin(
                bilanz_jahr
            )
        ),
        abs(
            np.nanmax(
                bilanz_jahr
            )
        ),
        0.001
    )

    ax_bilanz.set_ylim(
        -1.15 * bmax,
        1.15 * bmax
    )


    # Kennwerte
    rmse = berechne_rmse(
        masse
    )

    # Ende 2023 = letzter vorhandener historischer DGL-Wert
    M_2023 = (
        masse[
            n_hist - 1
        ]
        / 1e9
    )

    M_2100 = (
        masse[-1]
        / 1e9
    )

    info_text.set_text(
        f"c = {slider_c.val:.3e}   "
        f"d = {slider_d.val:.6f}   "
        f"f = {slider_f.val:.4f}   "
        f"Temp.-Faktor = {AKTUELLER_TEMP_FAKTOR:.2f}\n"
        f"Höhenschritt = {HOEHEN_SCHRITT_M:g} m "
        f"({len(HOEHEN)} Stufen)   |   "
        f"M(1955) = {M_START / 1e9:.4f} Mrd. t   |   "
        f"M(2023) = {M_2023:.4f} Mrd. t   |   "
        f"M(2100) = {M_2100:.4f} Mrd. t   |   "
        f"RMSE = {rmse:.4f} Mrd. t"
    )

    fig.canvas.draw_idle()


# ============================================================
# TEMPERATURFAKTOR
#
# Erst beim Loslassen des Sliders wird die Temperaturfunktion
# mit dem neuen Faktor erneut berechnet. Ab wann der Faktor
# wirkt, regelt das Temperaturmodell über TEMPERATUR_UNTIL.
# ============================================================

def faktor_losgelassen(
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

    # Der Faktor wird direkt an das Temperaturmodell übergeben.
    # Ab wann er wirkt, regelt erhalteTemperatur(...) selbst.
    berechne_temperatur_und_terme(
        neuer_faktor
    )

    linie_temp_modell.set_ydata(
        TEMP_MODELL_JAHR
    )

    # Danach Masse und Massenbilanz mit den neuen
    # Temperaturwerten neu bestimmen.
    aktualisieren()


fig.canvas.mpl_connect(
    "button_release_event",
    faktor_losgelassen
)


# ============================================================
# CHECKBOXEN
# ============================================================

def aktualisiere_achsen():

    ax_masse.yaxis.set_visible(
        linie_masse_hist.get_visible()
        or messpunkte.get_visible()
    )

    bil_sichtbar = (
        linie_bilanz_hist.get_visible()
        or linie_bilanz_zukunft.get_visible()
    )

    ax_bilanz.yaxis.set_visible(
        bil_sichtbar
    )

    ax_bilanz.spines["right"].set_visible(
        bil_sichtbar
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


def graph_sichtbarkeit(
    label
):

    if label == "Gletschermasse":

        neu = not (
            linie_masse_hist.get_visible()
        )

        linie_masse_hist.set_visible(
            neu
        )

        linie_masse_zukunft.set_visible(
            neu
        )


    elif label == "Massenbilanz":

        neu = not (
            linie_bilanz_hist.get_visible()
        )

        linie_bilanz_hist.set_visible(
            neu
        )

        linie_bilanz_zukunft.set_visible(
            neu
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


    aktualisiere_achsen()

    fig.canvas.draw_idle()


check_graphen.on_clicked(
    graph_sichtbarkeit
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

    if not np.isclose(
        AKTUELLER_TEMP_FAKTOR,
        TEMP_FAKTOR_STANDARD
    ):

        berechne_temperatur_und_terme(
            TEMP_FAKTOR_STANDARD
        )

        linie_temp_modell.set_ydata(
            TEMP_MODELL_JAHR
        )

    aktualisieren()


# ============================================================
# CSV SPEICHERN
# ============================================================

def speichern(
    _
):

    ausgabe = pd.DataFrame({
        "Datum": dgl_dates,
        "t": dgl_t,
        "Phase": np.where(
            dgl_hist_maske,
            "Vergangenheit",
            "Zukunft"
        ),
        "Masse_t": masse,
        "Masse_Mrd_t": masse / 1e9,
        "Massenbilanz_t_pro_Jahr": bilanz,
        "Massenänderung_t_pro_Schritt": delta_tag,
        "Niederschlag_DGL_mm": PP_DGL_m * 1000.0
    })

    ausgabe.to_csv(
    aktuelle_datei.parent / "InfoZukunft" / "gletschermodell_1955_2100.csv",
    index=False
    )

    print(
        "CSV gespeichert."
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
print(
    "Modell bereit."
)

print(
    "Historische DGL nutzt nur tatsächlich vorhandene CSV-Tage."
)

print(
    f"Höhenschritt: {HOEHEN_SCHRITT_M:g} m "
    f"-> {len(HOEHEN)} Höhenstufen"
)

plt.show()
