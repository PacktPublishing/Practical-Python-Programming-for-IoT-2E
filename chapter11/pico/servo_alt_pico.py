"""
chapter11/pico/servo_alt_pico.py

Using a Pico & MicroPython to control a servo.

$ mpremote mount . run servo_alt_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from time import sleep_ms
from machine import Pin, PWM

SERVO_GPIO = 21

# Pulse widths for extreme left/right and center positions in microseconds.
# The default values are 'typical' values for a hobby servo.
# Be gradual when changing the left and right adjustments
# because a servo can be damaged if rotated beyond its limits.
RIGHT_PULSE = 1000  # Smaller values for 'more' right
LEFT_PULSE  = 2000  # Higher values for 'more' left
# CENTER_PULSE = 1500  # or calculate as below
CENTER_PULSE = ((LEFT_PULSE - RIGHT_PULSE) // 2) + RIGHT_PULSE

# Delay to give servo time to move (milliseconds)
MOVEMENT_DELAY_MS = 500

# Note that after wrapping a Pin with PWM(), Pin methods including on(), off(), high(), low() and p.value(n) do not work.
# We can use pwm.duty_u16(65535) for fully 'on' and pwm.duty_u16(0) for fully'off'
p = Pin(SERVO_GPIO, Pin.OUT)
pwm = PWM(p)

# Servos commonly operate at 50Hz, that is one pulse every 20ms  (1 second / 50 Hz = 0.02)
pwm.freq(50)
PULSE_WIDTH = 20000.0  # 20000 microsecond = 20 milliseconds = 0.02 seconds

DUTYCYCLE_RANGE = 65535 # this is the max value for pwm.duty_u16()

def idle():
    """
    Idle servo (zero pulse width).
    Servo will be rotatable by hand with little force.
    """

    # WAS
    # pwm.duty_ns(0)

    # NOW
    dutycycle = 0
    pwm.duty_u16(dutycycle)


def center():
    """
    Center the servo.
    """

    # WAS
    # pwm.duty_ns(int(CENTER_PULSE * 1000))

    # NOW
    dutycycle_percent = CENTER_PULSE / PULSE_WIDTH
    # Scale duty cycle percentage into PiGPIO duty cycle range 
    dutycycle = int(dutycycle_percent * DUTYCYCLE_RANGE)
    pwm.duty_u16(dutycycle)


def left():
    """
    Rotate servo to full left position.
    """

    # WAS
    # pwm.duty_ns(int(LEFT_PULSE * 1000))

    # NOW
    dutycycle_percent = LEFT_PULSE / PULSE_WIDTH

    # Scale duty cycle percentage into PiGPIO duty cycle range 
    dutycycle = int(dutycycle_percent * DUTYCYCLE_RANGE)

    pwm.duty_u16(dutycycle)


def right():
    """
    Rotate servo to full right position.
    """

    # WAS
    # pwm.duty_ns(int(RIGHT_PULSE * 1000))

    # NOW
    dutycycle_percent = RIGHT_PULSE / PULSE_WIDTH

    # Scale duty cycle percentage into PiGPIO duty cycle range
    dutycycle = int(dutycycle_percent * DUTYCYCLE_RANGE)

    pwm.duty_u16(dutycycle)


def angle(to_angle):
    """
    Rotate servo to specified angle (between -90 and +90 degrees)
    """

    # Restrict to -90..+90 degrees
    to_angle = int(min(max(to_angle, -90), 90))

    ratio = (to_angle + 90) / 180.0
    pulse_range = LEFT_PULSE - RIGHT_PULSE
    pulse = LEFT_PULSE - round(ratio * pulse_range)

    # WAS
    # pwm.duty_ns(int(pulse * 1000))

    # NOW
    # Pulse in seconds divided by frequency in Hertz
    dutycycle_percent = (pulse / 1000) / 50

    # Scale duty cycle percentage into duty cycle range
    dutycycle = int(dutycycle_percent * DUTYCYCLE_RANGE)

    pwm.duty_u16(dutycycle)


def sweep(count=4):
    """
    Sweep servo horn left and right 'count' times.
    """

    left()  # Starting position
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
        idle()
        pwm.deinit()  # Disable PWM
        p.value(0)  # Ensure GPIO is Off
