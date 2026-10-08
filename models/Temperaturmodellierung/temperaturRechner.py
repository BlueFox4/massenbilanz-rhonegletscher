#Eingabe: Tage nach 1.1.1999 <--> t=0 und Höhe (Wetterstation bei 482m)
import math
import numpy as np
from datetime import date, timedelta
import spezifischesJahr.besteParameterEntwicklung as params

def f(x, a, b, c , d):
    return a*np.sin(2*np.pi*(x-c)/b)+d


# Gives the temperature at a given time and a given height since year 0 (e.g. 1995 + (10/366)) by
# approximating the temperature as a sine wave with 4 different parameters which
# themselve are linear functions. Since and until simply tells over which time slot 
# these parameters should be approximated on the given data
#
# Param factor: used for modelling future developments; just influences the slope of the 
# curve after the axis x = until
def erhalteTemperatur(t, h, since, until=date.today().year, factor=1):
    year = math.floor(t)
    tag = (t - year) * 366

    a = params.a_func(t, since, until)
    b = params.b_func(t, since, until)
    c = params.c_func(t, since, until)
    d = params.d_func(t, since, until, factor)
    temperatur_wetterstation = f(tag, a, b, c, d)
    temperatur = temperatur_wetterstation - 0.65 * ( (h-482) / 100 )
    return temperatur*factor


if __name__ == "__main__":
    time=1955+(8*31/366)
    hoehe=2000
    while time < 2101:
        print(f"{time}: Model since 1994 {round(erhalteTemperatur(time, hoehe, 1994))}°C | Model since 2014 {round(erhalteTemperatur(time, hoehe, 2014))}°C")
        time += 1