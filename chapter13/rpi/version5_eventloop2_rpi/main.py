"""
chapter12/rpi/version4_eventloop2_rpi/main.py

## WARNING # WARNING # WARNING # WARNING # WARNING # WARNING # WARNING # WARNING ##
###################################################################################
##### VERSION 5 IS NOT EXPECTED TO WORK. THE REASON IS DISCUSSED IN THE BOOK ######
###################################################################################
## WARNING # WARNING # WARNING # WARNING # WARNING # WARNING # WARNING # WARNING ##

Refactored Version 1 Event Loop example for Raspberry Pi & Python.

Dependencies:
  pip3 install pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import adafruit_ads1x15.ads1115 as ADS
import pigpio

from time import sleep
import logging
import sys

# Our custom classes
from Button import Button
from Pot import Pot
from LED import LED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

pi = pigpio.pi()

# Button GPIO
Button_GPIO = 16

def button_handler(the_button, state):
    """ Handles button event.
        Parameters:
          'the_button' is a reference to the Button instance that invoked the callback (ie the button variable created below)
          'state' is the button state, eg PRESSED, RELEASED, HOLD """

    global led_index

    if state == Button.PRESSED:
        led_index += 1

        if led_index >= len(LEDS):
            led_index = 0

        logger.info("Turning the Potentiometer dial will change the rate for LED #{}".format(led_index))

    if state == Button.HOLD:
        rate = pot.get_value()
        logger.info("Changing rate for all LEDs to {}".format(rate))
        LED.set_rate_all(rate)


# Create Button class instances and register button_handler() callback with it.
button = Button(gpio=Button_GPIO,
               pi=pi,
               callback=button_handler)



# Potentiometer / ADC settings (for Pot Class)
Pot_CHANNEL = ADS.P0      # P0 maps to output A1 on ADS1115
MIN_BLINK_RATE_SECS = 0.1 # Minimum value returnable by Pot class
MAX_BLINK_RATE_SECS = 5   # Maximum value returnable by Pot class


def pot_handler(the_pot, value):
    """ Handles potentiometer event
        Parameters:
          'the_pot' is a reference to the Pot instance that invoked the callback (ie the pot variable created below)
          'value' is the mapped value (ie in the range MIN_BLINK_RATE_SECS..MAX_BLINK_RATE_SECS) """

    logger.debug(the_pot)
    logger.info("Changing LED #{} rate to {}".format(led_index, value))
    LEDS[led_index].set_rate(value)


# Create Pot class instances and register pot_handler() callback with it.
pot = Pot(analog_channel=Pot_CHANNEL,
         min_value=MIN_BLINK_RATE_SECS,
         max_value=MAX_BLINK_RATE_SECS,
         callback=pot_handler)



# Create LED class instances.
LEDS = [
    LED(gpio=20, pi=pi),
    LED(gpio=21, pi=pi)
]


# The index of the LED in LEDS List which will be affected when the potentiometer value changes.
# 'led_index' is updated in button_handler() and referenced in pot_handler()
led_index = 0


if __name__ == "__main__":

    print("\n## WARNING # WARNING # WARNING # WARNING # WARNING # WARNING # WARNING # WARNING ##")
    print("###################################################################################")
    print("##### VERSION 5 IS NOT EXPECTED TO WORK. THE REASON IS DISCUSSED IN THE BOOK ######")
    print("###################################################################################")
    print("## WARNING # WARNING # WARNING # WARNING # WARNING # WARNING # WARNING # WARNING ##\n")

    try:
        logger.info("Version 5 Refactored Event-Loop Example. Press Control + C To Exit.")

        # Initialise all LEDs
        rate = pot.get_value()
        LED.set_rate_all(rate)  # Initialise all LEDS based on Pot value.
        logger.info("Setting rate for all LEDs to {}".format(rate))

        logger.info("Turning the Potentiometer dial will change the rate for LED #{}".format(led_index))

        while True:

            for led in LEDS:
                led.run()

            pot.run()
            button.run()

    except KeyboardInterrupt:
        LED.set_rate_all(0) # Turn all LEDs off.
        pi.stop()
