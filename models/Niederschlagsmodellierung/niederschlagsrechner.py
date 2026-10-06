import visualisation.Jahresentwicklung as calc

# Needs to get t as a float where the whole number is the year, and the decimals are 1/366 of the day in the year
# since is simply the year since when the trend should be generated
def erhalteNiederschlagstageTrend(t, since):
    return calc.fit_pp_days_func(t, since)

# Needs to get t as a float where the whole number is the year, and the decimals are 1/366 of the day in the year
# since is simply a year since when the trend should be generated
def erhalteNiederschlagMonatlicherTrend(t, since):
    return calc.fit_monthly_pp_func(t, since)

if __name__ == "__main__":
    time=1996+(8*31/366)
    print("=======================\nZunächst wird sich der Trend der Niederschlagstage pro Jahr angesehen:\n")
    while time < 2101:
        print(f"{time}: Model since 1999 {round(erhalteNiederschlagstageTrend(time, 1996))} Tage | Model since 2014 {round(erhalteNiederschlagMonatlicherTrend(time, 2014))} Tage")
        time += 1
    
    time=1996+(8*31/366)
    print("\n\n=======================\nNun wird sich der monatliche Niederschlagsmengentrend angesehen:\n")
    while time < 2101:
        print(f"{time}: Model since 1999 {round(erhalteNiederschlagMonatlicherTrend(time, 1996))}mm | Model since 2014 {round(erhalteNiederschlagMonatlicherTrend(time, 2014))}mm")
        time += 1