"""
Created on 12 Apr, 2020

@author Lassi Lehtinen

Device-end script used to store values from ADS1115 to sqlite database.

ADS1115 is to be connected via i2c communication to Raspberry Pi for script to function properly.
"""
import board, busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from sql.sqlite import sqlite_object as SQL

def active_plot():
    pass

if __name__ == '__main__':
    active_plot()
