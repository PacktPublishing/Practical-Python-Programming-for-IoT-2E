"""
chapter11/pico/motor_class_pico.py

Using a Pico & MicroPython to control a L293D acting as a H-Bridge to control a DC Motor.

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from machine import Pin, PWM
from time import sleep

class Motor:

    def __init__(self, enable_gpio, logic_1_gpio, logic_2_gpio):

          self.enable_gpio = enable_gpio
          self.logic_1_gpio = logic_1_gpio
          self.logic_2_gpio = logic_2_gpio

          self.enable_pwm = PWM(Pin(enable_gpio))
          self.logic_1_pin = Pin(logic_1_gpio)
          self.logic_2_pin = Pin(logic_2_gpio)

          # MicroPython's PWM does not have the concept of a range,                # (1)
          # so we will manually handle the range (motor speed %)
          # in the methods below using the _speed_to_dutycycle()
          # helper function.

	      # Set default state - motor not spinning and set for forward direction.
          self.set_speed(0)                                                        # (2)
          self.right()


    def right(self, speed=None):                                                   # (3)
        """
        Spin motor right.
        """
        if speed is not None:
            self.set_speed(speed)

        self.logic_1_pin.low()
        self.logic_2_pin.high()


    def left(self, speed=None):                                                    # (4)
        """
        Spin motor left.
        """
        if speed is not None:
            self.set_speed(speed)

        self.logic_1_pin.high()
        self.logic_2_pin.low()

        
    def is_right(self):                                                            # (5)
        """
        Is motor set to spin right?
        """
        
        return (not self.logic_1_pin.value == 0  # LOW
              and self.logic_1_pin.value == 1)   # HIGH

    def set_speed(self, speed):                                                    # (6)
        """
        Set motor speed using PWM.
        """
        assert 0 <= speed <= 100

        duty_cycle = _speed_to_dutycycle(speed)
        self.enable_pwm.duty_u16(duty_cycle)


    def brake(self):                                                               # (7)
        """
        Motor Brake (Using L293D).
        """
        was_right = self.is_right() # To restore direction after braking
        
        self.set_speed(100)
        
        self.logic_1_pin.low()
        self.logic_2_pin.low()

        self.set_speed(0)

        # Restore motor direction
        if was_right:
            self.right()
        else:
            self.left()


    def brake_pwm(self, brake_speed=100, delay_millisecs=50):                      # (8)
        """
        Motor Brake (Alternative using Reverse PWM).
        You may need to adjust brake_speed and delay_millisecs
        based on your physical motor and voltage/current usage.
        """
        was_right = None # To restore direction after braking

        if self.is_right():      
            self.left(brake_speed)
            was_right = True
        else:
            self.right(brake_speed)
            was_right = False

        sleep(delay_millisecs / 1000)
        self.set_speed(0)

        # Restore motor direction
        if was_right:
            self.right()
        else:
            self.left()


def _speed_to_dutycycle(speed):
    """
    Helper function to convert a speed in the range 0..100
    to a machine.PWM dutycycle.
    """

    if speed < 0:
        speed = 0
    elif speed > 100:
        speed = 100

    # 65535 is the max value for pwm.duty_u16()
    duty_cycle = int(65535 / 100 * speed)

    return duty_cycle
