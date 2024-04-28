"""
chapter12/version4_asyncio_pico_asd1115/main.py

Asynchronous IO example with Pico & MicroPython.

$ mpremote mount . run main.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
import logging
import uasyncio as asyncio

# Our custom classes
from Pot import Pot
from Button import Button
from LED import LED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Main')

# GPIOs
LED1_GPIO = 20
LED2_GPIO = 21
BUTTON_GPIO = 16

# ADC Channel	GPIO
# -----------   ----
# 0	            26
# 1	            27
# 2	            28

POT_ADC_CHANNEL = 0

# Potentiometer / ADC settings (for POT Class)
MIN_BLINK_RATE_SECS = 0 # Minimum value returnable by POT class
MAX_BLINK_RATE_SECS = 5 # Maximum value returnable by POT class

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
button = Button(gpio=BUTTON_GPIO,
               hold_secs=0.5,
               callback=button_handler)


def pot_handler(the_pot, value):
    """ Handles potentiometer event
        Parameters:
          'the_pot' is a reference to the POT instance that invoked the callback (ie the pot variable created below)
          'value' is the mapped value (ie in the range MIN_BLINK_RATE_SECS..MAX_BLINK_RATE_SECS) """

    logger.info("Changing LED #{} rate to {}".format(led_index, value))
    LEDS[led_index].set_rate(value)


# Create POT class instances and register pot_handler() callback with it.
pot = Pot(analog_channel=POT_ADC_CHANNEL,
         min_value=MIN_BLINK_RATE_SECS,
         max_value=MAX_BLINK_RATE_SECS,
         callback=pot_handler)


# Create LED class instances.
LEDS = [
    LED(gpio=LED1_GPIO),
    LED(gpio=LED2_GPIO)
]

# The index of the LED in LEDS List which will be affected when the potentiometer value changes.
# 'led_index' is updated in button_handler() and referenced in pot_handler()
led_index = 0


async def setup():
    """ Setup asyncio tasks """

    tasks = []

    # Register the LEDs.
    for led in LEDS:
        tasks.append(
            asyncio.create_task(
                led.run()
            ))

    tasks.append(
          asyncio.create_task(
              pot.run()
          ))

    tasks.append(
        asyncio.create_task(
            button.run()
        ))

    await asyncio.gather(*tasks)  # *tasks unpacks list into args for .gather()


def main():
    """ Program Entry Point """

    try:

        logger.info("Version 4 - Pico & MicroPython - Asynchronous IO Example.")

        # Initialise all LEDs
        rate = pot.get_value()
        LED.set_rate_all(rate)  # Initialise all LEDS based on POT value.
        logger.info("Setting rate for all LEDs to {}".format(rate))
        logger.info("Turning the Potentiometer dial will change the rate for LED #{}".format(led_index))

        # Asynchronous IO
        asyncio.run(setup())

    except KeyboardInterrupt:
        LED.set_rate_all(0) # Turn all LEDs off.

main()
