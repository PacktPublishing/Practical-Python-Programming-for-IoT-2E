"""
File: chapter07/rpi/digital_output_test_rpi.py

Using a Raspberry Pi & Python to test digital output

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import pigpio
from time import sleep

GPIO = 21
pi = pigpio.pi()
pi.set_mode(GPIO, pigpio.OUTPUT)                   # (1)

try:
    while True:                                    # (2)
        # Alternate between HIGH and LOW
        state = pi.read(GPIO)        # 1 or 0
        new_state = (int)(not state) # 1 or 0
        pi.write(GPIO, new_state);
        print("GPIO {} is {}".format(GPIO, new_state))
        sleep(3)

except KeyboardInterrupt:
    print("Bye")
    pi.stop()  # PiGPIO cleanup.
