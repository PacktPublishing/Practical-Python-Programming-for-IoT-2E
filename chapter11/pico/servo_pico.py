"""
chapter11/rpi/servo_pico.py

Using a Pico & MicroPython to control a servo.

$ mpremote mount . run servo_pico.py

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
from time import sleep
from machine import Pin, PWM

SERVO_GPIO = 21

# Pulse widths for extreme left/right and center positions in nanoseconds.
# The default values are 'typical' values for a hobby servo.
# Be gradual when changing the left and right adjustments
# because a servo can be damaged if rotated beyond its limits.
RIGHT_PULSE   = 1000  # Smaller values for 'more' right             # (1)
LEFT_PULSE    = 2500  # Higher values for 'more' left
#CENTER_PULSE = 1500  # or calculate as below
CENTER_PULSE = ((LEFT_PULSE - RIGHT_PULSE) // 2) + RIGHT_PULSE

# Delay to give servo time to move
MOVEMENT_DELAY_SECS = 0.5                                           # (2)

# Note that after wrapping a Pin with PWM(), Pin methods including on(), off(), high(), low() and p.value(n) do not work.
# We can use pwm.duty_u16(65535) for fully 'on' and pwm.duty_u16(0) for fully'off'
p = Pin(SERVO_GPIO, Pin.OUT)
pwm = PWM(p)

# @TODO TBC
# Servos commonly operate at 50Hz, that is one pulse every 20ms  (1 second / 50 Hz = 0.02)
pwm.freq(50)

def idle():                                                         # (3)
    """
    Idle servo (zero pulse width).
    Servo will be rotatable by hand with little force.
    """
    pwm.duty_ns(0)


def center():
     """
     Center the servo.
     """
     pwm.duty_ns(CENTER_PULSE)


def left():
    """
    Rotate servo to full left position.
    """
    pwm.duty_ns(LEFT_PULSE)


def right():
    """
    Rotate servo to full right position.
    """
    pwm.duty_ns(RIGHT_PULSE)


def angle(to_angle):
    """
    Rotate servo to specified angle (between -90 and +90 degrees)
    """

    # Restrict to -90..+90 degrees
    to_angle = int(min(max(to_angle, -90), 90))

    ratio = (to_angle + 90) / 180.0
    pulse_range = LEFT_PULSE - RIGHT_PULSE
    pulse = LEFT_PULSE - round(ratio * pulse_range) 

    pwm.duty_ns(pulse)


def sweep(count=4):
    """
    Sweep servo horn left and right 'count' times.
    """
    left() # Starting position
    sleep(MOVEMENT_DELAY_SECS)

    for i in range(count):
        right()
        sleep(MOVEMENT_DELAY_SECS)
        left()
        sleep(MOVEMENT_DELAY_SECS)


if __name__ == '__main__':

    try:
        print("Sweeping left and right")
        sweep()

    finally:
        idle() # Idle servo.
        pwm.deinit()  # Disable PWM
        p.value(0)  # Ensure GPIO is Off
