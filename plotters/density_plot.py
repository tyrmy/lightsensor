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
import config

def density2d(span, search):
    conn = db.connect('../sensordata.db')
    c = conn.cursor()
    plt.figure(figsize=(8,8), constrained_layout=False, tight_layout=True)
    input_date = tools.generate_days(span)
    
    y = []
    x = []

    for i in range(1,len(input_date)+1):
        results = c.execute('SELECT {target}, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=input_date[i-1], target=search)).fetchall()

        idx = 0
        for row in results:
            y.append(row[0]) 
            x.append(idx)
            idx += 1

    y = tools.translate(y, -0.05)
    plt.suptitle('{}-day 2D-density plot'.format(span), fontsize=16)
    plt.hist2d(x,y,bins=90,norm=mcolors.PowerNorm(0.1))
    plt.show()

    if (config.picture):
        plt.savefig('{}_{}-day_density.png'.format(datetime.datetime.today(),span), dpi=100, frameon=True)

    conn.close()

if __name__ == '__main__':
    tools.print_stats(config.database_location)
    #density2d(20, 'ldr')
    density2d(config.density_span, 'ldr')
