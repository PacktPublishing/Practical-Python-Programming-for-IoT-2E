"""
chapter13/pico/version1_eventloop_pico/main.py

Event Loop example with Pico & MicroPython.

$ mpremote mount . run main.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from utime import sleep, ticks_ms, ticks_diff
from machine import Pin, ADC
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

#
# Setup LEDs
#

# Maximum and minimum "blinking" rates for the LEDs. These values will be the
# mapped values returned by our Potentiometer.
MIN_RATE = 0 # Seconds
MAX_RATE = 5 # Seconds

# GPIO's that our LEDs are connected to.
LED1_GPIO = 20
LED2_GPIO = 21

# Configure LED Pins as OUTPUT and turn LEDs off.
led_pins = [
    Pin(LED1_GPIO, mode=Pin.OUT, value=0),
    Pin(LED2_GPIO, mode=Pin.OUT, value=0)
]

# Variables to manage LEDs and their blinking.
led_index = 0
led_rates = [0, 0]
led_toggle_at_time = [0, 0]


#
# Setup Button
#
BUTTON_GPIO = 16
BUTTON_HOLD_SECS = 0.5

# Button GPIO is configured as INPUT with an internal pull-up resistor enabled,
# thus the button will be Active LOW.
button_pin = Pin(BUTTON_GPIO, mode=Pin.IN, pull=Pin.PULL_UP)

#
# Setup Potentiometer
#

# ADC Channel	GPIO
# -----------   ----
# 0	            26
# 1	            27
# 2	            28

POT_ADC_CHANNEL = 0
pot_adc = ADC(POT_ADC_CHANNEL)

# Edge adjustments for the Potentiometer's full CW/CCW positions.
# If you experience value issues when your Potentiometer it is rotated fully
# clockwise or counter-clockwise, adjust these variables. Please see the
# ADC example in "Chapter @TODO Connecting Your Raspberry Pi & Pico to the Physical World"
# for a discussion regarding edge value adjustments for Pots and ADC.
EDGE_ADJUST = 1000
MIN_POT_VALUE = 0 + EDGE_ADJUST
MAX_POT_VALUE = 65535 - EDGE_ADJUST

def map_value(in_v, in_min, in_max, out_min, out_max):
    """ Helper method to map an input value (v_in) between alternative max/min ranges. """
    v = (in_v - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return max(min(out_max, v), out_min)


def main():
    """ Program Entry Point """
    global led_rates, led_index, led_toggle_at_time

    SLEEP_DELAY = 0.01 # Seconds

    try:
        logger.info("Version 1 - Pico & MicroPython - Event Loop Example.")

        # Get initial reading from Potentiometer/ADC and map into a blinking 'rate'
        reading = pot_adc.read_u16()
        rate = round(map_value(reading, MIN_POT_VALUE, MAX_POT_VALUE, MIN_RATE, MAX_RATE), 1)

        # Initialise all LEDs
        led_rates = [rate] * len(led_rates) # Initialise blink rate to match POT value.
        logger.info("Setting rate for all LEDs to {}".format(rate))

        # State variables.
        last_rate = rate
        last_led_index = 0
        was_pressed = False
        button_held = False
        button_pressed = False
        button_hold_timer = 0

        logger.info("Turning the Potentiometer dial will change the rate for LED #{}".format(last_led_index))

        #
        # Start of "Event Loop"
        #
        while True:                                                                           # (1)
            #
            # Check if the button is pressed or held down.
            #
            button_pressed = button_pin.value() == 0 # Button is Active LOW.                  # (2)

            if button_pressed and not button_held:
                # Button has been pressed.
                button_hold_timer += SLEEP_DELAY
                was_pressed = True

            elif not button_pressed:

                if was_pressed and not button_held:
                    # Button has been released

                    # Update 'led_index' so that Potentiometer adjustments affect the next LED.
                    led_index += 1
                    if led_index >= len(led_pins):
                        led_index = 0

                    if led_index != last_led_index:
                        logger.info("Turning the Potentiometer dial will change the rate for LED #{}".format(led_index))
                        last_led_index = led_index

                button_held = False
                button_hold_timer = 0
                was_pressed = False

            if button_hold_timer >= BUTTON_HOLD_SECS and not button_held:
                # Button has been held down

                # Set all LEDs to same rate
                logger.info("Changing rate for all LEDs to {}".format(rate))
                led_rates = [rate] * len(led_rates)
                led_toggle_at_time = [0] * len(led_rates)

                for pin in led_pins:
                    # Turn all LEDs off so that when they start blinking (below) are all synchronised.
                    pin.value(0) # LED Off.

                button_hold_timer = 0
                button_held = True

            #
            # Check if the Potentiometer dial been turned.
            #
            reading = pot_adc.read_u16()
            rate = round(map_value(reading, MIN_POT_VALUE, MAX_POT_VALUE, MIN_RATE, MAX_RATE), 1)

            if rate != last_rate:
                # Set individual LED (at led_index) to new blinking rate
                logger.info("Changing LED #{} rate to {}".format(led_index, rate))
                led_rates[led_index] = rate
                last_rate = rate

            #
            # Blink the LEDs.
            #
            now = ticks_ms()                                                                      # (3)

            for i in range(len(led_pins)):
                if led_rates[i] <= 0:
                    led_pins[i].value(0) # LED Off.
                elif ticks_diff(now, led_toggle_at_time[i]) >= 0:
                    led_pins[i].toggle() # Toggle LED on/off.
                    led_toggle_at_time[i] = int(now + (led_rates[i] * 1000))

            logger.debug("Sleep...")
            sleep(SLEEP_DELAY)

    except KeyboardInterrupt:

        # Turn all LEDs off.
        for pin in led_pins:
            pin.value(0) # LED Off.


main()