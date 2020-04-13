"""
Created on 12 Apr, 2020

@author Lassi Lehtinen

Script generates a custom plot and stores it as .png file
"""
import sqlite3 as db
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import datetime

from tools import convert_datetimes
from tools import generate_days
from tools import print_stats

import numpy as np
from math import ceil

scale_value = 1.7
database_location = '../sensordata.db'

def print_day_plot(x,y,days):
    """
    Create a image file consisting of x times y plots on a specified span of days.
    """
    conn = db.connect('../sensordata.db')
    c = conn.cursor()
    plt.figure(figsize=(11,19), constrained_layout=False, tight_layout=True)
    input_date = generate_days(days)

    for i in range(1,len(input_date)+1):
        results = c.execute('SELECT ldr, sunpanel, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=input_date[i-1])).fetchall()

        ldr = []
        sunpanel = []
        datetimes = []


        for row in results:
           ldr.append(row[0]) 
           sunpanel.append(row[1]) 
           datetimes.append(row[2]) 

        max_value = max(ldr)

        ldr[:] = [(max_value-x)*scale_value for x in ldr]
        total_ldr = ceil(np.trapz(ldr))
        total_sp = ceil(np.trapz(sunpanel))
        datetime_objects = convert_datetimes(datetimes)

        plt.subplot(y,x,i)
        plt.title(input_date[i-1], fontsize=10)
        plt.plot(datetime_objects, ldr, label='LDR', linewidth=1)
        plt.plot(datetime_objects, sunpanel, label='SP')

        ax = plt.gca()
        ax.text(0.05, 0.95, total_ldr, verticalalignment='top', horizontalalignment='left', transform=ax.transAxes, color='blue', fontsize=8)
        ax.text(0.5, 0.01, len(datetimes), verticalalignment='bottom', horizontalalignment='center', transform=ax.transAxes, color='black', fontsize=10)
        ax.text(0.95, 0.95, total_sp, verticalalignment='top', horizontalalignment='right', transform=ax.transAxes, color='orange', fontsize=8)
        #ax.axes.xaxis.set_visible(False)
        ax.xaxis.set_major_locator(dates.HourLocator(interval=3))
        ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        ax.axes.yaxis.set_visible(False)
        ax.grid(True)

        plt.gcf().autofmt_xdate()
        #plt.legend()

    plt.suptitle('{}-day summary'.format(days), fontsize=16)
    #plt.show()
    plt.savefig('{}_{}-day_sum.png'.format(datetime.datetime.today(),days), dpi=100, frameon=True)
    conn.close()

if __name__ == '__main__':
    print_stats(database_location)
    #print_day_plot(3,3,9)
    print_day_plot(2,11,22)
