"""
chapter12/pico/hc-sr501_pico.py

Using a Pico & MicroPython to read a HC-SR501 PIR Sensor.

$ mpremote mount . run hc-sr501_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from machine import Pin
from time import sleep_ms

GPIO = 21
triggered = False

# Initialise GPIO
pin = Pin(GPIO, mode=Pin.IN, pull=Pin.PULL_DOWN)                     # (1)

#@FIXME pi.set_glitch_filter(GPIO, 10000) # microseconds debounce            # (2)

def callback_handler(pin):                             # (3)
    """ Called whenever a level change occurs on GPIO Pin. """
    global triggered

    if pin.value() == 1:
        triggered = True
        print("Triggered")
    elif pin.value() == 0:
        triggered = False
        print("Not Triggered")


# Register Callback
callback = pin.irq(handler=callback_handler, trigger=Pin.IRQ_RISING | Pin.IRQ_FALLING)  # (4)

if __name__ == "__main__":

    print("\nPLEASE NOTE - The HC-SR501 needs 1 minute after applying power to initialise itself.\n")
    print("Monitoring environment...")
    print("Press Control + C to Exit")

    # Simple keep-alive because we are using IRQ callback on GPIO/pin
    while True:
        sleep_ms(10)
    