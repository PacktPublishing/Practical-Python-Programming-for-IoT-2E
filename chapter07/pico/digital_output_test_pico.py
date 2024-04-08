"""
File: chapter07/pico/digital_output_test_pico.py

Using a Pico & MicroPython to test digital output

$ mpremote mount . run digital_output_test_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from time import sleep
from machine import Pin

GPIO = 21

p = Pin(GPIO, Pin.OUT)                                 # (1)

try:
    while True:                                        # (2)
        # Alternate between HIGH and LOW
        state = p.value()            # 1 or 0
        new_state = (int)(not state) # 1 or 0
        p.value(new_state)
        print("GPIO {} is {}".format(GPIO, new_state))
        sleep(3)

except KeyboardInterrupt:
    print("Bye")
