"""
Created on 15 Apr, 2020

@author Lassi Lehtinen

Generates a 2d density plot
"""

import sqlite3 as db
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

import datetime
import tools

database_location = '../sensordata.db'

def get_values():
    pass

def density2d(span, search):
    conn = db.connect('../sensordata.db')
    c = conn.cursor()
    plt.figure(figsize=(8,8), constrained_layout=False, tight_layout=True)
    input_date = tools.generate_days_from(span,2020,4,14)
    
    y = []
    x = []

    for i in range(1,len(input_date)+1):
        results = c.execute('SELECT {target}, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=input_date[i-1], target=search)).fetchall()

        idx = 0
        for row in results:
            y.append(row[0]) 
            x.append(idx)
            idx += 1

    y = tools.translate(y, 0.05)
    #plt.scatter(x, y, s=10, alpha=0.4, c='b')
    plt.suptitle('{}-day 2D-density plot'.format(span), fontsize=16)
    plt.hist2d(x,y,bins=60,norm=mcolors.PowerNorm(0.1))
    plt.show()

if __name__ == '__main__':
    tools.print_stats(database_location)
    #density2d(20, 'ldr')
    density2d(20, 'sunpanel')
