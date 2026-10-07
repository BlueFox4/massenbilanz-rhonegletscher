# Gruppe 3 - Massenbilanz des Rhonegletschers

## Daten

- [Daten zum Scrapen](https://de.tutiempo.net/klima/ws-67200.html#google_vignette)
- [Zum Abgleich Modell-Wirklichkeit](https://naturwissenschaften.ch/snow-glaciers-permafrost-explained/glaciers/mass_balance/rhone)


### Bericht

Der Bericht wird in Markdown (teilweise mit eingebettetem [LaTeX](https://www.latex-project.org/)) geschrieben und anschließend mit [Pandoc](https://pandoc.org/) in eine PDF umgewandelt.

Ist Pandoc ordnungsgemäß installiert, inkl. der PDF-Engine `xelatex` (eben für die LaTeX), tut es folgender Befehl:

```sh
cd bericht
pandoc Bericht.md -o Bericht.pdf --pdf-engine=xelatex
```

