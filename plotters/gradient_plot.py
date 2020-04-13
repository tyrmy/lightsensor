"""
Created on 13 Apr, 2020

@author Lassi Lehtinen

Generates a summary plot of one database value over multiple days in a gradient color scheme
"""
import sqlite3 as db
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import datetime

from tools import convert_datetimes
from tools import generate_days
from tools import print_stats
import tools

import numpy as np
from math import ceil

scale_value = 1.7
database_location = '../sensordata.db'

def print_gradient(span, search):
    """
    Create a gradient plot of one value
    """
    conn = db.connect('../sensordata.db')
    c = conn.cursor()
    plt.figure(figsize=(10,7), constrained_layout=False, tight_layout=True)
    input_date = generate_days(span)

    for i in range(1,len(input_date)+1):
        results = c.execute('SELECT {target}, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=input_date[i-1], target=search)).fetchall()

        y_values = []
        datetimes = []

        for row in results:
            y_values.append(row[0]) 
            datetimes.append(row[1]) 

        datetime_objects = tools.extract_times(datetimes)
        max_value = max(y_values)
        y_values[:] = [(max_value-x)*1.7 for x in y_values]

        clr = i/(len(input_date)+1)
        plt.plot(datetime_objects, y_values, linewidth=2, alpha=0.5, color=(1,clr,0))
        plt.gcf().autofmt_xdate()

        ax = plt.gca()
        ax.xaxis.set_major_locator(dates.HourLocator(interval=3))
        ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        #ax.axes.yaxis.set_visible(False)
        ax.grid(True)

    plt.suptitle('{}-day gradient'.format(span), fontsize=16)
    plt.show()
    #plt.savefig('{}_{}-day_gradient.png'.format(datetime.datetime.today(),span), dpi=100, frameon=True)
    conn.close()

if __name__ == '__main__':
    print_stats(database_location)
    print_gradient(7,'ldr')
