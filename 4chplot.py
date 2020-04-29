import config
import pandas as pd
import sqlite3, os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

os.system('./get_database.sh')
conn = sqlite3.connect(config.database_location)
#df = pd.read_sql_query("select * from ads1115 order by id desc limit 100;", conn)
df = pd.read_sql_query("select * from ads1115;", conn)

""" Combine datetimes """
datetimes = pd.to_datetime(df['txt_date'] + ' ' + df['txt_time'])
df = df.drop(columns=['txt_date', 'txt_time'])
df['datetimes'] = datetimes

#print(df)
df.plot(x='datetimes', y=['ch0','ch1','ch2','ch3'], grid=True)

plt.show()
