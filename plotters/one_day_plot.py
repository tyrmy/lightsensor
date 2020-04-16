"""
Created on 10 Apr, 2020

@author Lassi Lehtinen

Script generates a plot of last fully measured day when run seperately
"""

import sqlite3 as db
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import datetime

from tools import convert_datetimes
from tools import generate_days

import numpy as np
from math import ceil

def print_last_full_day():
    """
    Prints a figure of last fully measured day
    """
    conn = db.connect('../sensordata.db')
    c = conn.cursor()

    a = datetime.date.today()
    a = a - datetime.timedelta(days = 1)

    results = c.execute('SELECT ldr, sunpanel, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=a)).fetchall()
    plt.figure(figsize=(12,8), constrained_layout=False, tight_layout=True)

    ldr = []
    sunpanel = []
    datetimes = []
    for row in results:
       ldr.append(row[0]) 
       sunpanel.append(row[1]) 
       datetimes.append(row[2]) 

    max_value = max(ldr)
    scale_value = 1.7

    ldr[:] = [(max_value-x)*scale_value for x in ldr]
    total_ldr = ceil(np.trapz(ldr))
    total_sp = ceil(np.trapz(sunpanel))
    datetime_objects = convert_datetimes(datetimes)

    plt.title(a)
    plt.plot(datetime_objects, ldr, label='LDR')
    plt.plot(datetime_objects, sunpanel, label='SP')

    ax = plt.gca()
    plt.gcf().autofmt_xdate()
    ax.xaxis.set_major_locator(dates.HourLocator())
    ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    ax.xaxis.set_minor_locator(dates.MinuteLocator(interval=15))

    ax.text(0.05, 0.99, total_ldr, verticalalignment='top', horizontalalignment='left', transform=ax.transAxes, color='blue', fontsize=12)
    ax.text(0.5, 0.99, len(datetimes), verticalalignment='top', horizontalalignment='center', transform=ax.transAxes, color='black', fontsize=14)
    ax.text(0.95, 0.99, total_sp, verticalalignment='top', horizontalalignment='right', transform=ax.transAxes, color='orange', fontsize=12)
    ax.grid(True)

    #plt.show()
    plt.savefig('{}_day_sum.png'.format(datetime.datetime.today()), dpi=150, frameon=True)
    conn.close()

if __name__ == '__main__':
    print_last_full_day()
    exit()
