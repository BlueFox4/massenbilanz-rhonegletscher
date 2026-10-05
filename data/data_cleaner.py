# Source - https://stackoverflow.com/q/1877999
# Posted by torger, modified by community. See post 'Timeline' for change history
# Retrieved 2026-10-05, License - CC BY-SA 4.0

for year in range(1955, 2024):
    for month in range(1, 13):
        if month < 10:
            display_month = "0" + str(month)
        else:
            display_month = str(month)

        try:
            file = open("data/rhonegletscher_" + str(year) + "_" + display_month + ".csv", "r")
        except IOError:
            print("Failed to read file.")
            continue

        lines = file.readlines()
        file.close()

        file.write("Y, M, D, T, TM, Tm, SLP, H, PP, VV, V, VM, VG, RA, SN, TS, FG\n")

        lines = lines[1:-2]  # Skip the header line

        for i, line in enumerate(lines):
            if i < 10:
                line = line[2:]
            else:
                line = line[3:]

            line = str(year) + "," + str(month) + "," + line
            file.write(line)

        file.close()