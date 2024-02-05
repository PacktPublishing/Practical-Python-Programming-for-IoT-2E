"""
chapter10/pico/moisture_calibrate_ads1115_pico.py

Using a Pico & MicroPython to measure maximum and minimum voltages using an ADS1115 ADC

$ mpremote mount . run moisture_calibrate_ads1115_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from machine import Pin, I2C
from time import sleep, sleep_ms
from ADS1115_pico import ADS1115

# ADC Channel	ADS1115
# -----------   ----
# 0	            A0
# 1	            A1
# 2	            A2
# 3	            A3

ADC_CHANNEL = 0

# I2C Parameters
BUS_ID = 0
SCL_GPIO = 17
SDA_GPIO = 16

i2c = I2C(BUS_ID, scl=Pin(SCL_GPIO), sda=Pin(SDA_GPIO))
adc = ADS1115(i2c)

# Number of voltage readings to sample
SAMPLES = 100

# Write results to this file
OUTPUT_FILE = "moisture_calibration_config_ads1115_pico.py"

def sample(samples):
    """
    Read a number of samples from ADC
    and return the average voltage.
    """

    # Note - The Pico ADC returns a 12 bit reading in the range 
    # 0 - 65535 (4096 discrete units). This reading is then
    # converted to volts for consistency with the Raspberry Pi
    # ADS1115 ADC LDR example.

    volts_sum = 0

    for c in range(SAMPLES):
        reading = adc.read(ADC_CHANNEL)
        volts_sum += reading['volts']
        sleep_ms(10)

    return volts_sum / samples


def main():
    """
    Program entry point.
    """

    output  = "# This file was automatically created by moisture_calibrate_ads1115_pico.py\n"
    output += "# Number of samples: " + str(SAMPLES) + "\n"

    # Average minimum and maximum voltages
    min_volts = 0
    max_volts = 0

    print("Dry probe. Starting measurement in 4 seconds...")
    sleep(4)
    print("Please wait...\n")
    max_volts = sample(SAMPLES)

    print("Wet probe. Starting measurement in 4 seconds...")
    sleep(4)
    print("Please wait...\n")
    min_volts = sample(SAMPLES)

    output += f"# Voltage range is {max_volts - min_volts:0.4f}\n"
    output += f"MIN_VOLTS = {min_volts:0.4f}\n"
    output += f"MAX_VOLTS = {max_volts:0.4f}\n"

    with open(OUTPUT_FILE, "w") as f:
        f.write(output)

    print("File " + OUTPUT_FILE + " created with:\n")
    print(output)


main()
