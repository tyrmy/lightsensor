import sqlite3 as db
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import datetime

import numpy as np
from math import ceil

def convert_datetimes(datetimes):
    datetime_objects = []
    for datetime_str in datetimes:
        datetime_objects.append(datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S'))
    return datetime_objects

def generate_days(num):
    a = datetime.date.today()
    dates = []
    for x in range (0, num):
        dates.append(a - datetime.timedelta(days = x))
    dates.sort()
    return dates

def print_last_full_day():
    conn = db.connect('sensordata.db')
    c = conn.cursor()

    a = datetime.date.today()
    a = a - datetime.timedelta(days = 1)

    results = c.execute('SELECT ldr, sunpanel, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=a)).fetchall()
    plt.figure(figsize=(7,7), constrained_layout=False)

    ldr = []
    sunpanel = []
    datetimes = []
    for row in results:
       ldr.append(row[0]) 
       sunpanel.append(row[1]) 
       datetimes.append(row[2]) 

    max_value = 0
    scale_value = 1.7

    for j in ldr:
        if j > max_value:
            max_value = j

    ldr[:] = [(max_value-x)*scale_value for x in ldr]
    total_ldr = ceil(np.trapz(ldr))
    total_sp = ceil(np.trapz(sunpanel))
    datetime_objects = convert_datetimes(datetimes)

    plt.title(a)
    plt.plot(datetime_objects, ldr, label='LDR')
    plt.plot(datetime_objects, sunpanel, label='SP')

    ax = plt.gca()
    plt.gcf().autofmt_xdate()
    #ax.xaxis.set_major_locator(hours)
    ax.xaxis.set_major_locator(dates.HourLocator())
    ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    ax.xaxis.set_minor_locator(dates.MinuteLocator(interval=15))

    ax.text(0.05, 0.99, total_ldr, verticalalignment='top', horizontalalignment='left', transform=ax.transAxes, color='blue', fontsize=12)
    ax.text(0.5, 0.99, len(datetimes), verticalalignment='top', horizontalalignment='center', transform=ax.transAxes, color='black', fontsize=14)
    ax.text(0.95, 0.99, total_sp, verticalalignment='top', horizontalalignment='right', transform=ax.transAxes, color='orange', fontsize=12)
    ax.grid(True)

    plt.show()
    conn.close()

print_last_full_day()
exit()
