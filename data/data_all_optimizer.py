from datetime import date
import numpy as np
import csv

DATA_ALL_PATH = "data/data_all.csv"

# =======
# READING
# =======

print("Parsing document... ", end="", flush=True)

# Get all data and parse it into one beautiful (gigantic) python list
with open(DATA_ALL_PATH, 'r') as f:
    data = f.readlines()

data_dict = {}
for title in data[0].split(","):
    data_dict[title.strip()] = []
data = data[1:]

for datum in data:
    datum = datum.split(",")
    for i, l in enumerate(data_dict.values()):
        try:
            l.append(float(datum[i].strip()))
        except ValueError:
            l.append(np.nan)

print("parsed document.")


# ==========
# Add column
# ==========

print("Optimizing Data... ", end="", flush=True)

if "t" not in data_dict.keys():
    # Days in a year as fractions of 1, added to the year in one column (e.g. 2.1.1955 -> )
    data_dict["t"] = []
    months = data_dict["M"]
    days = data_dict["D"]
    for i, y in enumerate(data_dict["Y"]):
        y = int(y)
        m = int(months[i])
        d = int(days[i])
        diff_since_jan_1 = (date(y, m, d) - date(y,1,1)).days
        time = y + (diff_since_jan_1 / 366)
        data_dict["t"].append(time)
    print("Done.")
else:
    print("Data has already been optimized. Skipping.")


# =============
# WRITE CHANGES
# =============

with open(DATA_ALL_PATH, "w") as f:
    csv_writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(data_dict.keys())

    for i in range(len(data_dict["Y"])):
        row = []
        for d in data_dict.values():
            row.append(d[i])
        csv_writer.writerow(row)
    