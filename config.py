"""
@author Lassi Lehtinen

Manually set configurations here
"""

#change to access different database
database_location = './databases/sensordata.db'
linewidths = 2

#parameters for different plots
x = 2
y = 3
total = 6
gradient_span = 30
density_span = 30
resolution2d = 90
target = 'ldr'

# if True plotting starts from today
today = True
# else from date specified
year = 2020
month = 4
date = 20
span = 6

# If True plots will be saved as imagefiles
picture = False

# If True plots also a smooth curve of data
savgol = True
savgol_window = 41
savgol_degree = 4

def setToday(b):
    today = b
