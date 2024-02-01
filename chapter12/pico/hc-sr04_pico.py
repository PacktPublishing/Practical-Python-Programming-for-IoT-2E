"""
chapter12/pico/hc-sr04_pico.py

Using a Pico & MicroPython to measure distance with a HC-SR04 Sensor.

$ mpremote mount . run sr04_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from time import time, sleep_us, sleep_ms, ticks_ms, ticks_diff
from machine import Pin

# REMEMBER the HC-SR04 is a 5-volt
# device so you MUST use a voltage
# divider on ECHO_GPIO
TRIG_GPIO = 20                                         # (1)
ECHO_GPIO = 21


# Speed of Sound in meters per second
# at 20 degrees C (68 degrees F)
VELOCITY = 343                                         # (2)

# Sensor timeout and return value
TIMEOUT_SECS = 0.1   # based on max distance of 4m     # (3)
SENSOR_TIMEOUT  = -1

# Initialise GPIOs
trigger_pin = Pin(TRIG_GPIO, mode=Pin.OUT, value=0)
echo_pin = Pin(ECHO_GPIO, mode=Pin.IN, pull=Pin.PULL_DOWN)

# For timing our ultrasonic pulse
echo_callback = None                                   # (4)
tick_start = -1
tick_end = -1
reading_success = False


def trigger():                                         # (5)
    """ Trigger ultrasonic pulses """
    global reading_success

    reading_success = False

    # Start ultrasonic pulses
    trigger_pin.high()                                 # (6)
    sleep_us(10) # Pause 10 microseconds
    trigger_pin.low()


def get_distance_cms():                                # (7)
    """ Get distance in centimeters """
    trigger()

    timeout = ticks_ms() + (TIMEOUT_SECS * 1000)       # (8)

    while not reading_success:
      if ticks_diff(ticks_ms(), timeout) < 0:
          return SENSOR_TIMEOUT
      sleep_ms(10)

    # Elapsed time in milliseconds. Divide by 2 to get time from sensor to object.
    elapsed_milliseconds = ticks_diff(tick_start, tick_end) / 2                             # (9)
    
    # Convert to seconds
    elapsed_seconds = elapsed_milliseconds / 1000

    # Calculate distance in meters (d = v * t)
    distance_in_meters = elapsed_seconds * VELOCITY                                         # (10)

    # Convert to centimeters
    distance_in_centimeters = distance_in_meters * 100

    return distance_in_centimeters


def echo_handler(pin):                                                                      # (11)
    """ Called whenever a level change occurs on ECHO_GPIO Pin. """
    global tick_start, tick_end, reading_success

    if pin.value == 1:
        tick_start = ticks_ms() # Start Timer                                               # (12)

    elif pin.value == 0:
        tick_end = ticks_ms()   # End Timer                                                 # (13)
        reading_success = True


# Register ECHO Pin Callback
echo_callback = echo_pin.irq(handler=echo_handler, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)    # (14)

def main():
    """
    Program Main Entry Point.
    """

    while True:                                                                             # (15)

        distance_cms = get_distance_cms()

        if distance_cms == SENSOR_TIMEOUT:
            print("Timeout")
        else:
            distance_inches = distance_cms/2.54
            print(f"{distance_cms:0.4f}cm, {distance_inches:0.4f}\"")

        sleep_ms(250) # Sleep a little between readings. (Note - We shouldn't query the sensor more than once every 60ms.)


main()