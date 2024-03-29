"""
chapter11/rpi/stepper_rpi.py

Using a Raspberry Pi & Python to control a bipolar stepper motor.

Dependencies:
  pip3 install pigpio

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
from time import sleep
import pigpio

pi = pigpio.pi()

CHANNEL_1_ENABLE_GPIO = 5                                           # (1)
CHANNEL_2_ENABLE_GPIO = 16

INPUT_1A_GPIO = 6   # Blue Coil 1 Connected to 1Y                   # (2)
INPUT_2A_GPIO = 13  # Pink Coil 2  Connected to 2Y
INPUT_3A_GPIO = 20  # Yellow Coil 3 Connected to 3Y
INPUT_4A_GPIO = 21  # Orange Coil 4 Connected to 4Y

# Coil GPIOs as a list.
coil_gpios = [                                                      # (3)
    INPUT_1A_GPIO,
    INPUT_2A_GPIO,
    INPUT_3A_GPIO,
    INPUT_4A_GPIO
]

# Initialise each coil GPIO as OUTPUT.
for gpio in coil_gpios:                                             # (4)
    pi.set_mode(gpio, pigpio.OUTPUT)


def off():
    """
    Turn all coil off.
    """
    for gpio in coil_gpios:                                         # (5)
        pi.write(gpio, pigpio.HIGH)  # Coil off

off()  # All coils off

# Enable Channels (always high)
pi.set_mode(CHANNEL_1_ENABLE_GPIO, pigpio.OUTPUT)                   # (6)
pi.write(CHANNEL_1_ENABLE_GPIO, pigpio.HIGH)
pi.set_mode(CHANNEL_2_ENABLE_GPIO, pigpio.OUTPUT)
pi.write(CHANNEL_2_ENABLE_GPIO, pigpio.HIGH)


COIL_HALF_SEQUENCE = [                                              # (7)
    [0, 1, 1, 1],
    [0, 0, 1, 1],   # (a)
    [1, 0, 1, 1],
    [1, 0, 0, 1],   # (b)
    [1, 1, 0, 1],
    [1, 1, 0, 0],   # (c)
    [1, 1, 1, 0],
    [0, 1, 1, 0]    # (d)
]


COIL_FULL_SEQUENCE = [
    [0, 0, 1, 1],   # (a)
    [1, 0, 0, 1],   # (b)
    [1, 1, 0, 0],   # (c)
    [0, 1, 1, 0]    # (d)
]

# For rotate() to keep track of the sequence row it is on.
sequence_row = 0


def rotate(steps, sequence=COIL_HALF_SEQUENCE, delay_ms=0.2):        # (8)
    """ 
    Rotate number of steps
    use -steps to rotate in reverse
    """
    assert delay_ms > 0
    assert sequence == COIL_HALF_SEQUENCE or sequence == COIL_FULL_SEQUENCE

    global sequence_row
    
    direction = +1

    if steps < 0:
        direction = -1

    for step in range(abs(steps)):                                  # (9)

      coil_states = sequence[sequence_row]                          # (10)

      for i in range(len(sequence[sequence_row])):

          gpio = coil_gpios[i]                                      # (11)
          state = sequence[sequence_row][i] # 0 or 1                # (12)
          pi.write(gpio, state)                                     # (13)

          sleep(delay_ms / 1000)

      sequence_row += direction                                     # (14)

      if sequence_row < 0:
          sequence_row = len(sequence) - 1
      elif sequence_row >= len(sequence):
          sequence_row = 0


if __name__ == '__main__':

    try:                                                            # (15)
        # Delay in milliseconds between coil steps.
        # Too low a value and motor will not step or will step erratically.
        STEP_DELAY_MS = 0.5

        # Faster rotation speed, lower step resolution.
        print("2048 steps for 360 degree rotation using sequence COIL_FULL_SEQUENCE.")
        rotate(2048, COIL_FULL_SEQUENCE, STEP_DELAY_MS)  # Rotate one direction
        rotate(-2048, COIL_FULL_SEQUENCE, STEP_DELAY_MS) # Rotate reverse direction

        # Slower rotation speed, higher step resolution.
        print("4096 steps for 360 degree rotation using sequence COIL_HALF_SEQUENCE.")
        rotate(4096, COIL_HALF_SEQUENCE, STEP_DELAY_MS)  # Rotate one direction
        rotate(-4096, COIL_HALF_SEQUENCE, STEP_DELAY_MS) # Rotate reverse direction
 
    finally:
        off()  # Turn stepper coils off
        pi.stop()  # PiGPIO Cleanup
