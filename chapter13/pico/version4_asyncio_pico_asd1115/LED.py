"""
chapter13/pico/version4_asyncio_pico/Button.py

MicroPython LED Class.

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
from machine import Pin
from utime import ticks_ms, ticks_diff
import logging
import uasyncio as asyncio

logger = logging.getLogger('LED')

class LED:

    # A list of all LED instances that have been created.
    instances = []

    @classmethod
    def set_rate_all(cls, rate):
        """ Set rate and synchronise all LEDs """

        # Turn all LED's Off
        for i in LED.instances:
            i.set_rate(0)

        # Start LED's blinking
        for i in LED.instances:
            i.set_rate(rate)


    def __init__(self, gpio, rate=0):
        """ Constructor """

        self.gpio = gpio
        self.blink_rate_secs = 0
        self.toggle_at = 0 # time when we will toggle the LED On/Off. <=0 means LED is off.

        # Configure LED GP as Output and LOW (0) (ie LED Off) by default.
        self.pin = Pin(gpio, mode=Pin.OUT, value=0)

        # Add this LED instance to the Class-level instances list/array.
        LED.instances.append(self)

        # Start LED blinking (Note it will not start blinking until .run() has been registered with an event-loop!)
        self.set_rate(rate)


    def __del__(self):
        """ Destructor """
        self.instances.remove(self)


    def __str__(self):
        """ To String """

        if self.is_blinking:
            return "LED on GP {} is blinking at a rate of {} seconds".format(self.gpio, self.blink_rate_secs)
        else:
            return "LED on GP {} is Off".format(self.gpio)


    async def run(self):
        """ Do the blinking """

        while True:                                                                      # (1)

            if self.toggle_at > 0 and ticks_diff(ticks_ms(), self.toggle_at) >= 0:       # (2)

                self.pin.toggle() # Toggle LED
                self.toggle_at += int(self.blink_rate_secs * 1000) # Seconds to Milliseconds

                logger.debug("LED on GP {} is {}".format(self.gpio, "On" if self.pin.value else "Off"))
                                
            await asyncio.sleep(0)                                                       # (3)

    def set_rate(self, secs):
        """ Set LED blinking rate.
        A rate <= 0 will turn the LED off. """

        logger.debug("LED on GP {} is blinking at a rate of {} seconds.".format(self.gpio, secs))
        self.blink_rate_secs = secs

        if secs <= 0:
            self.toggle_at = 0

            # Turn LED Off. @TODO Cleanup
            # self.pin.off() # or 
            self.pin.value(0) # or 
            # self.pin.low()

        else:            
            self.toggle_at = int(ticks_ms() + (self.blink_rate_secs * 1000)) # Seconds to Milliseconds

            # Turn LED On. @TODO Cleanup
            # self.pin.on() # or
            # self.pin.high() # or
            self.pin.value(1)


    def is_blinking(self):
        """ Test if the LED is blinking. """
        return self.blink_rate_secs > 0


if __name__ == '__main__':
    """ Test the LED Class """

    logging.basicConfig(level=logging.DEBUG)

    LED_GP = 21

    led = LED(gpio=LED_GP, rate=0)
    led.set_rate(0.1) # seconds

    loop = asyncio.get_event_loop()
    loop.create_task(led.run())

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        led.set_rate(0) # LED Off.
