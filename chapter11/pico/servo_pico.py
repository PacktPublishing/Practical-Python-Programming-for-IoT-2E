"""
chapter11/pico/servo_pico.py

Using a Pico & MicroPython to control a servo.

$ mpremote mount . run servo_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from time import sleep_ms
from machine import Pin, PWM

SERVO_GPIO = 21

# Pulse widths for extreme left/right and center positions in microseconds.
# The default values are 'typical' values for a hobby servo.
# Be gradual when changing the left and right adjustments
# because a servo can be damaged if rotated beyond its limits.
RIGHT_PULSE   = 1000  # Smaller values for 'more' right             # (1)
LEFT_PULSE    = 2000  # Higher values for 'more' left
# CENTER_PULSE = 1500  # or calculate as below
CENTER_PULSE = ((LEFT_PULSE - RIGHT_PULSE) // 2) + RIGHT_PULSE

# Delay to give servo time to move (milliseconds)
MOVEMENT_DELAY_MS = 500                                             # (2)

# Note that after wrapping a Pin with PWM(), Pin methods including on(), off(), high(), low() and p.value(n) do not work.
# We can use pwm.duty_u16(65535) for fully 'on' and pwm.duty_u16(0) for fully'off'
p = Pin(SERVO_GPIO, Pin.OUT)
pwm = PWM(p)

# Servos commonly operate at 50Hz, that is one pulse every 20ms  (1 second / 50 Hz = 0.02)
pwm.freq(50)


def left():                                                         # (3)
    """
    Rotate servo to full left position.
    """

    # Multiply by 1000 to convert microseconds to nanoseconds. 
    pwm.duty_ns(int(LEFT_PULSE * 1000))


def center():
     """
     Center the servo.
     """
     
     # Multiply by 1000 to convert microseconds to nanoseconds. 
     pwm.duty_ns(int(CENTER_PULSE * 1000))


def right():
    """
    Rotate servo to full right position.
    """

    # Multiply by 1000 to convert microseconds to nanoseconds. 
    pwm.duty_ns(int(RIGHT_PULSE * 1000))


def idle():                                                         # (4)
    """
    Idle servo (zero pulse width).
    Servo will be rotatable by hand with little force.
    """
    pwm.duty_ns(0)


def angle(to_angle):                                                # (5)
    """
    Rotate servo to specified angle (between -90 and +90 degrees)
    """

    # Restrict to -90..+90 degrees
    to_angle = int(min(max(to_angle, -90), 90))

    ratio = (to_angle + 90) / 180.0                                 # (6)
    pulse_range = LEFT_PULSE - RIGHT_PULSE
    pulse = LEFT_PULSE - round(ratio * pulse_range)                 # (7)

    # Multiply by 1000 to convert microseconds to nanoseconds. 
    pwm.duty_ns(int(pulse * 1000))


def sweep(count=4):                                                 # (8)
    """
    Sweep servo horn left and right 'count' times.
    """
    left() # Starting position
    sleep_ms(MOVEMENT_DELAY_MS)

    for i in range(count):
        right()
        sleep_ms(MOVEMENT_DELAY_MS)
        left()
        sleep_ms(MOVEMENT_DELAY_MS)


if __name__ == '__main__':

    try:
        print("Centering")
        center()
        sleep_ms(1000)

        print("Sweeping left and right")
        sweep()
        sleep_ms(1000)

        print("Centering")
        center()
        sleep_ms(1000)

    finally:
        idle() # Idle servo.
        pwm.deinit()  # Disable PWM
        p.value(0)  # Ensure GPIO is Off
