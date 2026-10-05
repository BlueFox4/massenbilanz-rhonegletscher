import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons, Slider


# Get all data and parse it into one beautiful (gigantic) python dictionary
with open('data/data_year.csv','r') as f:
    data = f.readlines()[1:]

data_dict = {
    "year": [],
    "avg_temp": [],
    "avg_temp_max": [],
    "avg_temp_min": [],
    "avg_preci": [],
    "avg_wind_speed": [],
    "rain_days": [],
    "snow_days": [],
    "thunderstorm_days": [],
    "fog_days": [],
    "tornado_days": [],
    "hail_days": [],
    "MpA/dt": [],
    "L/dt": [],
    "L": [],
    "A": [],
    "M": [],
}

for datum in data:
    datum = datum.split(",")
    for i, l in enumerate(data_dict.values()):
        try:
            l.append(float(datum[i].strip()))
        except ValueError:
            l.append(np.nan)


data_dict_annotations = {
    "color": [
        "",                # year
        "cyan",            # avg temp
        "red",             # avg temp max
        "blue",            # avg temp min
        "gray",            # precipitation
        "olive",           # avg wind speed
        "navy",            # rain days
        "gainsboro",       # snow days
        "gold",            # thunder days
        "lightslategray",  # fog days
        "magenta",         # tornado days
        "firebrick",       # hail days
        "indigo",          # MpA/dt
        "turquoise",       # L/dt
        "forestgreen",     # L
        "fuchsia",         # A
        "black",           # M
    ],
    "factor": [
        1,      # year
        1,      # avg temp
        1,      # avg temp max
        1,      # avg temp min
        0.01,   # precipitation
        1,      # avg wind speed
        0.1,    # rain days
        1,      # snow days
        1,      # thunder days
        1,      # fog days
        1,      # tornado days
        1,      # hail days
        0.001,  # MpA/dt
        0.1,    # L/dt
        0.001,  # L
        1,      # A
        10,     # M
    ],
    "unit": [
        "",         # year
        "°C",       # avg temp
        "°C",       # avg temp max
        "°C",       # avg temp min
        "mm",       # precipitation (+ melted snow)
        "km/h",     # avg wind speed
        "",         # rain days
        "",         # snow days
        "",         # thunder days
        "",         # fog days
        "",         # tornado days
        "",         # hail days
        "mm w.e.",  # MpA/dt
        "m/t",      # L/dt
        "m",        # L
        "km²",      # A
        "Mrd. t",   # M
    ],
    "linestyle": [
        "",     # year
        "-",    # avg temp
        "-.",   # avg temp max
        "-.",   # avg temp min
        "-",    # precipitation (+ melted snow)
        "-.",   # avg wind speed
        "-",    # rain days
        "-",    # snow days
        "-.",   # thunder days
        "-.",   # fog days
        "-.",   # tornado days
        "-.",   # hail days
        "-.",   # MpA/dt
        "-.",   # L/dt
        "-",    # L
        "-.",   # A
        "-",    # M
    ],
    "visibility": [
        True,     # year
        True,     # avg temp
        False,    # avg temp max
        False,    # avg temp min
        True,     # precipitation
        True,     # avg wind speed
        True,     # rain days
        True,     # snow days
        False,    # thunder days
        False,    # fog days
        False,    # tornado days
        False,    # hail days
        False,   # MpA/dt
        False,   # L/dt
        False,   # L
        False,   # A
        True,    # M
    ],
}

# Now the plotting part
fig, ax = plt.subplots()
plots = []
for i, (key, value) in enumerate(data_dict.items()):
    key_beautified = key.replace("_", " ").capitalize()
    if key == "year":
        continue
    factor = data_dict_annotations['factor'][i]
    division_by = 1/factor
    unit = data_dict_annotations['unit'][i]
    linestyle = data_dict_annotations['linestyle'][i]
    visibility = data_dict_annotations['visibility'][i]
    label = f"{key_beautified} {'in ' + unit if unit != "" else ''} {' /' + str(division_by) if division_by != 1 else ''}"
    color = data_dict_annotations['color'][i]
    plots += ax.plot(data_dict["year"], np.array(value)/division_by, visible=visibility, label=label, marker=".", linestyle=linestyle, c=color)

ax.legend(loc='lower right', ncol=3, prop={'size': 7})
plots_by_label = {p.get_label(): p for p in plots}


# Show/Hide logic

rax = ax.inset_axes([0.0, 0.0, 0.2, 0.3])
check = CheckButtons(
    ax=rax,
    labels=plots_by_label.keys(),
    actives=[p.get_visible() for p in plots_by_label.values()],
    label_props={'color': data_dict_annotations["color"][1:]},
    frame_props={'edgecolor': data_dict_annotations["color"][1:]},
    check_props={'facecolor': data_dict_annotations["color"][1:]},
)
for label in check.labels:
    label.set_fontsize(7)
def callback(label):
    pn = plots_by_label[label]
    pn.set_visible(not pn.get_visible())
    pn.figure.canvas.draw_idle()
    ax.legend(loc='lower right', ncol=3, prop={'size': 7})
check.on_clicked(callback)

plt.show()