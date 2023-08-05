import datetime as dt

def third_tuesday_of_month(year, month):
  d = dt.datetime(year, month, 1)
  wd = d.weekday()
  # monday
  if wd == 0:
    return 16
  # tuesday
  if wd == 1:
    return 15
  # wensday
  if wd == 2:
    return 14
  # thursday
  if wd == 3:
    return 13
  # friday
  if wd == 4:
    return 12
  # saturday
  if wd == 5:
    return 11
  # sunday 6
  if wd == 6:
    return 17