#Eingabe: Tage nach 1.1.1999 <--> t=0 und Höhe (Wetterstation bei 482m)
import numpy as np
from datetime import date, timedelta

#Intervall der betrachteten Jahre für zukünftige Prognosen
BETRACHTETE_JAHRE = [2020, 2024]

def berechneJahrTag(t):
    tagNull = date(1999, 1, 1)
    gesuchterTag = tagNull + timedelta(days=t)
    return ([gesuchterTag.year, int(gesuchterTag.strftime('%j'))-1])

def berechneParameter(jahr):
    if (jahr < 2025):
        file =  open(f"models/Temperaturmodellierung/spezifischesJahr/bestenParameter.csv",'r')
        alleBestenParameter = file.readlines()
        alleBestenParameter.pop(0)
        for bestenParameter in alleBestenParameter:
            bestenParameter = bestenParameter[:-1].split(",")
            if int(bestenParameter[0]) == jahr:
                return ([float(bestenParameter[1]), float(bestenParameter[2]), float(bestenParameter[3]), float(bestenParameter[4])])
        print(f"Konnte das Jahr {jahr} nicht finden, verwendet voriges Jahr ({jahr-1}).")
        return(berechneParameter(jahr-1))
    else:
        #Prognose für nächsten Jahre soll Mittelwert der letzten 5 Jahre sein
        file =  open(f"models/Temperaturmodellierung/spezifischesJahr/bestenParameter.csv",'r')
        alleBestenParameter = file.readlines()
        alleBestenParameter.pop(0)
        summenParameter = [0, 0, 0, 0]
        for bestenParameter in alleBestenParameter:
            bestenParameter = bestenParameter[:-1].split(",")
            if int(bestenParameter[0]) <= BETRACHTETE_JAHRE[1] and  int(bestenParameter[0]) >= BETRACHTETE_JAHRE[0]:
                summenParameter[0] += float(bestenParameter[1])
                summenParameter[1] += float(bestenParameter[2])
                summenParameter[2] += float(bestenParameter[3])
                summenParameter[3] += float(bestenParameter[4])
        anzahl = BETRACHTETE_JAHRE[1]-BETRACHTETE_JAHRE[0]+1
        return([summenParameter[0]/anzahl, summenParameter[1]/anzahl, summenParameter[2]/anzahl, summenParameter[3]/anzahl])


def f(x, a, b, c , d):
    return a*np.sin(2*np.pi*(x-c)/b)+d

def erhalteTemperatur(t, h):
    [jahr, tag] = berechneJahrTag(t)
    [a, b, c, d] = berechneParameter(jahr)
    temperatur_wetterstation = f(tag, a, b, c, d)
    temperatur = temperatur_wetterstation - 0.65 * ( (h-482) / 100 )
    return temperatur

tag=10250
hoehe=2000
print(berechneJahrTag(tag))
print(erhalteTemperatur(tag, hoehe))