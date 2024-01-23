"""
File: chapter08/pico/transistor_pico.py

Using MicroPython & Pico to Control a MOSFET Transistor.

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from time import sleep
from machine import Pin, PWM

GP = 21 # GPIO
p = Pin(GP, Pin.OUT)

# Note that after wrapping a Pin with PWM(), Pin methods including on(), off(), high(), low() and p.value(n) do not work.
# We can use pwm.duty_u16(65535) for fully 'on' and pwm.duty_u16(0) for fully'off'
pwm = PWM(p)
pwm.freq(8000)                                                          # (1)

try:
    print("On")
    pwm.duty_u16(65535) # Fully On.
    sleep(2)

    print("Off")
    pwm.duty_u16(0) # Fully Off.
    sleep(2)

    # Fade In.
    print("Fade In...")

    for duty_cycle_pc in range(0, 101):                                 # (3)
        print("Duty cycle {}%".format(duty_cycle_pc))
        
        # Translate Duty Cycle % (0 - 100) into a argument value for duty_u16 (0 - 65535)
        duty_cycle = int(65535 / 100 * duty_cycle_pc)
        
        pwm.duty_u16(duty_cycle)

        sleep(0.05)

    # Fade Out.
    print("\nFade Out...")
    
    for duty_cycle_pc in range(100, -1, -1):                             # (4)
        print("Duty cycle {}%".format(duty_cycle_pc))
        
        # Translate Duty Cycle % (0 - 100) into a argument value for duty_u16 (0 - 65535)
        duty_cycle = int(65535 / 100 * duty_cycle_pc)
        
        pwm.duty_u16(duty_cycle)

        sleep(0.05)

except KeyboardInterrupt:
    print("Bye")

finally:
    pwm.deinit()  # Disable PWM
    p.p.value(0)  # Ensure GPIO is Off

