"""
File: chapter08/rpi//transistor_rpi.py

Using a Raspberry & Python Control a MOSFET Transistor.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import pigpio
from time import sleep

GPIO = 21
pi = pigpio.pi()

# 8000 max hardware timed frequency by default pigpiod configuration.
pi.set_PWM_frequency(GPIO, 8000)

# We set the range to 0..100 to mimic 0%..100%. This means
# calls to pi.set_PWM_dutycycle(GPIO_PIN, duty_cycle) now
# take a value in the range 0 to 100 as the duty_cycle
# parameter rather than the default range of 0..255.
pi.set_PWM_range(GPIO, 100)                                      # (1)

try:
    print("On")
    pi.write(GPIO, pigpio.HIGH) # On                             # (2)
    sleep(2)

    print("Off")
    pi.write(GPIO, pigpio.LOW)  # Off 
    sleep(2)

    # Fade In.
    print("Fade In...")
    
    for duty_cycle_pc in range(0, 101):                           # (3)
        # duty_cycle_pc range is 0 to 100. The first 'from' arguement is inclusive, while the 2nd 'to' argument is exclusive.

        pi.set_PWM_dutycycle(GPIO, duty_cycle_pc)
        print("Duty cycle {}%".format(duty_cycle_pc))
        sleep(0.05)

    # Fade Out.
    print("\nFade Out...")

    for duty_cycle_pc in range(100, -1, -1):                        # (4)
        # duty_cycle_pc range is 100 to 0. The first 'from' arguement is inclusive, while the 2nd 'to' argument is exclusive.

        pi.set_PWM_dutycycle(GPIO, duty_cycle_pc)
        print("Duty Cycle {}%".format(duty_cycle_pc))
        sleep(0.05)

    # @TODO Removed, not  shure why it's needed sleep(2)

except KeyboardInterrupt:
    print("Bye")

finally:
    pi.write(GPIO, pigpio.LOW) # Ensure GPIO is Off
    pi.stop()                  # PiGPIO cleanup.

