import sqlite3 as db
import matplotlib.pyplot as plt
import datetime

def convert_datetimes(datetimes):
    datetime_objects = []
    for datetime_str in datetimes:
        datetime_objects.append(datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S'))
    return datetime_objects

conn = db.connect('sensordata.db')
c = conn.cursor()

a = datetime.date.today()
numdays = 12
input_date = []
for x in range (0, numdays):
        input_date.append(a - datetime.timedelta(days = x))

input_date.sort()

for i in range(1,len(input_date)+1):
    results = c.execute('SELECT ldr, sunpanel, text_datetime FROM sensor_readings WHERE text_datetime LIKE \'{date}%\''.format(date=input_date[i-1])).fetchall()

    ldr = []
    sunpanel = []
    datetimes = []
    for row in results:
       ldr.append(row[0]) 
       sunpanel.append(row[1]) 
       datetimes.append(row[2]) 

    max_value = 0
    scale_value = 1.7

    for j in ldr:
        if j > max_value:
            max_value = j

    ldr[:] = [(max_value-x)*scale_value for x in ldr]
    datetime_objects = convert_datetimes(datetimes)

    plt.subplot(3,4,i)
    plt.title(input_date[i-1])
    plt.plot(datetime_objects, ldr, label='LDR')
    plt.plot(datetime_objects, sunpanel, label='SP')
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.grid(True)

    plt.gcf().autofmt_xdate()
    #plt.legend()

plt.show()
