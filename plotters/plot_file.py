"""
Created on 12 Apr, 2020

@author Lassi Lehtinen

Script generates a custom plot and stores it as .png file
"""

import sqlite3 as db
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import datetime

import tools
import config

import numpy as np
from math import ceil

def print_day_plot(x,y,days):
    """
    Create a image file consisting of x times y plots on a specified span of days.
    """
    conn = db.connect('../sensordata.db')
    c = conn.cursor()
    plt.figure(figsize=(6,9), constrained_layout=False, tight_layout=True)
    input_date = tools.generate_days(days)

    for i in range(1,len(input_date)+1):
        results = c.execute('SELECT ldr, sunpanel, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=input_date[i-1])).fetchall()

        y1 = []
        y2 = []
        datetimes = []

        for row in results:
           y1.append(row[0]) 
           y2.append(row[1]) 
           datetimes.append(row[2]) 

        y1 = tools.translate(y1, -1.7)
        total_y1 = ceil(np.trapz(y1))
        total_y2 = ceil(np.trapz(y2))

        datetime_objects = tools.convert_datetimes(datetimes)

        plt.subplot(y,x,i)
        plt.title(input_date[i-1], fontsize=10)
        plt.plot(datetime_objects, y1, label='LDR', linewidth=1)
        plt.plot(datetime_objects, y2, label='SP')
        ax = plt.gca()
        ax.grid(True)
        ax.xaxis.set_major_locator(dates.HourLocator(interval=3))
        ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        ax.axes.yaxis.set_visible(False)
        ax.text(0.05, 0.95, total_y1, verticalalignment='top', horizontalalignment='left', transform=ax.transAxes, color='blue', fontsize=8)
        ax.text(0.5, 0.01, len(datetimes), verticalalignment='bottom', horizontalalignment='center', transform=ax.transAxes, color='black', fontsize=10)
        ax.text(0.95, 0.95, total_y2, verticalalignment='top', horizontalalignment='right', transform=ax.transAxes, color='orange', fontsize=8)
    #ax.axes.xaxis.set_visible(False)

    plt.gcf().autofmt_xdate()

    plt.suptitle('{}-day summary'.format(days), fontsize=16)
    plt.savefig('{}_{}-day_sum.png'.format(datetime.datetime.today(),days), dpi=100, frameon=True)
    conn.close()

if __name__ == '__main__':
    tools.print_stats(config.database_location)
    print_day_plot(config.y,config.x,config.total)
