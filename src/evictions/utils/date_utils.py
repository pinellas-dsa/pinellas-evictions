import calendar


def find_last_day_of_month(year: int, month: int) -> int:
    monthrange = calendar.monthrange(year, month)
    return monthrange[1]
