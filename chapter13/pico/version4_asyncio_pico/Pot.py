"""
chapter13/pico/version4_asyncio_pico/Pot.py

MicroPython Potentiometer Class.

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""

# Sanity check that runtime is MicroPython.
from platform import platform
assert platform().startswith("MicroPython"), "This code is for MicroPython, (not CPython)"

from time import sleep
import machine
import logging
import uasyncio as asyncio

logger = logging.getLogger('Pot')

class Pot:

    # Edge adjustments for the Potentiometer's full CW/CCW positions.
    # If you experience value issues when your Potentiometer it is rotated fully
    # clockwise or counter-clockwise, adjust these variables. Please see the
    # ADS1115 example in "Chapter 5 Connecting Your Raspberry Pi & Pico to the Physical World"
    # for a discussion regarding edge value adjustments for Pots and ADC.
    EDGE_ADJUST = 100
    MIN_POT_VALUE = 0 + EDGE_ADJUST
    MAX_POT_VALUE = 65335 - EDGE_ADJUST


    def __init__(self, analog_channel, min_value, max_value, callback=None):
        """ Constructor """
        
        self.pin = machine.ADC(analog_channel)

        # Min and Max values returned by .get_value()
        self.min_value = min_value
        self.max_value = max_value

        self.callback = callback

        self.last_value = self.get_value()


    def __str__(self):
        """ To String """
        return "Potentiometer mapped value is {}".format(self.get_value())


    async def run(self):
        """ Poll ADC for Voltage Changes """

        while True:

            # Check if the Potentiometer has been adjusted.
            current_value = self.get_value()
            if self.last_value != current_value:
                
                logger.debug("Potentiometer mapped value is {}".format(current_value))

                if self.callback:
                    self.callback(self, current_value)

                self.last_value = current_value

            await asyncio.sleep(0)


    def _map_value(self, in_v):
        """ Helper method to map an input value (v_in) between alternative max/min ranges. """
        v = (in_v - self.MIN_POT_VALUE) * (self.max_value - self.min_value) / (self.MAX_POT_VALUE - self.MIN_POT_VALUE) + self.min_value
        return max(min(self.max_value, v), self.min_value)


    def get_value(self):
        """ Get current value """
        reading = self.pin.read_u16() # a value 0..65335
        return round(self._map_value(reading), 1) # Mapped to min_value/max_value range

if __name__ == '__main__':
    """ Test Pot Class """

    logging.basicConfig(level=logging.DEBUG)

    def pot_handler(the_pot, value):
        logger.info(the_pot)

    pot = Pot(analog_channel=0, # Ch 0 is Pin 26
              min_value=0,
              max_value=5,
              callback=pot_handler)

    loop = asyncio.get_event_loop()
    loop.create_task(pot.run())
    loop.run_forever()
