"""
chapter10/pico/pico_adc/ldr_calibrate_pico.py

Using a Pico & MicroPython to measure maximum and minimum voltages using ADC

$ mpremote mount . run ldr_calibrate_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from machine import ADC
from time import sleep, sleep_ms

# ADC Channel	GPIO
# -----------   ----
# 0	            26
# 1	            27
# 2	            28
ADC_CHANNEL = 0

adc = ADC(ADC_CHANNEL)

# Number of voltage readings to sample
SAMPLES = 100

# Write results to this file
OUTPUT_FILE = "ldr_calibration_config_pico.py"

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
        reading = adc.read_u16()
        volts = 3.3 * (reading / 65535)

        volts_sum += volts
        sleep_ms(10)

    return volts_sum / samples


def main():
    """
    Program entry point.
    """

    output  = "# This file was automatically created by ldr_calibrate_pico.py\n"
    output += "# Number of samples: " + str(SAMPLES) + "\n"

    # Average minimum and maximum voltages
    min_volts = 0
    max_volts = 0

    print("Place LDR in the light. Starting measurement in 4 seconds...")
    sleep(4)
    print("Please wait...\n")
    max_volts = sample(SAMPLES)

    print("Place LDR in the dark. Starting measurement in 4 seconds...")
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