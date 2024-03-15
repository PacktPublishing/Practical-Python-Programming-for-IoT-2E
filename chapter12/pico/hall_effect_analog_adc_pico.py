"""
chapter12/pico/hall_effect_analog_adc_pico.py

Using a Pico & MicroPython with a Ratiometric Type AH3505 Hall-Effect Sensor using ADC.

$ mpremote mount . run hall_effect_analog_adc_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from machine import ADC
from time import sleep_ms

# ADC Channel	GPIO
# -----------   ----
# 0	            26
# 1	            27
# 2	            28

ADC_CHANNEL = 0

adc = ADC(ADC_CHANNEL)

if __name__ == '__main__':
      
    # Sample a resting voltage to calculate delta voltage.
    print("Calibrating... make sure magnet is not near hall effect sensor")

    resting_volts = 0
    sum_volts = 0

    for n in range(0, 100):
        # Take 100 samples
        reading = adc.read_u16()
        volts = 3.3 * (reading / 65535)        
        sum_volts = sum_volts + volts

    resting_volts = sum_volts / 100

    while True:
        reading = adc.read_u16()
        volts = 3.3 * (reading / 65535)        
        volts_delta = volts - resting_volts

        # Analog input voltage will fluctuate a little. Using 1 decimal point
        # to steady display output.
        output = "Volts={:>5.2f}, Delta Volts={:>5.2f}".format(volts, volts_delta)
        print(output)
        sleep_ms(50)
