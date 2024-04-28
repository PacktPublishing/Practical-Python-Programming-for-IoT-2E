"""
Scan addresses for devices connected to an I2C bus.

$ mpremote mount . run i2c_scan_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from machine import I2C, Pin

# Use color in terminal output for easier visual device identification.
# Set to False if your terminal output is garbled or has unwanted characters.
COLORISED_OUTPUT = True

# Print I2C initialisation code to terminal for found devices.
SHOW_CODE = True

# Test the following I2C Pins/Buses for connected devices.
I2Cs = [
  # [ID, SDA GPIO, SCL GPIO],
  [1, 2, 3],
  [0, 4, 5],
  [1, 6, 7],
  [0, 8, 9],
  [1, 10, 11],
  [0, 12, 13],
  [1, 14, 15],
  [1, 26, 27],
  [0, 20, 21],
  [1, 18, 19],
  [0, 16, 17]
]

def scan(): 
    """
    Scan for connected I2C devices.
    """

    for i2c in I2Cs:
        id, sda, scl = i2c
        dev = None

        try:
            print(f"\nID {id}  SDA Pin {sda}  SLC Pin {scl}:")

            dev = I2C(id, sda=Pin(sda), scl=Pin(scl))
            devices = dev.scan()
            
            if not len(devices):
                print("  Nothing detected")
            else:
                # Device(s) found.
                
                for device in devices: 
                    if COLORISED_OUTPUT:
                        print(f"\033[1m\033[32m  {hex(device)} {device}\033[0m {code(id, scl, sda)}")
                    else:
                        print(f"  {hex(device)} {device} {code(id, scl, sda)}")

        except ValueError as e:
            print("  ", e) 


def code(bus_id, scl, sda):
    """
    Generate I2C initialisation code example.
    """

    if SHOW_CODE:
        return f"  i2c = I2C({bus_id}, sda=Pin({sda}), scl=Pin({scl}))"
    else:
        return ""


scan()