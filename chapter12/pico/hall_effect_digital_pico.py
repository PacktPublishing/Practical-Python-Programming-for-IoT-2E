"""
chapter12/pico/hall_effect_digital_pico.py

Using a Pico & MicroPython with a Switch or Latching Type A4133 Hall-Effect Sensor (Active LOW).

$ mpremote mount . run hall_effect_digital_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from time import sleep_ms
from machine import Pin

GPIO = 21

# Initialise GPIO with Pull-Up. A3144 Hall-Effect sensor is Active LOW.
# so pull-up for inactive HIGH.
pin = Pin(GPIO, mode=Pin.IN, pull=Pin.PULL_UP)

def callback_handler(pin):
    """ Called whenever a level change occurs on GPIO Pin. """
    print("GPIO {} is {}.".format(GPIO, "HIGH" if pin.value() else "LOW"))


# Register Callback
callback = pin.irq(handler=callback_handler, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)


if __name__ == "__main__":

    print("Monitoring GPIO {}. Press Control + C to Exit.".format(GPIO))
    print("A3144 Hall-Effect Sensor is Active LOW.")
    print("GPIO {} is {}.".format(GPIO, "HIGH" if pin.value() else "LOW"))

    # Simple keep-alive because we are using IRQ callback on GPIO/pin
    while True:
        sleep_ms(10)
