# Gruppe 3 - Massenbilanz des Rhonegletschers

## Daten

- [Daten zum Scrapen](https://de.tutiempo.net/klima/ws-67200.html#google_vignette)
- [Zum Abgleich Modell-Wirklichkeit](https://naturwissenschaften.ch/snow-glaciers-permafrost-explained/glaciers/mass_balance/rhone)

## Annahmen

### Akkumulation

Der Gletscher wird näherungsweise als Quader beschrieben, der eine feste Breite ($B=2km$) hat und dessen Verhätnis zwischen Höhe und Länge immer gleich ist. Man geht weiter davon aus, dass der Niederschlag gleichmäßig auf die gesamte sichtbare Oberfläche, d.h. die obere Oberfläche, trifft und all dieser Niederschlag auch gefriert, sofern die Temperaturen auf den entsprechenden Höhen unter $2°C$ liegt. Für die Massenzunahme des Gletschers geht man weiter davon aus, dass die gesamte Flächenzunahme auf der Längenzunahme beruht ($A = l \cdot B, B = konst.$).

$$Z(t) = PP(t) \cdot \rho_{Wasser} \cdot c \cdot B \cdot M(t)$$


### Ablation

Ab einer Temperatur von $2°C$ schmilzt der Gletscher. Wenn die Temperatur $T(t) > 2°C$ und es regnet wird die Schmelze um einen unbekannten Faktor $f$ beschleunigt, da Niederschlag eine bessere Wärmleitung ermöglicht.

$$A(t) = M(t) \cdot d \cdot (T(t) - T_0) + PP(t) \cdot f \cdot M(t) \cdot (T(t) - T_0)$$

### Vernachlässigung

Wir vernachlässigen die Einflüsse von

- Luftfeuchtigkeit
- Direkter Sonneneinstrahlung / Albedo
- Wind
- Hangneigung
- der konstanten Sublimation


