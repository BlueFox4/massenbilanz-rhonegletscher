import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

DATA_ALL_PATH = ""
DATA_YEAR_PATH = ""


def Massen(temp, pp, mass, c, d, f, change_velocity):
    new_mass = mass
    snow = 0    #falls es schneit wird akkumuliert: 1
    not_freeze = 0  #falls es nicht friert schmilzt etwas: 1
    pp = pp / 1000
    for hoehe in range(14):
        temp = temp  - 0.65
        if temp < 2:
            snow = 1
            not_freeze = 0
        elif temp > 2:
            snow = 0
            not_freeze = 1
        else:
            snow = 0
            not_freeze = 0
        new_mass = new_mass + change_velocity * (1 / 14) * (new_mass * (new_mass * snow * pp * c - (not_freeze * temp * (d + pp * f))))
        print(new_mass)

    return new_mass


Startmasse = 2.04714 * (10 ** 6) #tausend tonnen
masse = []
datum = []
avg_temp = []
avg_pp = []
tats_masse = []

with open("data_all.csv") as file:
    for i, line in enumerate(file.readlines()):
        if i == 0:
            continue
        else:
            datum.append((int(line.split(",")[0]), int(line.split(",")[1]), int(line.split(",")[2])))
            #print(datum[i-1])
            try:
                avg_temp.append(float(line.split(",")[3]))
            except ValueError:
                avg_temp.append(avg_temp[i - 2])

            try:
                avg_pp.append(float(line.split(",")[8]))
            except ValueError:
                avg_pp.append(avg_temp[i - 2])

with open("data_year.csv") as file:
    for i, line in enumerate(file.readlines()):
        if i > 0:
            if int(line.strip().split(",")[0]) >= 1999 and float(line.strip().split(",")[0]) <= 2023:
                tats_masse.append(float(line.strip().split(",")[16]) * (10 ** 6))

def calc(c, d, f, ch_vel):
    masse.clear()
    for i, day in enumerate(datum):
        if i == 0:
            aktuelle_masse = Startmasse

        aktuelle_masse = Massen(avg_temp[i], avg_pp[i], aktuelle_masse, c, d, f, ch_vel)
        masse.append(aktuelle_masse)
        print(i, aktuelle_masse)


calc(5.012 * (10 ** -7), 3.162 * (10 ** -3), 0.1, 0.1)
#print(masse)
fig, ax = plt.subplots()
c_slidax = plt.axes([0.1, 0, 0.8, 0.05])
d_slidax = plt.axes([0.1, 0.05, 0.8, 0.05])
f_slidax = plt.axes([0.1, 0.1, 0.8, 0.05])
ch_vel_slidax = plt.axes([0.1, 0.15, 0.8, 0.05])

c_slider = Slider(c_slidax, "c", 0, 0.000001, valinit=5.012 * (10 ** -7))
d_slider = Slider(d_slidax, "d", 0, 0.01, valinit=0.002)
f_slider = Slider(f_slidax, "f", 0, 0.1, valinit=3.162 * (10 ** -3))
ch_vel_slider = Slider(ch_vel_slidax, "vel", 0.001, 0.1)

graph, = ax.plot(masse)
x_vals = []
for i in range(365, 9132, 365):
    x_vals.append(i)
compare, = ax.plot(x_vals, tats_masse, marker="x")
rain_data =[]
for i in avg_pp:
    rain_data.append(i * 10000)
rain, = ax.plot(rain_data, marker="o", linestyle="none")

fig.subplots_adjust(bottom=0.2)

def update(val):
    c = c_slider.val
    d = d_slider.val
    f = f_slider.val
    change_velocity = ch_vel_slider.val
    calc(c, d, f, change_velocity)
    graph.set_ydata(masse)
    ax.relim()
    ax.autoscale_view()
    fig.canvas.draw_idle()
ch_vel_slider.on_changed(update)
c_slider.on_changed(update)
d_slider.on_changed(update)
f_slider.on_changed(update)
plt.show()