import numpy as np
import matplotlib.pyplot as plt
from datetime import date
from matplotlib.widgets import CheckButtons, Slider


# Get all data and parse it into one beautiful (gigantic) python dictionary
with open('data/data_all.csv','r') as f:
    data = f.readlines()[1:]

data_dict = {
    "year": [],
    "month": [],
    "day": [],
    "avg_temp": [],
    "avg_temp_max": [],
    "avg_temp_min": [],
    "pressure_msl": [],
    "humidity": [],
    "avg_preci": [],
    "avg_visibility": [],
    "avg_wind_speed": [],
    "max_sustained_wind_speed": [],
    "max_wind_speed": [],
    "rain_day": [],
    "snow_day": [],
    "thunderstorm": [],
    "fog_day": []
}

for datum in data:
    datum = datum.split(",")
    for i, l in enumerate(data_dict.values()):
        try:
            l.append(float(datum[i].strip()))
        except ValueError:
            l.append(np.nan)

# Merge the first three data columns (year, month, day) and convert to a difference
data_dict["days_since_1955"] = []
for i,y in enumerate(data_dict["year"]):
    y = int(y)
    m = int(data_dict["month"][i])
    d = int(data_dict["day"][i])
    data_dict["days_since_1955"].append((date(y,m,d)-date(1955,1,1)).days)

data_dict.pop("year", None)
data_dict.pop("month", None)
data_dict.pop("day", None)

data_dict_annotations = {
    "color": [
        "cyan",            # avg temp
        "red",             # avg temp max
        "blue",            # avg temp min
        "teal",            # pressure msl
        "aqua",            # humidity
        "gray",            # precipitation
        "lawngreen",       # avg visibility
        "olive",           # avg wind speed
        "olivedrab",       # max sustained speed
        "yellowgreen",     # max wind speed
        "navy",            # rain days
        "gainsboro",       # snow days
        "gold",            # thunder days
        "lightslategray",  # fog days
        "",                # days since jan 1, 1955
    ],
    "factor": [
        1,  # avg temp
        1,  # avg temp max
        1,  # avg temp min
        0.001,  # pressure msl
        1,  # humidity
        1,  # precipitation
        1,  # avg visibility
        1,  # avg wind speed
        1,  # max sustained speed
        1,  # max wind speed
        1,  # rain days
        1,  # snow days
        1,  # thunder days
        1,  # fog days
        1,   # days since jan 1, 1955
    ],
    "unit": [
        "°C",    # avg temp
        "°C",    # avg temp max
        "°C",    # avg temp min
        "hPa",   # pressure msl
        "%",     # humidity
        "mm",    # precipitation
        "km",    # avg visibility
        "km/h",  # avg wind speed
        "km/h",  # max sustained speed
        "km/h",  # max wind speed
        "",      # rain days
        "",      # snow days
        "",      # thunder days
        "",       # fog days
        "",      # days since jan 1, 1955
    ],
    "linestyle": [
        "-",   # avg temp
        "-.",  # avg temp max
        "-.",  # avg temp min
        "-.",  # pressure msl
        "-",   # humidity
        "-",   # precipitation
        "-.",  # avg visibility
        "-",   # avg wind speed
        "-.",  # max sustained speed
        "-.",  # max wind speed
        "-",   # rain days
        "-",   # snow days
        "-.",  # thunder days
        "-.",   # fog days
        "-.",  # days since jan 1, 1955
    ],
    "visibility": [
        True,   # avg temp
        False,  # avg temp max
        False,  # avg temp min
        False,  # pressure msl
        True,   # humidity
        True,   # precipitation
        False,  # avg visibility
        True,   # avg wind speed
        False,  # max sustained speed
        False,  # max wind speed
        True,   # rain days
        True,   # snow days
        False,  # thunder days
        False,  # fog days
        True,   # days since jan 1, 1955
    ],
}

# Now the plotting part
fig, ax = plt.subplots()
plots = []
for i, (key, value) in enumerate(data_dict.items()):
    key_beautified = key.replace("_", " ").capitalize()
    if key == "days_since_1955":
        continue
    factor = data_dict_annotations['factor'][i]
    division_by = 1/factor
    unit = data_dict_annotations['unit'][i]
    linestyle = data_dict_annotations['linestyle'][i]
    visibility = data_dict_annotations['visibility'][i]
    label = f"{key_beautified} {'in ' + unit if unit != "" else ''} {' /' + str(division_by) if division_by != 1 else ''}"
    color = data_dict_annotations['color'][i]
    plots += ax.plot(data_dict["days_since_1955"], np.array(value)/division_by, visible=visibility, label=label, marker="", linestyle=linestyle, c=color)
ax.legend()
plots_by_label = {p.get_label(): p for p in plots}


# Show/Hide logic

rax = ax.inset_axes([0.0, 0.7, 0.25, 0.3])
check = CheckButtons(
    ax=rax,
    labels=plots_by_label.keys(),
    actives=[p.get_visible() for p in plots_by_label.values()],
    label_props={'color': data_dict_annotations["color"][:-1]},
    frame_props={'edgecolor': data_dict_annotations["color"][:-1]},
    check_props={'facecolor': data_dict_annotations["color"][:-1]},
)
def callback(label):
    pn = plots_by_label[label]
    pn.set_visible(not pn.get_visible())
    pn.figure.canvas.draw_idle()
    ax.legend()
check.on_clicked(callback)

plt.show()