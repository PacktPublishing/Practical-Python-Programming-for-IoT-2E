"""
chapter11/rpi/servo_rpi.py

Using a Raspberry Pi & Python to control a servo.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
from time import sleep
import pigpio

SERVO_GPIO = 21

# Pulse widths for extreme left/right and center positions in microseconds.
# The default values are 'typical' values for a hobby servo.
# Be gradual when changing the left and right adjustments
# because a servo can be damaged if rotated beyond its limits.
RIGHT_PULSE   = 1000  # Smaller values for 'more' right             # (1)
LEFT_PULSE    = 2000  # Higher values for 'more' left
#CENTER_PULSE = 1500  # or calculate as below
CENTER_PULSE = ((LEFT_PULSE - RIGHT_PULSE) // 2) + RIGHT_PULSE

# Delay to give servo time to move
MOVEMENT_DELAY_SECS = 0.5                                           # (2)

pi = pigpio.pi()
pi.set_mode(SERVO_GPIO, pigpio.OUTPUT)

def left():                                                         # (3)
    """
    Rotate servo to full left position.
    """
    pi.set_servo_pulsewidth(SERVO_GPIO, LEFT_PULSE)
    
    
def center():
     """
     Center the servo.
     """
     pi.set_servo_pulsewidth(SERVO_GPIO, CENTER_PULSE)


def right():
    """
    Rotate servo to full right position.
    """
    pi.set_servo_pulsewidth(SERVO_GPIO, RIGHT_PULSE)


def idle():                                                         # (4)
    """
    Idle servo (zero pulse width).
    Servo will be rotatable by hand with little force.
    """
    pi.set_servo_pulsewidth(SERVO_GPIO, 0)


def angle(to_angle):                                                # (5)
    """
    Rotate servo to specified angle (between -90 and +90 degrees)
    """

    # Restrict to -90..+90 degrees
    to_angle = int(min(max(to_angle, -90), 90))

    ratio = (to_angle + 90) / 180.0                                 # (6)
    pulse_range = LEFT_PULSE - RIGHT_PULSE
    pulse = LEFT_PULSE - round(ratio * pulse_range)                 # (7)

    pi.set_servo_pulsewidth(SERVO_GPIO, pulse)


def sweep(count=4):                                                 # (8)
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
        print("Centering")
        center()
        sleep(1)

        print("Sweeping left and right")
        sweep()
        sleep(1)
        
        print("Centering")
        center()
        sleep(1)

    finally:
        idle() # Idle servo.
        pi.stop() # PiGPIO Cleanup
