for jahr in range(1955, 2026, 1):
    try:
        file =  open(f"models/Temperaturmodellierung/spezifischesJahr/daten/klimadaten_67200_{jahr}.csv",'r')
    except:
        print(f"Datei des Jahres {jahr} konnte nicht gefunden werden.")
        continue
    lines = file.readlines()
    if len(lines)-1 != 365 and len(lines)-1 != 366:
        print(f"Das Jahr {jahr} hat {len(lines)-1} Tage")
# -->
# Das Jahr 1964 hat 153 Tage --> Löschen
# Datei des Jahres 1970 konnte nicht gefunden werden.
# Datei des Jahres 1971 konnte nicht gefunden werden.
# Datei des Jahres 1972 konnte nicht gefunden werden.
# Das Jahr 2025 hat 243 Tage --> Löschen