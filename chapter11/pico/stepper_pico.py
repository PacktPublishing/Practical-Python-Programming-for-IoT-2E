"""
chapter11/pico/stepper_pico.py

Using a Pico & MicroPython to control a bipolar stepper motor.

$ mpremote mount . run stepper_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from time import sleep_us
from machine import Pin

CHANNEL_1_ENABLE_GPIO = 5                                           # (1)
CHANNEL_2_ENABLE_GPIO = 16

INPUT_1A_GPIO = 6   # Blue Coil 1 Connected to 1Y                   # (2)
INPUT_2A_GPIO = 13  # Pink Coil 2  Connected to 2Y
INPUT_3A_GPIO = 20  # Yellow Coil 3 Connected to 3Y
INPUT_4A_GPIO = 21  # Orange Coil 4 Connected to 4Y

# Coil GPIOs Pins as a list.                                        # (3)
# and initialise each coil GPIO Pins as OUTPUT.                     # (4)
coil_gpios_pins = [                             
    Pin(INPUT_1A_GPIO, mode=Pin.OUT),
    Pin(INPUT_2A_GPIO, mode=Pin.OUT),
    Pin(INPUT_3A_GPIO, mode=Pin.OUT),
    Pin(INPUT_4A_GPIO, mode=Pin.OUT)
]

def off():
    """
    Turn all coil off.
    """
    for pin in coil_gpios_pins:                                     # (5)
        pin.high() # Coil off

off()  # All coils off


# Enable Channels (always high)                                     # (6)
channel_1_enable_pin = Pin(CHANNEL_1_ENABLE_GPIO, mode=Pin.OUT, value=1)
channel_2_enable_pin = Pin(CHANNEL_2_ENABLE_GPIO, mode=Pin.OUT, value=1)


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

    global sequence_row

    direction = +1

    if steps < 0:
        direction = -1

    for step in range(abs(steps)):                                  # (9)

      coil_states = sequence[sequence_row]                          # (10)

      for i in range(len(sequence[sequence_row])):

          pin = coil_gpios_pins[i]                                  # (11)
          state = sequence[sequence_row][i] # 0 or 1                # (12)
          pin.value(state)                                          # (13)

          # sleep_ms() cannot take a float (and therefore a fraction of a millisecond)
          # so using sleep_us() and converting milliseconds to microseconds.
          sleep_us(int(delay_ms * 1000))

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
