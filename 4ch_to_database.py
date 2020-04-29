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
    ch2 = AnalogIn(ads, ADS.P2)
    ch3 = AnalogIn(ads, ADS.P3)
    ads.gain = 1

    command = '''
    INSERT INTO ads1115 (ch0, ch1, ch2, ch3, txt_date, txt_time)
    VALUES({}, {}, {}, {}, date('now','localtime'), time('now', 'localtime'));
    '''.format(ch0.value, ch1.value, ch2.value, ch3.value)

    sql = SQL()
    sql.create_connection('/home/pi//python/lightsensor/databases/sensordata.db')
    sql.write_to_database(command)
    sql.close_connection()

if __name__ == '__main__':
    store_values()
