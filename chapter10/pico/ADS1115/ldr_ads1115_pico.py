"""
File: chapter10/pico/ldr_ads1115_pico.py

Using a Pico & MicroPython to read an LDR  using an ADS1115 ADC

$ mpremote mount . run ldr_ads1115_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from machine import Pin, I2C
from time import sleep_ms
from ADS1115_pico import ADS1115
import ldr_calibration_config_ads1115_pico as calibration                     # (1)

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

# LED is connected to this GPIO Pin
LED_GPIO = 21

# Configure LED Pin and start with LED Off
led = Pin(LED_GPIO, mode=Pin.OUT, value=0)

# Voltage readings from ASC when
# LDR is in the Dark and in the Light
LIGHT_VOLTS = calibration.MAX_VOLTS                                   # (2)
DARK_VOLTS = calibration.MIN_VOLTS

# Votage reading (and buffer) where we set
# global variable triggered = True or False
TRIGGER_VOLTS = LIGHT_VOLTS - ((LIGHT_VOLTS - DARK_VOLTS) / 2)        # (3)
TRIGGER_BUFFER = 0.25                                                 # (4)

# "triggered" is set to True or False as the voltage
# read by the ADC passes over it's
# TRIGGER_VOLTS (+/- TRIGGER_BUFFER) thresholds.
triggered = False                                                     # (5)

def update_trigger(volts):
    """
    Compare the volts parameter to trigger conditions
    TRIGGER_VOLTS +/- TRIGGER_BUFFER and update
    the global 'triggered' variable as appropiate.
    """
    global triggered

    if triggered and volts > TRIGGER_VOLTS + TRIGGER_BUFFER:
        triggered = False
    elif not triggered and volts < TRIGGER_VOLTS - TRIGGER_BUFFER:
        triggered = True


def main():
    """
    Program Entry Point.
    """

    trigger_text = f"{TRIGGER_VOLTS:0.4f} +/- {TRIGGER_BUFFER}"

    try:
        while True:                                                   # (6)
            # Read voltage from ADC
            reading = adc.read(ADC_CHANNEL)
            
            update_trigger(reading.volts)

            output = f"LDR Reading volts={reading.volts:>5.3f}, trigger at {trigger_text}, triggered={triggered}"
            print(output)

            # Switch LED on or off based on trigger.
            led.value(triggered)                                      # (7)
            sleep_ms(50)

    except KeyboardInterrupt:        
        print("Switching LED Off")
        led.off()

main()