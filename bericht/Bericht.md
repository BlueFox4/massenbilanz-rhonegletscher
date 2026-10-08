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

Im Zuge der Modellierungswoche 2026, einem Projekt des Zentrums für Mathematik, wurde ein Modell entwickelt, welches auf Basis von historischen Wetterdaten einerseits näherungsweise die historische Massenveränderung des Rhonegletschers im Kanton Wallis in der Schweiz nachstellt und im zweiten Schritt mit Prognosen für die zukünfitgen klimatischen Bedingungen auch die zukünftige Massenveränderung des Gletschers aufzeigt. Vorrangig wurde dabei eine Funktion für die Massenveränderung aufgestellt, welche gleich der Differenz der Massenakkumulation (Massenzunahme) des Gletschers und der Massenablation (Massenabhnahme) des Gletschers an einem gewissen Zeitpunkt ist. Dabei sind Massenakkumulation und Massenablation Funktionen, die von Niederschlag und Temperatur zu eben diesem Zeitpunkt abhängig sind. Niederschlag und Temperatur sind ihrerseits Funktionen, die sich aus Wetterdatensätzen der letzten 30 Jahre speißen. Zur optimalen Bestimmung der Modellparameter dienten Daten über die tatsächliche historische Massenbilanz des Gletschers.

\newpage

\tableofcontents


# Zielsetzung

Der Rhonegletscher ist ein Gletscher in der Südschweiz, von dem bereits seit Mitte des letzten Jahrhunderts Messdaten über Masse und Länge des Gletschers sowie über das Wetter, etwa Niederschlagmenge, Regentage, Temperatur sowie Windstärke und -richtung vorliegen. Unser Ziel liegt nun darin, im ersten Schritt ein Modell zu entwickeln, das die Massenveränderung des Gletschers historisch bestmöglich beschreibt, und dann weiter die Wetterdaten auf Basis von Saisonalitäten und Trends so in die Zukunft zu prognostizieren, auf dass man eine begründete Vermutung über die zukünftige Massenveränderung des Gletschers mittels eben diesem Modell abgeben kann.

\clearpage


# Daten

## Herkunft

