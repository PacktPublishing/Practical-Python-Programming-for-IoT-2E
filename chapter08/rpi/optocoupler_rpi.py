"""
File: chapter08/rpi/optocoupler_rpi.py

Using a Raspberry & Python Control an Optocoupler.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import pigpio
from time import sleep

GPIO = 21
pi = pigpio.pi()

try:
    # Note: Circuit is wired as ACTIVE LOW.
    pi.write(GPIO, pigpio.LOW) # On.                       # (1)
    print("On")
    sleep(2)
    pi.write(GPIO, pigpio.HIGH)  # Off.                    # (2)
    print("Off")
    sleep(2)

except KeyboardInterrupt:
    print("Bye")

finally:
    pi.write(GPIO, pigpio.HIGH) # Off.
    pi.stop() # PiGPIO cleanup.

