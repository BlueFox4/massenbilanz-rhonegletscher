# Herkunft der Daten

Die Beschreibung der Daten gibt es auch in einer Datei mit entsprechendem Suffix `.description.csv`.

## Quellen

Für die Herkunft der Daten, s. folgende Untertitel. 

- [Quelle 1](https://de.tutiempo.net/klima/ws-67200.html#google_vignette): Wo `tt` angegeben ist, handelt es sich um die in der Aufgabenstellung gegebenen Quelle. 
- [Quelle 2](https://www.glamos.ch/factsheet#/B43-03): Wo `gl` angegeben ist, handelt es sich um (Gletscher-)Daten von dieser Seite (Q3 verlinkt hierauf).
- [Quelle 3](https://naturwissenschaften.ch/snow-glaciers-permafrost-explained/glaciers/mass_balance/rhone): Wo `na` angegeben ist, handelt es sich um Massen- und Längenbilanzen.

## data_year.csv

Hierbei handelt es sich um alle Daten, die jahresweise erhoben worden sind.

Bei der Herleitung einiger der letzten Werte wurden folgende Annahmen getroffen:

- Dichte des Eises (/Alles von Eis über Firn bis Neuschnee) liegt gemittelt bei $\rho_{Eis} = 918 \frac{kg}{m^{3}}$
- Die Breite des Gletschers wird als konstant vereinfacht mit $B = 1,5km$
- Der Gletscher wird für die Massenberechnung stark vereinfacht als Quader mit Grundfläche A (was eigentlich die obere Oberfläche ist) und Tiefe H

Die Formeln lauten:

- für die Integration der Länge: $\int{L(t)} = L(t-1) + \frac{L(t)}{dt}$
- für die Berechnnung der Masse um 1999 (Fixpunkt) in Mrd. t: $M = ρ_{Eis} \cdot (2.23km^{3} \cdot 10^{9}) / 10^{12}$
- für die Umrechnung der Massenbilanz pro Fläche auf Masse (diesmal jedoch Dichte von Wasser, da ja Änderung in $mm\ w.e.$ angegeben): $M(t) = M(t-1) + \frac{MpA}{dt}(t) \cdot A(t)$ (Einheiten beachten!)

Die Formeln können im Spreadsheet, welches im Repository enthalten ist, nachgelesen werden. Die `.csv`-Datei ist schlicht die Ausgabe dieses Spreadsheets.

| **Dimension** | **Einheit**                 | **Beschreibung**                      | **Herkunft**                                                                                                                                                                        |
|---------------|-----------------------------|---------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **T**         | $^{\circ}C$                        | Temperatur                            | tt (scraped)                                                                                                                                                                        |
| **TM**        | $^{\circ}C$                        | Maximaltemp.                          | tt (scraped)                                                                                                                                                                        |
| **Tm**        | $^{\circ}C$                        | Minimaltemp.                          | tt (scraped)                                                                                                                                                                        |
| **PP**        | $mm$                        | Jahresniederschlag                    | tt (scraped)                                                                                                                                                                        |
| **V**         | $\frac{km}{h}$              | Durchschnittliche Windgeschwindigkeit | tt (scraped)                                                                                                                                                                        |
| **RA**        | -                           | Regentage                             | tt (scraped)                                                                                                                                                                        |
| **SN**        | -                           | Schneetage                            | tt (scraped)                                                                                                                                                                        |
| **TS**        | -                           | Sturmtage                             | tt (scraped)                                                                                                                                                                        |
| **FG**        | -                           | Nebeltage                             | tt (scraped)                                                                                                                                                                        |
| **TN**        | -                           | Tornadotage                           | tt (scraped)                                                                                                                                                                        |
| **GR**        | -                           | Hageltage                             | tt (scraped)                                                                                                                                                                        |
| **MpA/dt**    | $mm\ w.e. = \frac{kg}{m^2}$ | Massenänderung pro Fläche             | na (abgeschrieben)                                                                                                                                                                  |
| **L/dt**      | $m$                         | Längenänderung                        | na (abgeschrieben)                                                                                                                                                                  |
| **L**         | $m$                         | Länge                                 | Hergeleitet aus $\frac{L}{dt}$ und gegebener $Länge\ um\ 1999$ in der Aufgabenstellung (dort ohne Quelle)                                                                           |
| **A**         | km²                         | Fläche                                | Berechnet aus $L$ und fest angenommener $B$                                                                                                                                         |
| **M**         | $Mrd.\ t$                   | Durchschnittliche Masse               | Hergeleitet aus $\frac{MpA}{dt}$ und der $MpA$ um 1999 (diese ist berechnet aus dem in der Aufgabenstellung gegebenem $V$, der durchschnittlichen $Dichte\ \rho\ von\ Eis$ und $A$) |



## data_all.csv

Hierbei handelt es sich um tagesweise erhobene Wetterdaten. Es wurden keine Daten aus anderen hergeleitet, dementsprechend ist hier weniger Aufwand vonnöten - schlicht das Scraping wurde durchgeführt mit den in diesem Ordner befindlichen Python-Dateien.

| **Dimension** | **Einheit**    | **Beschreibung**                                                            | **Herkunft**          |
|---------------|----------------|-----------------------------------------------------------------------------|-----------------------|
| **Y**         | -              | Jahr                                                                        | tt (scraped)          |
| **M**         | -              | Monat                                                                       | tt (scraped)          |
| **D**         | -              | Tag                                                                         | tt (scraped)          |
| **T**         | $^{\circ}C$           | Durchschnittstemp.                                                          | tt (scraped)          |
| **TM**        | $^{\circ}C$           | Maximale Durchschnittstemp.                                                 | tt (scraped)          |
| **Tm**        | $^{\circ}C$           | Minimale Durchschnittstemp.                                                 | tt (scraped)          |
| **SLP**       | $hPa$          | Luftdruck auf Meereshöhe                                                    | tt (scraped)          |
| **H**         | -            | rel. Luftfeuchte                                                            | tt (scraped)          |
| **PP**        | $mm$           | Niederschlag                                                                | tt (scraped)          |
| **VV**        | $km$           | Durchschnittliche Sicht                                                     | tt (scraped)          |
| **V**         | $\frac{km}{h}$ | Mittelwind                                                                  | tt (scraped)          |
| **VM**        | $\frac{km}{h}$ | Durchschnittlicher anhaltender Wind                                         | tt (scraped)          |
| **VG**        | $\frac{km}{h}$ | Maximale Windgeschwindigkeit                                                | tt (scraped)          |
| **RA**        | -              | Regentage                                                                   | tt (scraped)          |
| **SN**        | -              | Schneetage                                                                  | tt (scraped)          |
| **TS**        | -              | Sturmtage                                                                   | tt (scraped)          |
| **FG**        | -              | Nebeltage                                                                   | tt (scraped)          |
| **t**         | -              | Jahr seit 1955 addiert zur Gleitkommazahl mit Tagen als Quotient durch 366. | Berechnet aus Y, M, D |



