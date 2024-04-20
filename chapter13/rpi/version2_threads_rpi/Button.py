"""
chapter13/rpi/version2_threads_rpi/Button.py

Python Button Class.

Dependencies:
  pip3 install pigpio adafruit-circuitpython-ads1x15

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import pigpio
from time import sleep
import logging

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

        # Register internal PiGPIO callback (as an alternative to polling the button in a while loop)
        self._pigpio_callback = self.pi.callback(self.gpio, pigpio.EITHER_EDGE, self._callback_handler)


    def __str__(self):
        """ To String """
        return "Button on GPIO {}: pressed={}, hold={}".format(self.gpio, self.pressed, self.hold)


    def _callback_handler(self, gpio, level, tick):                                      # (1)
        """ PiGPIO Callback """

        if level == pigpio.LOW: # Active LOW
            # Button is pressed
            self.pressed = True

            if self.callback:
                self.callback(self, Button.PRESSED)

            # While button is pressed start a timer to detect if
            # it remains pressed for self.hold_secs
            timer = 0                                                                    # (2)
            while (timer < self.hold_secs) and not self.pi.read(self.gpio):
                sleep(0.01)
                timer += 0.01

            if not self.pi.read(self.gpio): # Active LOW
                # Button is still pressed after self.hold_secs
                self.hold = True

                if self.callback:
                    self.callback(self, Button.HOLD)

        else: # level is HIGH
            # Button released
            self.pressed = False
            self.hold = False

            if self.callback:
                self.callback(self, Button.RELEASED)


if __name__ == '__main__':
    """ Run from command line to test Button Class. Control + C to exit. """

    from signal import pause

    logging.basicConfig(level=logging.DEBUG)
    print("Press or Hold the Button")

    BUTTON_GPIO = 21

    def button_handler(the_button, state):
        print(the_button)

    button = Button(gpio=BUTTON_GPIO,
                    pi=pigpio.pi(),
                    hold_secs=0.5,
                    callback=button_handler)

    pause()
