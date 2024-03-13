"""
chapter12/pico/hc-sr501_pico.py

Using a Pico & MicroPython to read a HC-SR501 PIR Sensor.

$ mpremote mount . run hc-sr501_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from signal import pause
import pigpio

GPIO = 21
triggered = False

pi = pigpio.pi()

# Initialise GPIO
pi.set_mode(GPIO, pigpio.INPUT)                                      # (1)
pi.set_pull_up_down(GPIO, pigpio.PUD_DOWN)
pi.set_glitch_filter(GPIO, 10000) # microseconds debounce            # (2)

def callback_handler(gpio, level, tick):                             # (3)
    """ Called whenever a level change occurs on GPIO Pin.
      Parameters defined by PiGPIO pi.callback() """
    global triggered

    if level == pigpio.HIGH:
        triggered = True
        print("Triggered")
    elif level == pigpio.LOW:
        triggered = False
        print("Not Triggered")


# Register Callback
callback = pi.callback(GPIO, pigpio.EITHER_EDGE, callback_handler)   # (4)


if __name__ == "__main__":

    try:
        print("\nPLEASE NOTE - The HC-SR501 needs 1 minute after applying power to initialise itself.\n")
        print("Monitoring environment...")
        print("Press Control + C to Exit")
        pause()

    except KeyboardInterrupt:
        callback.cancel()
        pi.stop()
