"""
Created on 12 Apr, 2020

@author Lassi Lehtinen

A plotter class which can generate different plots
"""

import sqlite3 as db
import matplotlib.dates as dates
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import datetime

from sql.sqlite import sqlite_object as SQL

import tools
import config

import numpy as np
from math import ceil

class plotter:
    def __init__(self):
        """
        Constructs a new plotter
        """
        self.sql_obj = SQL(config.database_location)
        self.print_stats()

    def print_stats(self):
        """
        Prints sql database stats.
        """
        total_points = self.sql_obj.count_values('sensor_readings')
        distinct_dates_amount = len(self.sql_obj.return_quary(('SELECT DISTINCT DATE(text_datetime) FROM sensor_readings')))
        #distinct_dates = self.sql_obj.return_quary(('SELECT DISTINCT DATE(text_datetime) FROM sensor_readings'))

        print("Total datapoints: {}".format(total_points))
        print("Data collected on span of {} days.".format(distinct_dates_amount))

    def close(self):
        """
        Closes the sql interface connection
        """
        self.sql_obj.close_connection()


    def density2d(self, span, search, bamount):
        """
        Plots a density function
        """
        plt.figure(figsize=(9,5), constrained_layout=False)
        input_date = tools.generate_days(span)
        
        y = []
        x = []

        for i in range(1,len(input_date)+1):
            results = self.sql_obj.return_quary('SELECT {target}, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=input_date[i-1], target=search))

            idx = 0
            for row in results:
                y.append(row[0]) 
                x.append(idx)
                idx += 1

        y = tools.translate(y, -0.05)
        plt.suptitle('{}-day 2D-density plot'.format(span), fontsize=16)
        plt.hist2d(x,y,bins=bamount,norm=mcolors.PowerNorm(0.1))
        if (config.picture):
            plt.savefig('{}_{}-day_density.png'.format(datetime.datetime.today(),span), dpi=100, frameon=True)
        plt.show()

    def summary_plot(self,x,y,days):
        """
        Create a image file consisting of x times y plots on a specified span of days.
        """
        plt.figure(figsize=(6,9), constrained_layout=False, tight_layout=True)
        input_date = tools.generate_days(days)

        for i in range(1,len(input_date)+1):
            results = self.sql_obj.return_quary('SELECT ldr, sunpanel, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=input_date[i-1]))

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
        if (config.picture):
            plt.savefig('{}_{}-day_sum.png'.format(datetime.datetime.today(),days), dpi=100, frameon=True)
        plt.show()


    def gradient(self, span, search):
        """
        Create a gradient plot of one value
        """
        plt.figure(figsize=(10,7), constrained_layout=False, tight_layout=True)
        input_date = tools.generate_days(span)

        for i in range(1,len(input_date)+1):
            results = self.sql_obj.return_quary('SELECT {target}, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=input_date[i-1], target=search))

            y_values = []
            datetimes = []

            for row in results:
                y_values.append(row[0]) 
                datetimes.append(row[1]) 

            datetime_objects = tools.extract_times(datetimes)
            y_values = tools.translate(y_values, -0.05)

            plt.scatter(datetime_objects, y_values, s=25, alpha=0.3, c='b')
            plt.gcf().autofmt_xdate()

        ax = plt.gca()
        ax.xaxis.set_major_locator(dates.HourLocator(interval=3))
        ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        #ax.axes.yaxis.set_visible(False)
        ax.grid(True)

        plt.xlim(left=datetime.date.today(), right=datetime.date.today() + datetime.timedelta(days=1))
        plt.suptitle('{}-day gradient'.format(span), fontsize=16)
        if (config.picture):
            plt.savefig('{}_{}-day_gradient.png'.format(datetime.datetime.today(),span), dpi=100, frameon=True)
        plt.show()


    def yesterday(self):
        """
        Prints a figure of last fully measured day
        """
        a = tools.yesterday()

        results = self.sql_obj.return_quary('SELECT ldr, sunpanel, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=a))
        plt.figure(figsize=(12,8), constrained_layout=False, tight_layout=True)

        ldr = []
        sunpanel = []
        datetimes = []
        for row in results:
           ldr.append(row[0]) 
           sunpanel.append(row[1]) 
           datetimes.append(row[2]) 

        ldr = tools.translate(ldr, -1.7)
        # Integrate the area under curves
        total_ldr = ceil(np.trapz(ldr))
        total_sp = ceil(np.trapz(sunpanel))
        datetime_objects = tools.convert_datetimes(datetimes)

        plt.title(a)
        plt.plot(datetime_objects, ldr, label='LDR')
        plt.plot(datetime_objects, sunpanel, label='SP')

        ax = plt.gca()
        plt.gcf().autofmt_xdate()
        ax.xaxis.set_major_locator(dates.HourLocator())
        ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        ax.xaxis.set_minor_locator(dates.MinuteLocator(interval=15))

        ax.text(0.05, 0.99, total_ldr, verticalalignment='top', horizontalalignment='left', transform=ax.transAxes, color='blue', fontsize=12)
        ax.text(0.5, 0.99, len(ldr), verticalalignment='top', horizontalalignment='center', transform=ax.transAxes, color='black', fontsize=14)
        ax.text(0.95, 0.99, total_sp, verticalalignment='top', horizontalalignment='right', transform=ax.transAxes, color='orange', fontsize=12)
        ax.grid(True)

        if (config.picture):
            plt.savefig('{}_day_sum.png'.format(datetime.datetime.today()), dpi=150, frameon=True)
        plt.show()

if __name__ == '__main__':
    print('plotter: demonstration')
    pl = plotter()
    print('plotter: one day plot')
    pl.yesterday()
    print('plotter: summary plot')
    pl.summary_plot(config.x, config.y, config.total)
    print('plotter: gradient plot')
    pl.gradient(config.gradient_span, config.target)
    print('plotter: 2D density plot')
    pl.density2d(config.density_span, config.target, config.resolution2d)

    pl.close()
