#Eingabe: Tage nach 1.1.1999 <--> t=0 und Höhe (Wetterstation bei 482m)
import math
import numpy as np
from datetime import date, timedelta
import spezifischesJahr.besteParameterEntwicklung as params

def f(x, a, b, c , d):
    return a*np.sin(2*np.pi*(x-c)/b)+d

def erhalteTemperatur(t, h, since):
    year = math.floor(t)
    tag = (t - year) * 366

    temperatur_wetterstation = f(tag, params.a_func(t, since), params.b_func(t, since), params.c_func(t, since), params.d_func(t, since))
    temperatur = temperatur_wetterstation - 0.65 * ( (h-482) / 100 )
    return temperatur


if __name__ == "__main__":
    time=1994+(8*31/366)
    hoehe=2000
    while time < 2101:
        print(f"{time}: Model since 1994 {round(erhalteTemperatur(time, hoehe, 1994))}°C | Model since 2014 {round(erhalteTemperatur(time, hoehe, 2014))}°C")
        time += 1