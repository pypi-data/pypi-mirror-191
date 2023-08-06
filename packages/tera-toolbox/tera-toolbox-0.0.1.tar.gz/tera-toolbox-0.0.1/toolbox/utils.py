import datetime as dt


def inc_day(date, inc):
    """increment date by some amount of days"""
    return date + dt.timedelta(days=inc)
