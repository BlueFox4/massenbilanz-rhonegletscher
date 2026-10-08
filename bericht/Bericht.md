---
title: Massenbilanz des Rhonegletschers
subtitle: Wie können Messdaten genutzt werden, um die zeitliche Veränderung der Masse des Rhonegletschers mathematisch zu beschreiben?
date: \today
lang: de
papersize: a4

numbersections: true

author: 
- Benjamin Burkhardt
- Ole Hayn
- Fabian Lehmann
- Neo Koidl
- Jona Jeritslev
- Magnus Wagner

header-right: MODWO2026 Kassel
footer-left: Gruppe 3

hanging-indent: true
linestretch: 1.5

geometry:
  - top=25mm
  - bottom=25mm
  - left=25mm
  - right=25mm
---

# tl;dr

\newpage

\tableofcontents


# Zielsetzung

Der Rhonegletscher ist ein Gletscher in der Schweiz, von dem bereits seit Mitte des letzten Jahrhunderts Messdaten über Länge, Breite, Höhe (Volumen) sowie über das Wetter, etwa Niederschlagmenge, Regentage, Temperatur sowie Windstärke und -richtung vorliegen. Unser Ziel liegt nun darin, im ersten Schritt ein Modell zu entwickeln, das die Massenveränderung des Gletschers historisch bestmöglich beschreibt, und dann weiter die Wetterdaten auf Basis von Saisonalitäten und Trends so in die Zukunft zu prognostizieren, auf dass man eine begründete Vermutung über die zukünftige Massenveränderung des Gletschers abgeben kann.

\clearpage


# Daten

## Herkunft



## Aufbereitung



## Visualisierung



## Schwächen

Die Wetterstation, die die Daten erhoben hat, liegt etwa 90km südwestlicher Richtung vom Rhonegletscher entfernt. Dadurch ist eine gewisse Abweichung von den tatsächlichen Wetterverhältnissen am Gletscher zu erwarten.

![Das Problem mit der Entfernung](assets/luftlinie_klimastation_sion_rhonegletscher.png){width=70%}

Allerdings ist dieser Umstand vernachlässigbar, da die Station und der Gletscher im gleichen Tal liegen und somit den gleichen Wetterphänomenen ausgesetzt sind. 

![Die Entfernung ist jedoch im gleichen Tal](assets/meteoblue.com-2026-10-07_11-38_-_wetterkarte-im-tal.png){width=70%}

Zudem besitzt der ursprüngliche Datensatz teilweise Lücken, die mit interpolierten Daten ausgefüllt werden mussten.


\clearpage

# Modell

## Allgemeine Annahmen

### Temperatur

Zunächst wird der jährliche Temperaturverlauf mithilfe einer Sinus-Funktion modelliert.

$$y = a \cdot sin(2 \pi \cdot \frac{(x-c)}{b}) + d$$

![Durchschnittsjahr 1955-2025](assets/temp_avg_all_years.png){width=70%}

Nun werden programmatisch numerisch optimierte Parameter für jedes Jahr gefunden. 

Über diese vier Parameter $a$, $b$, $c$ und $d$ lässt sich je eine Ausgleichsgerade bilden und damit der zukünftige Verlauf modellieren:

$$y = a_{regr}(t) \cdot sin(2 \pi \cdot \frac{(x-c_{regr}(t))}{b_{regr}(t)}) + d_{regr}(t)$$

![Parameterentwicklung ($b, c = const.$)](assets/temp_params_development.png){width=70%}

Je nachdem, seit wann man die Regressionsgerade bildet, ergeben sich unterschiedliche Steigungen, wir gehen jedoch von einer 30-jährigen Klimaperiode aus und haben Daten bis 2024 - daraus folgt eine Regression über alle Jahresparameter von 1994 bis 2024.

![Modellierte Temperaturentwicklung mit Daten seit 1994 und 2014](assets/temp_modelled_twice.png){width=70%}

### Niederschlag

Beim Niederschlag lässt sich - betrachtet man die Jahresverläufe - zunächst keine Regelmäßigkeit ausmachen.

![Gegenüberstellung der Tagesniederschläge 1994 und 2014](assets/pp_gegenueberstellung-1994-2014.png){width=70%}

Kumuliert man jedoch die Tageswerte monatlich und zeichnet eine Ausgleichsgerade durch diese, erhält man eine Funktion, die den Niederschlag pro Monat in $\frac{mm}{Monat}$ annähert. Da die Daten eine hohe Streuung haben, ist dies für den einzelnen Zeitpunkt jedoch ungenau. Um zu validieren, dass zumindest die Steigung stimmt, kumuliert man nun die Regentage jährlich (da diese eine deutlich geringere Streuung aufweisen) und zeichnet auch hier eine Regressionsgerade, zeigt sich ein ähnliches Bild.

![Jährliche Regentagsanzahl, Monatliche Niederschläge und die Ausgleichsgeraden](assets/pp_modelliert.png){width=70%}

\clearpage

## Akkumulation

Der Gletscher wird näherungsweise als Quader beschrieben, der eine feste Breite ($B=2km$) hat und dessen Verhätnis zwischen Höhe und Länge immer gleich ist. Man geht weiter davon aus, dass der Niederschlag gleichmäßig auf die gesamte sichtbare Oberfläche, d.h. die obere Oberfläche, trifft und all dieser Niederschlag auch gefriert, sofern die Temperaturen auf den entsprechenden Höhen unter $2°C$ liegt. Für die Massenzunahme des Gletschers geht man weiter davon aus, dass die gesamte Flächenzunahme auf der Längenzunahme beruht ($A = l \cdot B, B = const.$).

$$Z(t) = PP(t) \cdot \rho_{Wasser} \cdot c \cdot B \cdot M(t)$$


## Ablation

Ab einer Temperatur von $2°C$ schmilzt der Gletscher. Wenn die Temperatur $T(t) > 2°C$ und es regnet wird die Schmelze um einen unbekannten Faktor $f$ beschleunigt, da Niederschlag eine bessere Wärmleitung ermöglicht.

$$A(t) = M(t) \cdot d \cdot (T(t) - T_0) + PP(t) \cdot f \cdot M(t) \cdot (T(t) - T_0)$$



## Vernachlässigung

Wir vernachlässigen die Einflüsse von

- Luftfeuchtigkeit
- Direkter Sonneneinstrahlung / Albedo
- Wind
- Hangneigung
- der konstanten Sublimation

\clearpage


# Fazit

- ca 90km Luftlinie zwischen Messstation und Gletscher (und einige Höhenmeter)