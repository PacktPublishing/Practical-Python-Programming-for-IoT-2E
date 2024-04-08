"""
File: chapter07/rpi/analog_pwm_output_test_rpi.py

Using a Raspberry Pi & Python to create a PWM output signal

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import pigpio
from time import sleep

GPIO = 21
pi = pigpio.pi()

# 8000 max hardware timed frequency by default pigpiod configuration.
pi.set_PWM_frequency(GPIO, 8000)                                        # (1)

duty_cycle_percentages = [0, 25, 50, 75, 100]                           # (2)
max_voltage = 3.3

try:
    while True:
       for duty_cycle_pc in duty_cycle_percentages:                     # (3)
           
           # 255 is the max value for pi.set_PWM_dutycycle
           duty_cycle = int(255 * duty_cycle_pc / 100)
           estimated_voltage = max_voltage * duty_cycle_pc / 100
           print("Duty Cycle {}%, estimated voltage {} volts".format(duty_cycle_pc, estimated_voltage))
           
           pi.set_PWM_dutycycle(GPIO, duty_cycle)                       # (4)
           sleep(5)

except KeyboardInterrupt:
  print("Bye")
  pi.stop() # PiGPIO cleanup.
