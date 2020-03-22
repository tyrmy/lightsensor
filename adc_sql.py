import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

from sql.sqlite import sqlite_object as SQL

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
ldr = AnalogIn(ads, ADS.P0)
sunpanel = AnalogIn(ads, ADS.P1)
ads.gain = 1

# Create differential input between channel 0 and 1
# chan = AnalogIn(ads, ADS.P0, ADS.P1)

sql = SQL()
sql.create_connection("sensordata.db")
sql.write_to_database('''INSERT INTO sensor_readings (ldr, sunpanel, text_datetime)
VALUES({LDR}, {SUN}, datetime('now','localtime'));
'''.format(LDR=ldr.value, SUN=sunpanel.value))
#sql.print_quary('SELECT * FROM sensor_readings;')
#print('{}\t{:>5.3f}\t'.format(ldr.value, ldr.voltage))
#print('{}\t{:>5.3f}'.format(sunpanel.value, sunpanel.voltage))
sql.close_connection()
