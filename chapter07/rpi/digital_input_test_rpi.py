"""
File: chapter07/rpi/digital_input_test_rpi.py

Using a Raspberry Pi & Python to test digital input

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import pigpio
from time import sleep

GPIO = 21
pi = pigpio.pi()
pi.set_mode(GPIO, pigpio.INPUT)                         # (1)
pi.set_pull_up_down(GPIO, pigpio.PUD_OFF)
#pi.set_pull_up_down(GPIO_PIN, pigpio.PUD_UP)
#pi.set_pull_up_down(GPIO_PIN, pigpio.PUD_DOWN)

try:
    while True:                                          # (2)
        state = pi.read(GPIO);
        print("GPIO {} is {}".format(GPIO, state))
        sleep(0.02)

except KeyboardInterrupt:
  print("Bye")
  pi.stop() # PiGPIO cleanup.