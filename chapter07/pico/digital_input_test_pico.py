"""
File: chapter07/pico/digital_input_test_pico.py

Using a Pico & MicroPython to test digital input

$ mpremote mount . run digital_input_test_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from time import sleep_ms
from machine import Pin

GPIO = 21

p = Pin(GPIO, mode=Pin.IN, pull=None)                       # (1)
#p = Pin(GPIO, mode=Pin.IN, pull=Pin.PULL_UP)
#p = Pin(GPIO, mode=Pin.IN, pull=Pin.PULL_DOWN)

try:
    while True:                                             # (2)
        state = p.value() # 0 or 1
        print("GPIO {} is {}".format(GPIO, state))
        sleep_ms(20)

except KeyboardInterrupt:
  print("Bye")