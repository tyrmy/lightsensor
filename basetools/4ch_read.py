import time, board, busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Create the ADC object using the I2C bus
ads = ADS.ADS1115(i2c)
# you can specify an I2C adress instead of the default 0x48
# ads = ADS.ADS1115(i2c, address=0x49)

# Create single-ended input on channel 0
ch0 = AnalogIn(ads, ADS.P0)
ch1 = AnalogIn(ads, ADS.P1)
ch2 = AnalogIn(ads, ADS.P2)
ch3 = AnalogIn(ads, ADS.P3)
#ch2 = AnalogIn(ads, ADS.P2)
#ch3 = AnalogIn(ads, ADS.P3)
ads.gain = 1

print("{:>5}\t{:>5}\t{:>5}\t{:>5}".format("ch0", "ch1", "ch2", "ch3"))

while True:
    try:
        print('{}\t{}\t'.format(ch0.value, ch1.value), end='')
        print('{}\t{}'.format(ch2.value, ch3.value))
        time.sleep(1)
    except KeyboardInterrupt:
        print("Closing...")
        exit()
