import datetime
import calendar


def year_and_month_from_string(back_until_string):
    start_month, start_year = back_until_string.split('-')
    start_month = int(start_month)
    start_year = int(start_year)
    return start_year, start_month

def current_month_year_string():
    now = datetime.datetime.now()
    return f"{now.month}-{now.year}"

def two_digit_str(integer):
    s = str(integer)

    if len(s) == 1:
        s = '0' + s

    return s

def ymd_date_string(date):
    return f"{date.year}-{date.month}-{date.day}"

def last_day_of_month(year_and_month):
    year, month = year_and_month
    return calendar.monthrange(year, month)[1]
