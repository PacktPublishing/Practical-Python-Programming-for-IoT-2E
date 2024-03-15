"""
chapter12/pico/hall_effect_analog_ads1115_pico.py

Using a Pico & MicroPython with a Ratiometric Type AH3505 Hall-Effect Sensor using an ADS1115 ADC.

$ mpremote mount . run hall_effect_analog_ads1115_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from machine import Pin, I2C
from time import sleep_ms
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

if __name__ == '__main__':
      
    # Sample a resting voltage to calculate delta voltage.
    print("Calibrating... make sure magnet is not near hall effect sensor")

    resting_volts = 0
    sum_volts = 0

    for n in range(0, 100):
        # Take 100 samples
        reading = adc.read(ADC_CHANNEL)
        sum_volts = sum_volts + reading['volts']

    resting_volts = sum_volts / 100

    while True:
        reading = adc.read(ADC_CHANNEL)
        volts = reading['volts']
        volts_delta = volts - resting_volts

        # Analog input voltage will fluctuate a little. Using 1 decimal point
        # to steady display output.
        output = "Volts={:>5.2f}, Delta Volts={:>5.2f}".format(volts, volts_delta)
        print(output)
        sleep_ms(50)
