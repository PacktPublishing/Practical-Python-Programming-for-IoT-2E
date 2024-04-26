"""
chapter13/pico/version4_asyncio_pico/Button.py

MicroPython Button Class.

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
from machine import Pin
from utime import time, ticks_ms, ticks_diff
import logging
import uasyncio as asyncio

logger = logging.getLogger('Button')


class Button:

    # Button States. These are passed as the parameter to the registered callback handler.
    PRESSED  = "PRESSED"
    RELEASED = "RELEASED"
    HOLD     = "HOLD"

    def __init__(self, gpio, hold_secs=0.5, callback=None):
        """ Constructor """
        
        self.gpio = gpio
        self.hold_secs = hold_secs
        self.callback = callback

        # Setup Button GPIO as INPUT and enable internal Pull-Up Resistor.
        # Our button is therefore Active LOW.
        self.pin = Pin(self.gpio, mode=Pin.IN, pull=Pin.PULL_UP)

        self._hold_timer = 0  # For detecting hold events.
        self.pressed = False  # True when button pressed, false when released.
        self.hold = False     # Hold has been detected.

        self.__last_level = self.pin.value() # Initialise last GPIO Level so we can detect button pressed and releases.

    def __str__(self):
        """ To String """
        return "Button on GPIO {}: pressed={}, hold={}".format(self.gpio, self.pressed, self.hold)


    async def run(self):
        """  Polling the Button GPIO """

        while True:

            level = self.pin.value()

            # Waiting for a GPIO level change.
            while level == self.__last_level:
                await asyncio.sleep(0)
                level = self.pin.value()

            # Level change has been detected.
            self.__last_level = level

            if level == 0: # Active LOW
                # Button is pressed.
                self.pressed = True

                if self.callback:
                    self.callback(self, Button.PRESSED)

                # While button is pressed start a timer to detect if it remains pressed for self.hold_secs
                hold_timeout_at = int(ticks_ms() + (self.hold_secs * 1000))
                
                while ticks_diff(ticks_ms(), hold_timeout_at) <= 0 and not self.pin.value():
                    await asyncio.sleep(0)

                if not self.pin.value(): # Active LOW
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
    """ Test Button Class """

    logging.basicConfig(level=logging.DEBUG)

    BUTTON_GPIO = 17

    def button_handler(the_button, state):
        logger.info(the_button)

    button = Button(gpio=BUTTON_GPIO,
                    hold_secs=0.5,
                    callback=button_handler)

    logger.info("Press or Hold the Button")

    loop = asyncio.get_event_loop()
    loop.create_task(button.run())
    loop.run_forever()