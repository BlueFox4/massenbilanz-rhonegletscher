
# file = open("data/data_all.csv", "r")
# lines = file.readlines()
# lines.pop(0)
# anzahlKeineNiederschlagsdaten=0
# anzahlKeineTemperaturdaten=0
# for i in range(len(lines)):
#     lines[i]=lines[i][:-1].split(",")
#     # print(lines[i])
#     try:
#         float(lines[i][8])
#     except:
#         anzahlKeineNiederschlagsdaten+=1
#     try:
#         float(lines[i][3])
#     except:
#         anzahlKeineTemperaturdaten+=1

# ZEITRAUM = [1999, 2023]
# anzahlKeineNiederschlagsdatenImZeitraum=0
# anzahlKeineTemperaturdatenImZeitraum=0
# anzahlDatenImZeitraum=0
# for i in range(len(lines)):
#     # print(lines[i][0])
#     if int(lines[i][0]) < ZEITRAUM[0] or int(lines[i][0]) > ZEITRAUM[1]:
#         continue
#     anzahlDatenImZeitraum += 1
#     try:
#         float(lines[i][8])
#     except:
#         anzahlKeineNiederschlagsdatenImZeitraum+=1
#     try:
#         float(lines[i][3])
#     except:
#         anzahlKeineTemperaturdatenImZeitraum+=1


# print(f"{anzahlKeineNiederschlagsdaten / len(lines) *100}% der täglichen Niederschlagsdaten fehlen.")
# print(f"{anzahlKeineTemperaturdaten / len(lines)*100}% der täglichen Temperaturdaten fehlen.")
# print(f"{anzahlKeineNiederschlagsdatenImZeitraum / anzahlDatenImZeitraum*100}% der täglichen Niederschlagsdaten im Zeitraum von {ZEITRAUM[0]} bis {ZEITRAUM[1]} fehlen.")
# print(f"{anzahlKeineTemperaturdatenImZeitraum / anzahlDatenImZeitraum*100}% der täglichen Temperaturdaten im Zeitraum von {ZEITRAUM[0]} bis {ZEITRAUM[1]}  fehlen.")

file = open("data/data_all.csv", "r")
lines = file.readlines()
lines.pop(0)

BETRACHTETES_JAHR = 2000

tagesdaten = []
for i in range(len(lines)):
    lines[i] = lines[i][:-1].split(",")
    