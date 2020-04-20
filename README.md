# ADS1115 and Matplotlib demonstration

The python application uses ads1115 chip to capture samples to a database and plot the results. If you're using a Raspberry Pi with a graphical user interface the script works without any tinkering needed. If you're running headless than for example scp can be used to retrieve .db file from Pi.

An example database is provided for demo.

## Notes

* Running _python3 plotters.py_runs a test script with the example database
* The database has to be constructed by user. See _init\_database.py_
* Plotting is more for demonstration it is hard to implement elsewhere outside this project

---

## Example plots

![plot](/images/figure_2.png)

---

![plot](/images/figure_3.png)

---

![plot](/images/figure_4.png)

---

![plot](/images/figure_5.png)

---

![plot](/images/figure_6.png)
