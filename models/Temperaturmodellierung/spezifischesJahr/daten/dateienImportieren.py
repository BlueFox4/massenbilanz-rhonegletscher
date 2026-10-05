import requests
import pandas as pd
from bs4 import BeautifulSoup
import time


# ============================================================
# EINSTELLUNGEN
# ============================================================

STATION = "67200"

START_JAHR = 1955
END_JAHR = 2025

URL_VORLAGE = (
    "https://de.tutiempo.net/klima/"
    "{monat:02d}-{jahr}/ws-{station}.html"
)


# ============================================================
# HTTP-EINSTELLUNGEN
# ============================================================

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0 Safari/537.36"
    )
}


# ============================================================
# SESSION
# ============================================================

session = requests.Session()
session.headers.update(headers)


# ============================================================
# JAHRE DURCHLAUFEN
# ============================================================

for jahr in range(START_JAHR, END_JAHR + 1):

    print()
    print("=" * 70)
    print(f"STARTE JAHR {jahr}")
    print("=" * 70)

    # Daten für dieses Jahr
    alle_daten = []


    # ========================================================
    # MONATE DURCHLAUFEN
    # ========================================================

    for monat in range(1, 13):

        url = URL_VORLAGE.format(
            monat=monat,
            jahr=jahr,
            station=STATION
        )

        print(
            f"Lese {jahr}-{monat:02d}: {url}"
        )

        try:

            response = session.get(
                url,
                timeout=20
            )

            response.raise_for_status()


            # ------------------------------------------------
            # HTML analysieren
            # ------------------------------------------------

            soup = BeautifulSoup(
                response.text,
                "html.parser"
            )


            # ------------------------------------------------
            # Tabellen suchen
            # ------------------------------------------------

            tabellen = soup.find_all("table")

            klima_tabelle = None

            for tabelle in tabellen:

                erste_zeile = tabelle.find("tr")

                if erste_zeile is None:
                    continue

                kopf = [
                    zelle.get_text(
                        " ",
                        strip=True
                    )
                    for zelle in erste_zeile.find_all(
                        ["th", "td"]
                    )
                ]

                # Klimatabelle erkennen
                if "Tag" in kopf:
                    klima_tabelle = tabelle
                    break


            if klima_tabelle is None:

                print(
                    "    ⚠ Keine Klimatabelle gefunden."
                )

                continue


            # ------------------------------------------------
            # Tabellenzeilen
            # ------------------------------------------------

            zeilen = klima_tabelle.find_all("tr")

            if not zeilen:

                print(
                    "    ⚠ Tabelle ist leer."
                )

                continue


            # ------------------------------------------------
            # Kopfzeile
            # ------------------------------------------------

            kopfzeile = [
                zelle.get_text(
                    " ",
                    strip=True
                )
                for zelle in zeilen[0].find_all(
                    ["th", "td"]
                )
            ]


            # ------------------------------------------------
            # Tagesdaten
            # ------------------------------------------------

            monatsdaten = []

            for zeile in zeilen[1:]:

                zellen = [
                    zelle.get_text(
                        " ",
                        strip=True
                    )
                    for zelle in zeile.find_all(
                        ["th", "td"]
                    )
                ]

                if not zellen:
                    continue


                # Nur Zeilen mit einem numerischen Tag
                try:
                    tag = int(zellen[0])
                except ValueError:
                    continue


                # Fehlende Zellen auffüllen
                while len(zellen) < len(kopfzeile):
                    zellen.append("")


                # Zu viele Zellen entfernen
                zellen = zellen[:len(kopfzeile)]

                monatsdaten.append(zellen)


            # ------------------------------------------------
            # Prüfen
            # ------------------------------------------------

            if not monatsdaten:

                print(
                    "    ⚠ Keine Tagesdaten gefunden."
                )

                continue


            # ------------------------------------------------
            # DataFrame erstellen
            # ------------------------------------------------

            df = pd.DataFrame(
                monatsdaten,
                columns=kopfzeile
            )


            # Jahr und Monat hinzufügen
            df.insert(0, "Jahr", jahr)
            df.insert(1, "Monat", monat)


            # ------------------------------------------------
            # Datum erstellen
            # ------------------------------------------------

            df["Datum"] = pd.to_datetime(
                {
                    "year": df["Jahr"],
                    "month": df["Monat"],
                    "day": pd.to_numeric(
                        df["Tag"],
                        errors="coerce"
                    )
                },
                errors="coerce"
            )


            # Datum an erste Stelle
            spalten = ["Datum"] + [
                spalte
                for spalte in df.columns
                if spalte != "Datum"
            ]

            df = df[spalten]


            # ------------------------------------------------
            # Daten des Monats speichern
            # ------------------------------------------------

            alle_daten.append(df)

            print(
                f"    ✓ {len(df)} Tage gefunden"
            )


        except requests.RequestException as e:

            print(
                f"    ✗ Fehler beim Abrufen: {e}"
            )


        except Exception as e:

            print(
                f"    ✗ Fehler beim Auslesen: {e}"
            )


        # Kleine Pause zwischen den Anfragen
        time.sleep(1)


    # ========================================================
    # JAHR ZUSAMMENFÜHREN
    # ========================================================

    if not alle_daten:

        print()
        print(
            f"⚠ Für {jahr} wurden keine Daten gefunden."
        )

        continue


    daten = pd.concat(
        alle_daten,
        ignore_index=True
    )


    # ========================================================
    # NACH DATUM SORTIEREN
    # ========================================================

    daten = daten.sort_values(
        "Datum"
    ).reset_index(drop=True)


    # ========================================================
    # DATEINAME
    # ========================================================

    dateiname = (
        f"klimadaten_{STATION}_{jahr}.csv"
    )


    # ========================================================
    # CSV SPEICHERN
    # ========================================================

    daten.to_csv(
        dateiname,
        index=False,
        sep=";",
        encoding="utf-8-sig"
    )


    # ========================================================
    # ERGEBNIS
    # ========================================================

    print()
    print(
        f"✓ JAHR {jahr} FERTIG"
    )

    print(
        f"  Datei: {dateiname}"
    )

    print(
        f"  Datensätze: {len(daten)}"
    )

    print()


# ============================================================
# ALLES FERTIG
# ============================================================

print()
print("=" * 70)
print("ALLE JAHRE FERTIG!")
print("=" * 70)

print(
    f"Zeitraum: {START_JAHR}–{END_JAHR}"
)

print(
    f"Dateien: {END_JAHR - START_JAHR + 1}"
)