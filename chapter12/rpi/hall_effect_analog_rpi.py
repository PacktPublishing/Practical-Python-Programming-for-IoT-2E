"""
chapter12/rpi/hall_effect_analog_rpi.py

Using a Raspberry & Python with a Ratiometric Type AH3505 Hall-Effect Sensor.

Dependencies:
  # https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15
  pip3 install pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
from time import sleep
import pigpio

# Below imports are part of Circuit Python ADS1115 Driver.
import board                                                      
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

pi = pigpio.pi()

# Create the I2C bus & ADS object.
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
analog_channel_A0 = AnalogIn(ads, ADS.P0)  # ADS.P0 --> A0 

if __name__ == '__main__':
      
    try:
        # Sample a resting voltage to calculate delta voltage.
        print("Calibrating... make sure magnet is not near hall effect sensor")

        resting_volts = 0
        sum_volts = 0

        for n in range(0, 100):
            # Take 100 samples
            sum_volts = sum_volts + analog_channel_A0.voltage

        resting_volts = sum_volts / 100

        while True:
            volts = analog_channel_A0.voltage
            volts_delta = volts - resting_volts

            # Analog input voltage will fluctuate a little. Using 1 decimal point
            # to steady display output.
            output = "Volts={:>5.2f}, Delta Volts={:>5.2f}".format(volts, volts_delta)
            print(output)
            sleep(0.05)

    except KeyboardInterrupt:
        i2c.deinit()                                                          
        pi.stop()
