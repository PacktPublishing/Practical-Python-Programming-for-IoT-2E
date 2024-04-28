"""
chapter13/rpi/version4_asyncio_rpi/main.py

Asynchronous IO example with Raspberry Pi & Python.

Dependencies:
  pip3 install pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import adafruit_ads1x15.ads1115 as ADS
import pigpio
from time import sleep
import asyncio
import logging
import sys

# Our custom classes
from Button import Button
from Pot import Pot
from LED import LED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

pi = pigpio.pi()

# GPIOs
BUTTON_GPIO = 16
LED1_GPIO = 20
LED2_GPIO = 21
POT_ADC_CHANNEL = ADS.P0 # P0 maps to output A1 on ADS1115

# Potentiometer / ADC settings (for Pot Class)
MIN_BLINK_RATE_SECS = 0.1 # Minimum value returnable by Pot class
MAX_BLINK_RATE_SECS = 5   # Maximum value returnable by Pot class


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


# Create BUTTON class instances and register button_handler() callback with it.
button = Button(gpio=BUTTON_GPIO,
               hold_secs=0.5,
               pi=pi,
               callback=button_handler)


def pot_handler(the_pot, value):
    """ Handles potentiometer event
        Parameters:
          'the_pot' is a reference to the Pot instance that invoked the callback (ie the pot variable created below)
          'value' is the mapped value (ie in the range MIN_BLINK_RATE_SECS..MAX_BLINK_RATE_SECS) """

    logger.debug(the_pot)
    logger.info("Changing LED #{} rate to {}".format(led_index, value))
    LEDS[led_index].set_rate(value)


# Create POT class instances and register pot_handler() callback with it.
pot = Pot(analog_channel=POT_ADC_CHANNEL,
         min_value=MIN_BLINK_RATE_SECS,
         max_value=MAX_BLINK_RATE_SECS,
         callback=pot_handler)



# Create LED class instances.
LEDS = [
    LED(gpio=LED1_GPIO, pi=pi),
    LED(gpio=LED2_GPIO, pi=pi)
]


# The index of the LED in LEDS List which will be affected when the potentiometer value changes.
# 'led_index' is updated in button_handler() and referenced in pot_handler()
led_index = 0


async def main():                                                        # (1)
    """
    Setup and register asyncio tasks.
    """

    tasks = []

    # Register the LEDs
    for led in LEDS:                                                     # (2)
        tasks.append(
            asyncio.create_task(
                led.run()
            ))

    # Register Potentiometer
    tasks.append(                                                        # (3)
          asyncio.create_task(
              pot.run()
          ))

    # Register Button
    tasks.append(                                                        # (4)
        asyncio.create_task(
            button.run()
        ))

    await asyncio.gather(*tasks)  # *tasks unpacks list into args for .gather()


if __name__ == "__main__":

    assert sys.version_info >= (3, 7), "Python 3.7+ Required"

    try:
        logger.info("Version 4 - Raspberry Pi & Python - Asynchronous IO Example. Press Control + C To Exit.")

        # Initialise all LEDs
        rate = pot.get_value()
        LED.set_rate_all(rate)  # Initialise all LEDS based on Pot value.
        logger.info("Setting rate for all LEDs to {}".format(rate))

        logger.info("Turning the Potentiometer dial will change the rate for LED #{}".format(led_index))

        ## Asynchronous IO (Python 3.7+)
        asyncio.run(main())                                                # (5)

    except KeyboardInterrupt:
        LED.set_rate_all(0) # Turn all LEDs off.
        pi.stop()
