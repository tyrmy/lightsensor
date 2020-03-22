import sqlite3 as db
import matplotlib.pyplot as plt
import datetime

conn = db.connect('sensordata.db')
conn.row_factory = lambda cursor, row: row[0]
c = conn.cursor()
ldr = c.execute('SELECT ldr FROM sensor_readings').fetchall()
sunpanel = c.execute('SELECT sunpanel FROM sensor_readings').fetchall()
datetimes = c.execute('SELECT text_datetime FROM sensor_readings').fetchall()

datetime_objects = []

for datetime_str in datetimes:
    datetime_objects.append(datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S'))

#print(ids)
plt.plot(datetime_objects, ldr)
plt.plot(datetime_objects, sunpanel)

plt.gcf().autofmt_xdate()

plt.show()
