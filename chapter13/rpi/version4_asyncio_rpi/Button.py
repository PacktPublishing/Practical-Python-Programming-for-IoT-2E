"""
chapter13/rpi/version2_asyncio_rpi/Button.py

Python Button Class.

Dependencies:
  pip3 install pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import pigpio
from time import time
import logging
import asyncio

logger = logging.getLogger('BUTTON')

class Button:

    # Button States. These are passed as the parameter to the registered callback handler.
    PRESSED  = "PRESSED"
    RELEASED = "RELEASED"
    HOLD     = "HOLD"

    def __init__(self, gpio, pi, hold_secs=0.5, callback=None):
        """ Constructor """
        self.gpio = gpio
        self.pi = pi
        self.hold_secs = hold_secs
        self.callback = callback

        # Setup Button GPIO as INPUT and enable internal Pull-Up Resistor.
        # Our button is therefore Active LOW.
        self.pi.set_mode(gpio, pigpio.INPUT)
        self.pi.set_pull_up_down(gpio, pigpio.PUD_UP)
        self.pi.set_glitch_filter(gpio, 10000) # microseconds debounce

        self._hold_timer = 0  # For detecting hold events.
        self.pressed = False  # True when button pressed, false when released.
        self.hold = False     # Hold has been detected.

        self.__last_level = self.pi.read(self.gpio) # Initialise last GPIO Level so we can detect button pressed and releases.

    def __str__(self):
        """ To String """
        return "Button on GPIO {}: pressed={}, hold={}".format(self.gpio, self.pressed, self.hold)


    async def run(self):
        """  Polling the Button GPIO for state changes """

        while True:

            level = self.pi.read(self.gpio) # LOW(0) or HIGH(1)

            # Waiting for a GPIO level change.
            while level == self.__last_level:
                await asyncio.sleep(0)
                level = self.pi.read(self.gpio)

            # Level change has been detected.
            self.__last_level = level

            if level == pigpio.LOW: # Active LOW
                # Button is pressed.
                self.pressed = True

                if self.callback:
                    self.callback(self, Button.PRESSED)

                # While button is pressed start a timer to detect if it remains pressed for self.hold_secs
                hold_timeout_at = time() + self.hold_secs
                while (time() < hold_timeout_at) and not self.pi.read(self.gpio):
                    await asyncio.sleep(0)

                if not self.pi.read(self.gpio): # Active LOW
                    # Button is still pressed after self.hold_secs
                    self.hold = True

                    if self.callback:
                        self.callback(self, Button.HOLD)

            else: # level is HIGH
                self.pressed = False
                self.hold = False

                if self.callback:
                    self.callback(self, Button.RELEASED)

            await asyncio.sleep(0)


if __name__ == '__main__':
    """ Run from command line to test Button Class. Control + C to exit. """

    logging.basicConfig(level=logging.DEBUG)

    BUTTON_GPIO = 21

    def button_handler(the_button, state):
        logger.info(the_button)

    button = Button(gpio=BUTTON_GPIO,
                    pi=pigpio.pi(),
                    hold_secs=0.5,
                    callback=button_handler)

    logger.info("Press or Hold the Button")

    loop = asyncio.get_event_loop()
    loop.create_task(button.run())
    loop.run_forever()
