"""
chapter10/rpi/moisture_ads1115_calibrate_rpi.py

Using a Raspberry Pi & Python to measure maximum and minimum voltages using ADS115 ADC

Dependencies:
  # https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15
  pip3 install adafruit-circuitpython-ads1x15

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
from time import sleep

# Below imports are part of Circuit Python ADS1115 Driver.
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Create the I2C bus & ADS object.
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
analog_channel = AnalogIn(ads, ADS.P0)  #ADS.P0 --> A0


# Number of voltage readings to sample
SAMPLES = 100


# Write results to this file
OUTPUT_FILE = "moisture_calibration_config_rpi.py"


def sample(samples):
    """
    Read a number of voltage samples from ADS1115
    and return the average voltage
    """
    volts_sum = 0
    for c in range(SAMPLES):
        volts = analog_channel.voltage
        volts_sum += volts
        sleep(0.01)

    return volts_sum / samples


if __name__ == '__main__':
    output  = "# This file was automatically created by " + __file__ + "\n"
    output += "# Number of samples: " + str(SAMPLES) + "\n"

    # Average minimum and maximum voltages
    min_volts = 0
    max_volts = 0

    try:
        print("Dry probe. Starting measurement in 4 seconds...")
        sleep(4)
        print("Please wait...\n")
        min_volts = sample(SAMPLES)

        print("Wet probe. Starting measurement in 4 seconds...")
        sleep(4)
        print("Please wait...\n")
        max_volts = sample(SAMPLES)

        output += f"# Voltage range is {max_volts - min_volts:0.4f}\n"
        output += f"MIN_VOLTS = {min_volts:0.4f}\n"
        output += f"MAX_VOLTS = {max_volts:0.4f}\n"
        
        with open(OUTPUT_FILE, "w") as f:
            f.write(output)

        print("File " + OUTPUT_FILE + " created with:\n")
        print(output)

    except KeyboardInterrupt:
        i2c.deinit()
