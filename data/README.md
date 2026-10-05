# Herkunft der Daten

## data_year.csv

Hierbei handelt es sich um alle Daten, die jahresweise erhoben worden sind.

Für die Herkunft der Daten, s. folgende Tabelle. Wo `tt` angegeben ist, handelt es sich um die in der Aufgabenstellung gegebenen [Quelle 1](https://de.tutiempo.net/klima/ws-67200.html#google_vignette). Steht dort `gl`, handelt es sich um (Gletscher-)Daten von [hier](https://www.glamos.ch/factsheet#/B43-03), verlinkt aus [Quelle 2](https://naturwissenschaften.ch/snow-glaciers-permafrost-explained/glaciers/mass_balance/rhone).

Bei der Herleitung einiger der letzten Werte wurden folgende Annahmen getroffen:

- Dichte des Eises (/Alles von Eis über Firn bis Neuschnee) liegt gemittelt bei `ρ_Eis = 918 kg*m−3`
- Die Breite des Gletschers wird als konstant vereinfacht mit `B = 2 km`
- Der Gletscher wird für die Massenberechnung stark vereinfacht als Quader mit Grundfläche A (was eigentlich die Oberfläche ist) und Tiefe H

Die Formeln lauten:

- für die Integration der Länge: `L(t-1) + L(t)/dt`
- für die Berechnnung der Masse um 1999 (Fixpunkt) in Mrd. t: `M = ρ_Eis * (2.23km^3 * 10^9) / 10^12`
- für die Umrechnung der Massenbilanz pro Fläche auf Masse (diesmal jedoch Dichte von Wasser, da ja Änderung in mm H20 angegeben): `M(t) = M(t-1) + MpA/dt(t)*A(t)` (Einheiten beachten!!)

Die Formeln können im Spreadsheet, welches im Repository enthalten ist, nachgelesen werden. Die `.csv`-Datei ist schlicht die Ausgabe dieses Spreadsheets.


 **Dimension**    | **T**          | **TM**           | **Tm**           | **PP**                 | **V**                                     | **RA**        | **SN**         | **TS**        | **FG**        | **TN**          | **GR**        | **MpA/dt**                    | **L/dt**           | **L**                                                                                       | **A**                              | **M**                                                                                                                                                         
--------------|------------|--------------|--------------|--------------------|---------------------------------------|-----------|------------|-----------|-----------|-------------|-----------|---------------------------|----------------|---------------------------------------------------------------------------------------------|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------
 **Einheit**      | °C         | °C           | °C           | mm                 | km/h                                  | -         | -          | -         | -         | -           | -         | mm w.e.                   | m              | m                                                                                           | km²                                     | Mrd. t                                                                                                                                                   
 **Beschreibung** | Temperatur | Maximaltemp. | Minimaltemp. | Jahresniederschlag | Durchschnittliche Windgeschwindigkeit | Regentage | Schneetage | Sturmtage | Nebeltage | Tornadotage | Hageltage | Massenänderung pro Fläche | Längenänderung | Länge                                                                                       | Fläche                                  | Durchschnittliche Masse                                                                                                                                   
 **Herkunft**     | tt         | tt           | tt           | tt                 | tt                                    | tt        | tt         | tt        | tt        | tt          | tt        | gl                        | gl             | Hergeleitet aus `L/dt` und gegebener `Länge um 1999` in der Aufgabenstellung (dort ohne Quelle) | Berechnet aus `L` und fest angenommener `B` | Hergeleitet aus `MpA/dt` und der `MpA` um 1999 (diese ist berechnet aus dem in der Aufgabenstellung gegebenem `V`, der durchschnittlichen `Dichte vom Eis` und `A`) 




