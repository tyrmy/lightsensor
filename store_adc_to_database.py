"""
Created on 12 Apr, 2020

@author Lassi Lehtinen
Device-end script used to store values from ADS1115 to sqlite database.

ADS1115 is to be connected via SPI communication to Raspberry Pi for script to function properly.
"""
import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from sql.sqlite import sqlite_object as SQL

if __name__ == '__main__':
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)

    ldr = AnalogIn(ads, ADS.P0)
    sunpanel = AnalogIn(ads, ADS.P1)
    ads.gain = 1

    # chan = AnalogIn(ads, ADS.P0, ADS.P1)

    sql = SQL()
    sql.create_connection("sensordata.db")
    sql.write_to_database('''INSERT INTO sensor_readings (ldr, sunpanel, text_datetime)
    VALUES({LDR}, {SUN}, datetime('now','localtime'));
    '''.format(LDR=ldr.value, SUN=sunpanel.value))

    sql.close_connection()
