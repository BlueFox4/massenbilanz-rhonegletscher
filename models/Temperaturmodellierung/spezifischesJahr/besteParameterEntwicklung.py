import numpy as np
import math
import matplotlib.pyplot as plt

#Lesen der Daten aus Datei bestenParameter.csv
file =  open(f"models/Temperaturmodellierung/spezifischesJahr/bestenParameter.csv",'r')  # open braucht den genauen Pfad ab working directory
Jahre = file.readlines()
Jahre.pop(0) # Entferne Beschriftung
x = []
a = []
b = []
c = []
d = []
for jahr in Jahre:
    jahr = jahr[:-1].split(",")
    x.append(int(jahr[0]))
    a.append(float(jahr[1]))
    b.append(float(jahr[2]))
    c.append(float(jahr[3]))
    d.append(float(jahr[4]))
file.close()

x = np.array(x)
a = np.array(a)
b = np.array(b)
c = np.array(c)
d = np.array(d)

# Ausgleichsgeraden berechnen
a_fit = np.polyfit(x, a, 1)
c_fit = np.polyfit(x, c, 1)
d_fit = np.polyfit(x, d, 1)

# ===========
# Funktionen für Import als Modul
# ===========

last_fit_since = 0
last_d_factor = 1
a_func_polynomial = np.polynomial.Polynomial.fit(x[x >= last_fit_since], a[x >= last_fit_since], deg=1)
b_func_polynomial = np.polynomial.Polynomial.fit(x[x >= last_fit_since], b[x >= last_fit_since], deg=1)
c_func_polynomial = np.polynomial.Polynomial.fit(x[x >= last_fit_since], c[x >= last_fit_since], deg=1)
d_func_polynomial = np.polynomial.Polynomial.fit(x[x >= last_fit_since], d[x >= last_fit_since], deg=1)
t, m = d_func_polynomial.convert().coef
d_func_polynomial_scaled = np.polynomial.Polynomial([t, m*last_d_factor])

def a_func(y, since):
    global a_func_polynomial
    global last_fit_since
    if last_fit_since != since:
        a_func_polynomial = np.polynomial.Polynomial.fit(x[x >= since], a[x >= since], deg=1)
        last_fit_since = since
    return a_func_polynomial(y)
def b_func(y, since):
    global b_func_polynomial
    global last_fit_since
    if last_fit_since != since:
        b_func_polynomial = np.polynomial.Polynomial.fit(x[x >= since], b[x >= since], deg=1)
        last_fit_since = since
    return b_func_polynomial(y)
def c_func(y, since):
    global c_func_polynomial
    global last_fit_since
    if last_fit_since != since:
        c_func_polynomial = np.polynomial.Polynomial.fit(x[x >= since], c[x >= since], deg=1)
        last_fit_since = since
    return c_func_polynomial(y)
def d_func(y, since, factor=1):
    global d_func_polynomial
    global d_func_polynomial_scaled
    global last_fit_since
    global last_d_factor
    if last_fit_since != since and last_d_factor != factor:
        d_func_polynomial = np.polynomial.Polynomial.fit(x[x >= since], d[x >= since], deg=1)
        t, m = d_func_polynomial.convert().coef
        d_func_polynomial_scaled = np.polynomial.Polynomial([t, m*factor])
        last_fit_since = since
        last_d_factor = factor
    return d_func_polynomial_scaled(y)


# =======
# Visuelle Darstellung, wenn direkt aufgerufen
# =======

if __name__ == "__main__":
    fig, ax = plt.subplots(figsize = (10, 4))
    plt.title(f"BestenParameter Entwicklung")
    plt.subplots_adjust(left = 0.12, bottom = 0.3)
    plt.xlim(1955, 2025)
    plt.ylim(0, 400)
    plt.xlabel(r"$Jahr$")
    plt.ylabel(r"Wert", rotation = 90)
    
    # Datenpunkte
    a_Graph, = plt.plot(x, a, 'b.', lw=1)
    b_Graph, = plt.plot(x, b, 'y-', lw=1, label="Periode")
    c_Graph, = plt.plot(x, c, 'r.', lw=1)
    d_Graph, = plt.plot(x, d, 'g.', lw=1)

    # Gleichungen in Konsole ausgeben
    print(f"Amplitude: y = {a_fit[0]:.6f}x + {a_fit[1]:.6f}")
    print(f"Phasenverschiebung: y = {c_fit[0]:.6f}x + {c_fit[1]:.6f}")
    print(f"Temperaturmittel: y = {d_fit[0]:.6f}x + {d_fit[1]:.6f}")

    # Gerade aus den Koeffizienten erstellen
    a_line = np.polyval(a_fit, x)
    c_line = np.polyval(c_fit, x)
    d_line = np.polyval(d_fit, x)

    # Ausgleichsgeraden zeichnen
    plt.plot(x, a_line, 'b-', lw=1.5, label="Amplitude")
    plt.plot(x, c_line, 'r-', lw=1.5, label="Phasenverschiebung")
    plt.plot(x, d_line, 'g-', lw=1.5, label="Temperaturmittel")

    plt.legend()

    plt.show()