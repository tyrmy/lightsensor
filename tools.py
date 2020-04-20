"""
Created on 10 Apr, 2020

@author Lassi Lehtinen

Utility functions
"""

import datetime
import sqlite3 as db
import config

def translate(input_array, multiplier):
    """
    Translate datapoints by a multiplier value. It can also be negative.
    """
    result = []
    max_y = max(input_array)
    min_y = min(input_array)
    result[:] = [(old-min_y) for old in input_array]
    result[:] = [(max_y-old)*-multiplier for old in input_array]
    return result

def yesterday():
    """
    Return a datetime object representing yesterday
    """
    a = datetime.date.today()
    a = a - datetime.timedelta(days = 1)
    return a

def convert_datetimes(datetimes):
    """
    Takes a list of string formatted datetimes and returns a converted list of datetime objects.
    """
    datetime_objects = []
    for datetime_str in datetimes:
        datetime_objects.append(datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S'))
    return datetime_objects

def extract_times(datetimes):
    """
    Takes a list of string datetimes and packs all datetimes to a span of one day.
    Returns a list of datetime objects.
    """
    datetime_objects = []
    for datetime_str in datetimes:
        datetime_objects.append(datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').time()))
    return datetime_objects

def extract_time(datetime_str):
    """
    Takes a list of string datetimes and packs all datetimes to a span of one day.
    Returns a list of datetime objects.
    """
    datetime_object = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S').time())
    return datetime_object

def generate_days(num):
    """
    Generetes a list of days starting from current day counting down based on parameter :num:
    Returns a list of dates.
    """
    if (config.today):
        a = datetime.date.today()
        a = a - datetime.timedelta(days = 1)
        dates = []
        for x in range (0, num):
            dates.append(a - datetime.timedelta(days = x))
        dates.sort()
        return dates
    else:
        return generate_days_from(config.span, config.year, config.month, config.date)

def generate_days_from(num, year, month, date):
    """
    Generetes a list of days starting from specified date counting down based on parameter :num:
    Returns a list of dates.
    """
    a = datetime.date(year,month,date)
    a = a - datetime.timedelta(days = 1)
    dates = []
    for x in range (0, num):
        dates.append(a - datetime.timedelta(days = x))
    dates.sort()
    return dates
