import datetime
import time
from datetime import  timedelta

def days_from_today_to_next_birthday(today, birthday):
    today = today.split("/")
    birthday = birthday.split("/")
    today = datetime.date(year=int(today[0]), month=int(today[1]), day=int(today[2]))
    birthday = datetime.date(year=int(birthday[0]), month=int(birthday[1]), day=int(birthday[2]))
    if birthday.month < today.month:
        next_birthday = datetime.date(year=today.year+1, month=birthday.month, day=birthday.day)
    elif birthday.month == today.month:
        if birthday.day < today.day:
            next_birthday = datetime.date(year=today.year+1, month=birthday.month, day=birthday.day)
        else:
            next_birthday = datetime.date(year=today.year, month=birthday.month, day=birthday.day)
    else:
        next_birthday = datetime.date(year=today.year, month=birthday.month, day=birthday.day)
    days = (next_birthday - today).days
    return days, str(next_birthday)

def compute_planday(next_birthday, n):
    next_birthday = next_birthday.split("-")
    next_birthday = datetime.date(int(next_birthday[0]), int(next_birthday[1]), int(next_birthday[2]))
    planday = next_birthday - datetime.timedelta(days=n)
    isSaturday = True
    if planday.weekday() != 5:
        isSaturday = False
    return str(planday), isSaturday

def correct_planday(planday):
    planday = planday.split("-")
    planday = datetime.date(int(planday[0]), int(planday[1]), int(planday[2]))
    weekday_planday = planday.weekday()
    if weekday_planday > 5:
        corrected_planday = planday + timedelta(days=weekday_planday-5)
    else:
        if weekday_planday - 5 + 7 < 5 - weekday_planday:
            corrected_planday = planday - timedelta(days=weekday_planday-5+7)
        else:
            corrected_planday = planday + timedelta(days=5-weekday_planday)
    return str(corrected_planday)
