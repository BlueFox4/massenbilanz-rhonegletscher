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


 **Dimension**    | **T**          | **TM**           | **Tm**           | **PP**                 | **V**                                     | **RA**        | **SN**         | **TS**        | **FG**        | **TN**          | **GR**        | **MpA/dt**                    | **L/dt**           | **L**                                                                                       | **A**                              | **M**                                                                                                                                                         
--------------|------------|--------------|--------------|--------------------|---------------------------------------|-----------|------------|-----------|-----------|-------------|-----------|---------------------------|----------------|---------------------------------------------------------------------------------------------|-----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------
 **Einheit**      | $°C$         | $°C$           | $°C$           | $mm$                 | $\frac{km}{h}$                                  | -         | -          | -         | -         | -           | -         | $mm\ w.e. = \frac{kg}{m^2}$                   | $m$              | $m$                                                                                           | km²                                     | $Mrd.\ t$                                                                                                                                                   
 **Beschreibung** | Temperatur | Maximaltemp. | Minimaltemp. | Jahresniederschlag | Durchschnittliche Windgeschwindigkeit | Regentage | Schneetage | Sturmtage | Nebeltage | Tornadotage | Hageltage | Massenänderung pro Fläche | Längenänderung | Länge                                                                                       | Fläche                                  | Durchschnittliche Masse                                                                                                                                   
 **Herkunft**     | tt (scraped)         | tt (scraped)           | tt (scraped)           | tt (scraped)                 | tt (scraped)                                    | tt (scraped)        | tt (scraped)         | tt (scraped)        | tt (scraped)        | tt (scraped)          | tt (scraped)        | gl (abgeschrieben)                        | gl (abgeschrieben)             | Hergeleitet aus $\frac{L}{dt}$ und gegebener $Länge\ um\ 1999$ in der Aufgabenstellung (dort ohne Quelle) | Berechnet aus $L$ und fest angenommener $B$ | Hergeleitet aus $\frac{MpA}{dt}$ und der $MpA$ um 1999 (diese ist berechnet aus dem in der Aufgabenstellung gegebenem $V$, der durchschnittlichen $Dichte\ \rho\ von\ Eis$ und $A$) 


## data_all.csv

Hierbei handelt es sich um tagesweise erhobene Wetterdaten. Es wurden keine Daten aus anderen hergeleitet, dementsprechend ist hier weniger Aufwand vonnöten - schlicht das Scraping wurde durchgeführt mit den in diesem Ordner befindlichen Python-Dateien.

|**Dimension**   |**T**       |**TM**      |**Tm**      |**PP**            |**V**                                |**RA**      |**SN**      |**TS**      |**FG**      |**TN**      |**GR**      |**MpA/dt**                 |**L/dt**          |**L**                                                                                                    |**A**                                      |**M**                                                                                                                                                                              |
|----------------|------------|------------|------------|------------------|-------------------------------------|------------|------------|------------|------------|------------|------------|---------------------------|------------------|---------------------------------------------------------------------------------------------------------|-------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|**Einheit**     |$°C$        |$°C$        |$°C$        |$mm$              |$\frac{km}{h}$                       |-           |-           |-           |-           |-           |-           |$mm\ w.e. = \frac{kg}{m^2}$|$m$               |$m$                                                                                                      |km²                                        |$Mrd.\ t$                                                                                                                                                                          |
|**Beschreibung**|Temperatur  |Maximaltemp.|Minimaltemp.|Jahresniederschlag|Durchschnittliche Windgeschwindigkeit|Regentage   |Schneetage  |Sturmtage   |Nebeltage   |Tornadotage |Hageltage   |Massenänderung pro Fläche  |Längenänderung    |Länge                                                                                                    |Fläche                                     |Durchschnittliche Masse                                                                                                                                                            |
|**Herkunft**    |tt (scraped)|tt (scraped)|tt (scraped)|tt (scraped)      |tt (scraped)                         |tt (scraped)|tt (scraped)|tt (scraped)|tt (scraped)|tt (scraped)|tt (scraped)|na (abgeschrieben)         |na (abgeschrieben)|Hergeleitet aus $\frac{L}{dt}$ und gegebener $Länge\ um\ 1999$ in der Aufgabenstellung (dort ohne Quelle)|Berechnet aus $L$ und fest angenommener $B$|Hergeleitet aus $\frac{MpA}{dt}$ und der $MpA$ um 1999 (diese ist berechnet aus dem in der Aufgabenstellung gegebenem $V$, der durchschnittlichen $Dichte\ \rho\ von\ Eis$ und $A$)|

