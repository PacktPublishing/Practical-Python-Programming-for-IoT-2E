"""
chapter13/pico/version4_asyncio_pico/Pot.py

MicroPython Potentiometer Class for ADS1115 ADC.

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
from time import sleep
from machine import Pin, I2C
import logging
import uasyncio as asyncio
from ADS1115_pico import ADS1115

logger = logging.getLogger('Pot')

class Pot:

    # Edge adjustments for the Potentiometer's full CW/CCW positions.
    # If you experience value issues when your Potentiometer it is rotated fully
    # clockwise or counter-clockwise, adjust these variables. Please see the
    # ADC example in "@TODO Connecting Your Raspberry Pi & Pico to the Physical World"
    # for a discussion regarding edge value adjustments for Pots and ADC.
    EDGE_ADJUST = 100
    MIN_POT_VALUE = 0 + EDGE_ADJUST
    MAX_POT_VALUE = 26400 - EDGE_ADJUST


    def __init__(self, analog_channel, min_value, max_value, scl_gpio=13, sda_gpio=12, bus_id=0, callback=None):
        """ Constructor """
        
        self.analog_channel = analog_channel
        self.i2c = I2C(bus_id, scl=Pin(scl_gpio), sda=Pin(sda_gpio))
        self.adc = ADS1115(self.i2c)

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
        reading = self.adc.read(self.analog_channel)
        return round(self._map_value(reading['value']), 1) # Mapped to min_value/max_value range

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
