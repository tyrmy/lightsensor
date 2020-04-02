# ADS1115 based lightsensor app

The app operates on Raspberry Pi and utilizes sqlite3, python, matplotlib and ads1115 ADC to gather and plot data. Sql interface uses my python-sqlite3 -interface.

Currently there are two plot scripts:

* one\_day\_plot.py
* 12\_day\_plot.py

The two device-end scripts do the following:

* ldr\_read.py
	* Displays continuos readings from the sensor

* adc\_sql.py
	* Reads the sensor values and stores them to a sqlite database

---

## Example plots

![plot](/images/figure_1.png)

---

![plot](/images/figure_2.png)

---

![plot](/images/figure_3.png)

---

![plot](/images/figure_4.png)
