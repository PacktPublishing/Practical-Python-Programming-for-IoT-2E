"""
chapter10/rpi/ldr_ads1115_rpi.py

Using a Raspberry Pi & Python to read LDR voltage using ADS115 ADC

Dependencies:
  # https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15
  pip3 install pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
from time import sleep
import pigpio
import ldr_calibration_config_rpi as calibration                           # (1)

# Below imports are part of Circuit Python ADS1115 Driver.
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

pi = pigpio.pi()

# LED is connected to this GPIO Pin
LED_GPIO = 21

# Configure LED pin and start with LED Off
pi.set_mode(LED_GPIO, pigpio.OUTPUT)
pi.write(LED_GPIO, pigpio.LOW)

# Voltage readings from ADS1115 when
# LDR is in the Dark and in the Light
LIGHT_VOLTS = calibration.MAX_VOLTS                                   # (2)
DARK_VOLTS = calibration.MIN_VOLTS

# Votage reading (and buffer) where we set
# global variable triggered = True or False
TRIGGER_VOLTS = LIGHT_VOLTS - ((LIGHT_VOLTS - DARK_VOLTS) / 2)        # (3)
TRIGGER_BUFFER = 0.25                                                 # (4)

# Create the I2C bus & ADS object.
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
analog_channel = AnalogIn(ads, ADS.P0)  #ADS.P0 --> A0

# "triggered" is set to True or False as the voltage
# read by the ADS1115 passes over it's
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


if __name__ == '__main__':

    trigger_text = f"{TRIGGER_VOLTS:0.4f} +/- {TRIGGER_BUFFER}"

    try:
        while True:                                                   # (6)
            # Read voltage from ADS1115 channel
            volts = analog_channel.voltage

            update_trigger(volts)

            output = f"LDR Reading volts={volts:>5.3f}, trigger at {trigger_text}, triggered={triggered}"
            print(output)

            # Switch LED on or off based on trigger.
            pi.write(LED_GPIO, triggered)                             # (7)
            sleep(0.05)

    except KeyboardInterrupt:
        i2c.deinit()
        print("Switching LED Off")
        pi.write(LED_GPIO, pigpio.LOW) # LED Off
        pi.stop() # PiGPIO Cleanup
