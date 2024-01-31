"""
chapter12/pico/hall_effect_digital_pico.py

Using a Pico & MicroPython with a Switch or Latching Type A4133 Hall-Effect Sensor (Active LOW).

$ mpremote mount . run hall_effect_digital_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from time import sleep
from signal import pause
import pigpio

GPIO = 21

pi = pigpio.pi()

# Initialise GPIO
pi.set_mode(GPIO, pigpio.INPUT)

# Pull-Up. A3144 Hall-Effect sensor is Active LOW.
# so pull-up for inactive HIGH.
pi.set_pull_up_down(GPIO, pigpio.PUD_UP)
pi.set_glitch_filter(GPIO, 10000) # microseconds debounce

def callback_handler(gpio, level, tick):
    """ Called whenever a level change occurs on GPIO Pin.
      Parameters defined by PiGPIO pi.callback() """

    print("GPIO {} is {}.".format(gpio, "HIGH" if level else "LOW"))


# Register Callback
callback = pi.callback(GPIO, pigpio.EITHER_EDGE, callback_handler)


if __name__ == "__main__":

    try:
        print("Monitoring GPIO {}. Press Control + C to Exit.".format(GPIO))
        print("A3144 Hall-Effect Sensor is Active LOW.")
        print("GPIO {} is {}.".format(GPIO, "HIGH" if pi.read(GPIO) else "LOW"))
        pause()

    except KeyboardInterrupt:
        callback.cancel()
        pi.stop()
