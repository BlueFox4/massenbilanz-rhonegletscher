import visualisation.Jahresentwicklung as calc

# Needs to get t as a float where the whole number is the year, and the decimals are 1/366 of the day in the year
# since is simply a year since when the trend should be generated
def erhalteNiederschlagMonatlicherTrend(t, since):
    calc.fit_monthly_pp_func(t, since)

# Needs to get t as a float where the whole number is the year, and the decimals are 1/366 of the day in the year
# since is simply the year since when the trend should be generated
def erhalteNiederschlagNiederschlagstageTrend(t, since):
    return calc.fit_pp_days_func(t, since)