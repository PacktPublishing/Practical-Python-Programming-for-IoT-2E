"""
File: chapter07/pico/analog_pwm_output_test_pico.py

Using a Pico & MicroPython to create a PWM output signal with Pico Internal ADC

$ mpremote mount . run analog_pwm_output_test_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from time import sleep
from machine import Pin, PWM

GPIO = 21

pwm = PWM(Pin(GPIO, mode=Pin.OUT))

pwm.freq(5000)                                                    # (1)

duty_cycle_percentages = [0, 25, 50, 75, 100]                     # (2)
max_voltage = 3.3

try:
    while True:
       for duty_cycle_pc in duty_cycle_percentages:               # (3)
           
           # 65535 is the max value for pwm.duty_u16()
           duty_cycle = int(65535 / 100 * duty_cycle_pc)
           estimated_voltage = max_voltage * duty_cycle_pc / 100

           print("Duty Cycle {}%, estimated voltage {} volts".format(duty_cycle_pc, estimated_voltage))
           pwm.duty_u16(duty_cycle)                               # (4)
           sleep(5)

except KeyboardInterrupt:
  print("Bye")
