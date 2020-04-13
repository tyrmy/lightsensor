"""
Created on 10 Apr, 2020

@author Lassi Lehtinen

Script generates a plot of last 12 days when run seperately including todays measurements
"""
import sqlite3 as db
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import datetime

from tools import convert_datetimes
from tools import generate_days

import numpy as np
from math import ceil

conn = db.connect('../sensordata.db')
c = conn.cursor()

input_date = generate_days(12)
#fig, ax = plt.subplots()
#print(input_date[0].isoformat())
total_points = c.execute('SELECT COUNT(*) FROM sensor_readings').fetchone()[0]
distinct_dates_amount = len(c.execute('SELECT DISTINCT DATE(text_datetime) FROM sensor_readings').fetchall())
distinct_dates = c.execute('SELECT DISTINCT DATE(text_datetime) FROM sensor_readings').fetchall()

print("Total datapoints: {}".format(total_points))
print("Data collected on span of {} days.".format(distinct_dates_amount))
#for date in distinct_dates:
#    print(date[0])

plt.figure(figsize=(12,7), constrained_layout=False, tight_layout=True)
for i in range(1,len(input_date)+1):
    results = c.execute('SELECT ldr, sunpanel, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=input_date[i-1])).fetchall()

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

    plt.subplot(3,4,i)
    plt.title(input_date[i-1], fontsize=9)
    plt.plot(datetime_objects, ldr, label='LDR', linewidth=1)
    plt.plot(datetime_objects, sunpanel, label='SP')
    ax = plt.gca()
    ax.text(0.05, 0.95, total_ldr, verticalalignment='top', horizontalalignment='left', transform=ax.transAxes, color='blue', fontsize=8)
    ax.text(0.5, 0.01, len(datetimes), verticalalignment='bottom', horizontalalignment='center', transform=ax.transAxes, color='black', fontsize=10)
    ax.text(0.95, 0.95, total_sp, verticalalignment='top', horizontalalignment='right', transform=ax.transAxes, color='orange', fontsize=8)
    #ax.axes.xaxis.set_visible(False)
    ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
    ax.axes.yaxis.set_visible(False)
    ax.grid(True)

    plt.gcf().autofmt_xdate()
    #plt.legend()

plt.suptitle('12-day summary', fontsize=16)
plt.show()
conn.close()
