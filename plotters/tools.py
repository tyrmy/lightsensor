"""
Created on 10 Apr, 2020

@Author Lassi Lehtinen
Utility functions
"""
import datetime
import sqlite3 as db

def print_stats(location):
    """
    Prints sql database stats.
    """
    conn = db.connect(location)
    c = conn.cursor()
    total_points = c.execute('SELECT COUNT(*) FROM sensor_readings').fetchone()[0]
    distinct_dates_amount = len(c.execute('SELECT DISTINCT DATE(text_datetime) FROM sensor_readings').fetchall())
    distinct_dates = c.execute('SELECT DISTINCT DATE(text_datetime) FROM sensor_readings').fetchall()
    conn.close()

    print("Total datapoints: {}".format(total_points))
    print("Data collected on span of {} days.".format(distinct_dates_amount))

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

def generate_days(num):
    """
    Generetes a list of days starting from current day counting down based on parameter :num:
    Returns a list of dates.
    """
    a = datetime.date.today()
    a = a - datetime.timedelta(days = 1)
    dates = []
    for x in range (0, num):
        dates.append(a - datetime.timedelta(days = x))
    dates.sort()
    return dates