Die historischen Daten über die Gletschermasse und -länge stammen von ["scnat wissen", dem Webportal der schweizer Akademie der Wissenschaften, aus einem Bericht der ETH Zürich](https://naturwissenschaften.ch/snow-glaciers-permafrost-explained/glaciers/mass_balance/rhone). Sie reichen bis 1900 zurück und wurden jährlich erhoben. Zur Überprüfung unserer Modellierung haben wir uns allerdings auf den Erhebungszeitraum zwischen 1955 und 2024 beschränkt.

Mittels eines Web-Scraping-Algorithmus wurden die tagesbezogenen Wetterdaten von einer Wetterstation in Sitten (franz. Sion), einer Stadt im Tal des Gletschers ermittelt. Sie liegen mehr oder minder kontinuierlich seit dem 1. Januar 1955 vor.

## Aufbereitung




## Schwächen

Die Wetterstation, die die Daten erhoben hat, liegt etwa 90km südwestlicher Richtung vom Rhonegletscher entfernt. Dadurch ist eine gewisse Abweichung von den tatsächlichen Wetterverhältnissen am Gletscher zu erwarten.

![Das Problem mit der Entfernung](assets/luftlinie_klimastation_sion_rhonegletscher.png){width=70%}

Allerdings ist dieser Umstand vernachlässigbar, da die Station und der Gletscher im gleichen Tal liegen und somit den gleichen Wetterphänomenen ausgesetzt sind. 

![Die Entfernung ist jedoch im gleichen Tal](assets/meteoblue.com-2026-10-07_11-38_-_wetterkarte-im-tal.png){width=70%}

Zudem besitzt der ursprüngliche Datensatz teilweise Lücken, die mit interpolierten Daten ausgefüllt werden mussten.


\clearpage

# Modell

## Annahmen

Zunächst nehmen wir den Gletscher als Quader mit fixer Breite $B = 1,5km$ an. Daraus folgt eine Abhängigkeit von der Länge $L$ für die Oberfläche $O(t) \propto L(t)$ und die Masse $M(t) \propto L(t)$ des Gletschers. Die Temperatur in der für unser Modell gewählten Standardatmosphäre nimmt alle $100m$ um $0,65^{\circ}\mathrm{C}$ ab.

Für die Akkumulation wird davon ausgegangen, dass Niederschlag ab einer Temperatur $T(t) < 2^{\circ}\mathrm{C}$ als der Gletschermasse zuträglich gewertet wird. 

Gleichzeitig wird Niederschlag ab einer Temperatur $T(t) > 2^{\circ}\mathrm{C}$ als der Masse abträglich (Ablation) gewertet. Dann kann man von einer Temperaturabhängigkeit sprechen: $A(t) \sim T(t)$

## Temperatur

Betrachtet man den durchschnittlichen jährlichen Temperaturverlauf, also die durchschnittliche Temperatur für einen bestimmten Tag im Jahresverlauf, lässt sich dieser gut durch eine Sinusfunktion modellieren:

$$
T(t) = a \cdot \sin\left(2\pi \cdot \frac{x-c}{b}\right) + d
$$

![Durchschnittsjahr 1955–2025](assets/temp_avg_all_years.png){width=70%}

Die einzelnen Parameter können dabei wie folgt interpretiert werden:

- $a$ bezeichnet die **Amplitude** in $^{\circ}\mathrm{C}$ und beschreibt, wie stark die Temperaturen im Jahresverlauf schwanken.
- $b$ bezeichnet die **Periodendauer** in Tagen. Dieser Wert wird sinnvollerweise auf $365{,}2524$ Tage festgelegt.
- $c$ bezeichnet die **Phasenverschiebung** in Tagen und gibt an, um welchen Betrag der Temperaturverlauf entlang der Zeitachse verschoben ist. Damit lässt sich insbesondere der Zeitpunkt des kältesten bzw. wärmsten Tages bestimmen.
- $d$ bezeichnet den **Temperaturmittelwert** in $^{\circ}\mathrm{C}$ und entspricht der vertikalen Verschiebung der Sinuskurve.

Statt den gesamten Messzeitraum durch eine einzige Sinuskurve zu beschreiben, werden die Parameter $a$, $c$ und $d$ nun für jedes Jahr separat bestimmt. Dadurch kann ihre zeitliche Entwicklung analysiert und für die Modellierung zukünftiger Jahre berücksichtigt werden. Die jeweils optimalen Parameter werden dabei programmatisch für jedes Jahr ermittelt und gespeichert.

Beispielhaft sind im Folgenden die ermittelten Parameter und die daraus resultierenden Sinuskurven für die Jahre 1994 und 2023 dargestellt:

![Temperatur-Sinuskurve für 1994](assets/temperaturmodell_1994.png){width=70%}

![Temperatur-Sinuskurve für 2023](assets/temperaturmodell_2023.png){width=70%}

Auf Grundlage der Parameter $a$, $b$, $c$ und $d$ lässt sich anschließend jeweils eine Regressionsgerade bestimmen. Diese beschreibt die zeitliche Entwicklung der einzelnen Parameter und kann verwendet werden, um den Temperaturverlauf zukünftiger Jahre zu modellieren:

![Entwicklung der Parameter $a$, $b$, $c$ und $d$](assets/temp_params_development.png){width=70%}

Die Entwicklung der Parameter lässt sich unter Berücksichtigung ihrer jeweiligen Bedeutung wie folgt interpretieren:

- Die **Amplitude $a$** steigt leicht an. Dies könnte darauf hindeuten, dass die jahreszeitlichen Temperaturschwankungen im betrachteten Zeitraum zunehmen. Ein möglicher Zusammenhang besteht mit zunehmenden Wetterextremen infolge des Klimawandels.
- Die **Periodendauer $b$** wurde bei der Berechnung der Parameter auf den festen Wert $365{,}2524$ Tage gesetzt und bleibt daher konstant.
- Die **Phasenverschiebung $c$** verändert sich nur geringfügig. Dies deutet darauf hin, dass sich der Zeitpunkt der jahreszeitlichen Temperaturminima und -maxima im betrachteten Zeitraum nur wenig verschoben hat. Allerdings ist dieser Zeitpunkt von verschiedenen meteorologischen und klimatischen Faktoren abhängig.
- Beim **Temperaturmittelwert $d$** ist hingegen ein deutlicher Anstieg von etwa $3^{\circ}\mathrm{C}$ über den betrachteten Messzeitraum zu erkennen. Dieser Anstieg steht im Einklang mit der allgemeinen Erwärmung im Zuge des Klimawandels.

Um die Genauigkeit der ermittelten Parameter zu bewerten, kann insbesondere der Parameter $d$, der den mittleren Temperaturwert eines Jahres beschreibt, mit den tatsächlich gemessenen Jahresmitteltemperaturen verglichen werden. In der unteren Abbildung stellt man fest, dass die tatsächlichen Werte nahezu identisch zu den modellierten Werten des Paramters $d$ sind.

Darüber hinaus stellt sich die Frage, welcher Zeitraum für die Bestimmung der Regressionsgeraden verwendet werden sollte. Wird der gesamte Messzeitraum betrachtet, ergibt sich eine geringere Steigung der Temperaturentwicklung. Dadurch könnte die aktuelle Erwärmung weniger deutlich abgebildet werden. Ein kürzerer Zeitraum reagiert dagegen stärker auf aktuelle Veränderungen, ist jedoch anfälliger für kurzfristige Schwankungen und einzelne ungewöhnlich warme oder kalte Jahre.

In der folgenden Abbildung sind die Regressionsgeraden für einen Zeitraum ab 2014 sowie für eine 30-jährige Klimaperiode von 1994 bis 2023 dargestellt. Wir haben uns bewusst gegen den kürzeren Zeitraum ab 2014 entschieden, da eine 30-jährige Periode besser geeignet ist, langfristige klimatische Entwicklungen abzubilden und den Einfluss kurzfristiger Schwankungen zu reduzieren.

![Modellierte Temperaturentwicklung mit Daten seit 1994 und 2014](assets/temp_modelled_twice.png){width=70%}

Zusammenfassend kann das Programm zur Berechnung der Massenbilanz nun für jeden beliebigen Zeitpunkt eine modellierte Temperatur bestimmen. Dazu wird zunächst der Zeitpunkt innerhalb des Jahres bestimmt und anschließend mit den für das jeweilige Jahr ermittelten Regressionsparametern die entsprechende Temperatur berechnet. Daraus ergibt sich die folgende Funktion:

$$
T(t) = a_{regr}(t) \cdot \sin\left(2\pi \cdot \frac{x-c_{regr}(t)}{b_{regr}(t)}\right) + d_{regr}(t)
$$

Die zugrunde liegenden Messdaten stammen von einer Wetterstation auf einer Höhe von $482,\mathrm{m}$. Der betrachtete Gletscher beginnt jedoch erst auf einer Höhe von etwa $2200,\mathrm{m}$, sodass dort von einer deutlich niedrigeren Temperatur auszugehen ist. Um diesen Höhenunterschied im Modell zu berücksichtigen, wird eine Temperaturabnahme von $0{,}65,^\circ\mathrm{C}$ pro $100,\mathrm{m}$ Höhenzunahme angenommen.

Damit kann aus den Messdaten der Wetterstation eine modellierte Temperaturentwicklung für die Höhe des Gletschers abgeleitet werden. Diese dient anschließend als Grundlage für die weitere Berechnung der Massenbilanz. Abschließen sieht man in der folgenden Abbildung unsere modellierte Temperatur und die tatsächlichen monatlichen Durchschnittwerte.

![Modellierte Temperaturentwicklung vs Daten con 1994 bis 2023](assets/modellWerteVsDatenTemperatur.png){width=70%}

## Niederschlag

Beim Niederschlag lässt sich - betrachtet man die Jahresverläufe - zunächst keine Regelmäßigkeit ausmachen.

![Gegenüberstellung der Tagesniederschläge 1994 und 2014](assets/pp_gegenueberstellung-1994-2014.png){width=70%}

Kumuliert man jedoch die Tageswerte monatlich und zeichnet eine Ausgleichsgerade durch diese, erhält man eine Funktion, die den Niederschlag pro Monat in $\frac{mm}{Monat}$ annähert. Da die Daten eine hohe Streuung haben, ist dies für den einzelnen Zeitpunkt jedoch ungenau. Um zu validieren, dass zumindest die Steigung stimmt, kumuliert man nun die Regentage jährlich (da diese eine deutlich geringere Streuung aufweisen) und zeichnet auch hier eine Regressionsgerade. Es zeigt sich eine ähnliche Steigung.

![Jährliche Regentagsanzahl, Monatliche Niederschläge und die Ausgleichsgeraden](assets/pp_modelliert.png){width=70% #fig:pp_modelliert}

Da die Niederschlagsmenge jedoch die richtige Einheit besitzt und somit genauer ist, fließt diese - wie die pinke Linie in Abbildung \ref{fig:pp_modelliert} zeigt - in unser tatsächliches Modell ein.

\clearpage

## Akkumulation

Der Gletscher wird näherungsweise als Quader beschrieben, der eine feste Breite ($B = 1,5km$) hat und dessen Verhältnis zwischen Höhe und Länge immer gleich ist. Man geht weiter davon aus, dass der Niederschlag gleichmäßig auf die gesamte sichtbare Oberfläche, d.h. die obere Oberfläche, trifft und all dieser Niederschlag auch gefriert, sofern die Temperaturen auf den entsprechenden Höhen unter $T_0 = 2^{\circ}\mathrm{C}$ liegt. Für die Massenzunahme des Gletschers geht man weiter davon aus, dass die gesamte Flächenzunahme auf der Längenzunahme beruht ($\frac{\text{Fläche}}{dt} = l \cdot B \text{, } B = const.$).

$$ 
Z(t) =
\begin{cases}
    0 & \text{für } T(t) \ge T_0 \\
    PP(t) \cdot \rho_{Wasser} \cdot c \cdot B \cdot M(t) & \text{für } T(t) < T_0
\end{cases}$$


## Ablation

Ab einer Temperatur $T_0 = 2^{\circ}\mathrm{C}$ schmilzt der Gletscher. Wenn die Temperatur $T(t) > 2^{\circ}\mathrm{C}$ und es regnet, wird die Schmelze um einen unbekannten Faktor $f$ beschleunigt, da Niederschlag eine bessere Wärmleitung ermöglicht. Beide Effekte sind direkt proportional zur Gletschermasse, da diese, unter unseren Annahmen, wiederum zur Gletscheroberfläche proportional ist und der Niederschlagseffekt auf der gesamten Oberfläche stattfindet. Der allgemeine Temperaturschmelzeffekt ist direkt massenabhängig, da Schmelze idealisiert für jedes Kilo Gletschereis gleichmäßig stattfindet. Der Temperaturgradient des Eises innerhalb des Gletschers, also der geringere Einfluss der Außentemperatur auf Eis, das nicht an der Luft liegt, wird als annähernd linear angenommen und fließt demnach in die Schmelzkonstante $d$ ein.

$$
A(t) = 
\begin{cases}
    PP(t) \cdot f \cdot M(t) \cdot (T(t) - T_0)
    + M(t) \cdot d \cdot (T(t)) 
    & \text{für } T(t) > 0 \\
    PP(t) \cdot f \cdot M(t) \cdot (T(t) - T_0) & \text{für } T(t) \le 0
\end{cases}
$$


## Vernachlässigung

In die derzetige Modellierung fließen bis dato nur die Temperatur und der Niederschlag ein. Dies scheint zwar eine soweit suffiziente Modellierung herzubieten, aber es ist davon auszugehen, dass der Einbezug weiterer Faktoren an dieser Stelle doch eine bessere Abbildung der Realität ermöglichen würde:

TODO:
- Breite nicht wirklich konstant
- Luftfeuchtigkeit
- Direkter Sonneneinstrahlung / Albedo
- Wind
- Hangneigung
- der konstanten Sublimation

\clearpage


# Fazit

- ca 90km Luftlinie zwischen Messstation und Gletscher (und einige Höhenmeter)