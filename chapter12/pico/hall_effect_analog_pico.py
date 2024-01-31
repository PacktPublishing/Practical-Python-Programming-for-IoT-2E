"""
chapter12/pico/hall_effect_analog_pico.py

Using a Pico & MicroPython with a Ratiometric Type AH3505 Hall-Effect Sensor.

$ mpremote mount . run hall_effect_analog_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from time import sleep
import pigpio

# Below imports are part of Circuit Python and Blinka
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
            output = "Volts={:>5.1f}, Delta Volts={:>5.1f}".format(volts, volts_delta)
            print(output)
            sleep(0.05)

    except KeyboardInterrupt:
        i2c.deinit()                                                          
        pi.stop()
