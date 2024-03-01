"""
chapter11/rpi/motor_rpi.py

Using a Raspberry Pi & Python to control a L293D acting as a H-Bridge to control a DC Motor.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import pigpio                                                   # (1)
from time import sleep
from motor_class_rpi import Motor

# Motor A
CHANNEL_1_ENABLE_GPIO = 5                                       # (2)
INPUT_1Y_GPIO = 6 
INPUT_2Y_GPIO = 13

# Motor B
CHANNEL_2_ENABLE_GPIO = 16                                      # (3)
INPUT_3Y_GPIO = 20
INPUT_4Y_GPIO = 21

pi = pigpio.pi()                                                # (4)
motor_A = Motor(pi, CHANNEL_1_ENABLE_GPIO, INPUT_1Y_GPIO, INPUT_2Y_GPIO)
motor_B = Motor(pi, CHANNEL_2_ENABLE_GPIO, INPUT_3Y_GPIO, INPUT_4Y_GPIO)


if __name__ == '__main__':
    try:
        # Make the motors move

        print("Motor A and B Speed 100, Right")
        motor_A.set_speed(100)                                   # (5)
        motor_A.right()
        motor_B.set_speed(100)    
        motor_B.right()
        sleep(4)

        print("Motor B Stop")
        motor_B.set_speed(0)
        sleep(4)

        print("Motor B Speed 100, Left")
        motor_B.left()
        motor_B.set_speed(100)
        sleep(4)

        print("Motor A Classic Brake, Motor B PWM Brake")
        motor_A.brake()                                         # (6)
        motor_B.brake_pwm()
        sleep(4)

    finally:
        motor_A.set_speed(0)                                               
        motor_B.set_speed(0)                                               
        pi.stop()
