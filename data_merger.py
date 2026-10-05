try:
    data = open('master_data.csv', 'w')
    data.write("Y, M, D, T, TM, Tm, SLP, H, PP, VV, V, VM, VG, RA, SN, TS, FG\n")

    for year in range(1955, 2024):
        for month in range(1, 13):
            if month < 10:
                month = "0" + str(month)
            else:
                month = str(month)

            try:
                file = open("cleaned_data/rhonegletscher_" + str(year) + "_" + month + ".csv", "r")
            except IOError:
                print("Failed to read file.")
                continue

            lines = file.readlines()
            lines = lines[1:]  # Skip the header line
            file.close()

            data.writelines(lines)
    data.close()

except IOError:
    print("Failed to write to master_data.csv.")