from datetime import datetime, date, time

from dateutil.relativedelta import relativedelta


def get_edge_days_month(rel_month=-1):
    """get the first day of month and first of next month """

    today = date.today()
    midnight = time.min

    reldate = today + relativedelta(months=rel_month)

    last_day = reldate + relativedelta(day=1, months=+1)
    first_day = reldate + relativedelta(day=1)

    lastday = datetime.combine(last_day, midnight)
    firstday = datetime.combine(first_day, midnight)

    return firstday, lastday


def get_edge_days_week(rel_week=-1):
    """get first day of week and first day of nexy week"""

    today = date.today()
    midnight = time.min

    reldate = today + relativedelta(weeks=rel_week)

    last_day = reldate + relativedelta(weekday=0)
    first_day = reldate + relativedelta(weeks=-1, weekday=0)

    lastday = datetime.combine(last_day, midnight)
    firstday = datetime.combine(first_day, midnight)

    return firstday, lastday


def get_abs_month(abs_month, abs_year=None):
    """docstring for set_abs_month"""
    if not abs_year:
        abs_year = date.now().year

    midnight = time.min

    firstday = date(abs_year, abs_month)
    firstday = datetime.combine(firstday, midnight)

    lastday = date(abs_year, abs_month + 1)
    lastday = datetime.combine(lastday, midnight)

    return firstday, lastday
