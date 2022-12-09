import calendar


def find_last_day_of_month(year: int, month: int) -> int:
    """Finds the last day of a given month

    Args:
        year (int): Year of the month in question
        month (int): Number of the month in question (1 - 12)

    Returns:
        int: Last day of the month
    """
    monthrange = calendar.monthrange(year, month)
    return monthrange[1]
