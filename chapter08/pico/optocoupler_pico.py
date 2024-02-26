"""
chapter08/pico/optocoupler_pico.py

Using a Pico & MicroPython to control an optocoupler.

$ mpremote mount . run optocoupler_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from time import sleep
from machine import Pin, PWM

GPIO = 21
p = Pin(GPIO, Pin.OUT)

try:
    # Note: Circuit is wired as ACTIVE LOW.
    p.value(0)  # On                     # (1)
    print("On")
    sleep(2)
    p.value(1)  # Off                    # (2)
    print("Off")
    sleep(2)

except KeyboardInterrupt:
    print("Bye")

finally:
    p.value(1)  # Off
    

