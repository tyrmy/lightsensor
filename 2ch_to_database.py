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

def store_values():
    """
    Writes ch0 and ch1 values from ADS1115 to database with timestamp
    """
    i2c = busio.I2C(board.SCL, board.SDA)
    ads = ADS.ADS1115(i2c)

    ch0 = AnalogIn(ads, ADS.P0)
    ch1 = AnalogIn(ads, ADS.P1)
    ads.gain = 1

    command = '''
    INSERT INTO sensor_readings (ldr, sunpanel, text_datetime)
    VALUES({LDR}, {SUN}, datetime('now','localtime'));
    '''.format(LDR=ch0.value, SUN=ch1.value)

    sql = SQL()
    sql.create_connection('./databases/sensordata.db')
    sql.write_to_database(command)
    sql.close_connection()

def store_all_channels():
    """
    Writes all channel values to database with timestamp
    """
    pass

if __name__ == '__main__':
    store_values()
