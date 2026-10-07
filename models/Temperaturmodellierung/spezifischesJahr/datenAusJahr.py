import numpy as np


def getJahresdaten(jahreszahl):
    with open(f'data/data_all.csv','r') as file:  # open braucht den genauen Pfad ab working directory
        daten = file.readlines()[1:]
        for i in range(len(daten)):
            daten[i] = daten[i].strip().split(",")
    jahresdaten = []
    for d in daten:
        if int(d[0]) == jahreszahl:
            jahresdaten.append(np.asarray(d, dtype=float))
    return(jahresdaten)

def getAlleJahre():
    with open(f'data/data_all.csv','r') as file:  # open braucht den genauen Pfad ab working directory
        daten = file.readlines()[1:]
        for i in range(len(daten)):
            daten[i] = daten[i].strip().split(",")
    alleJahre=[]
    jahreszahl = 1955
    jahresdaten=[]
    for d in daten:
        if int(d[0]) == jahreszahl:
            jahresdaten.append(np.asarray(d, dtype=float))
        else:
            alleJahre.append(jahresdaten)
            jahresdaten = []
            jahresdaten.append(np.asarray(d, dtype=float))
            jahreszahl = int(d[0])
    alleJahre.append(jahresdaten)
    return(alleJahre)

def getAlleJahreTemperatur():
    alleJahre = getAlleJahre()
    alleJahreTemperatur = []
    for i in range(len(alleJahre)):
        jahrTemperatur = []
        jahr = alleJahre[i]
        print(f"Jahr mit allem: {len(jahr)}")
        for j in range(len(jahr)):
            jahrTemperatur.append(jahr[j][3])
        alleJahreTemperatur.append(jahrTemperatur)
        print(f"Jahr mit Temperatur: {len(jahrTemperatur)}")

    return alleJahreTemperatur

if __name__ == "__main__":
    getAlleJahreTemperatur()