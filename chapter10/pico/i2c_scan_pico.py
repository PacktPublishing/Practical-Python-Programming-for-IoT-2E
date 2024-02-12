"""
Scan addresses for devices connected to an I2C bus.

$ mpremote mount . run i2c_scan_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from machine import I2C, Pin

# I2C Device is connected to the following Pico GPIOs:
BUS_ID = 0
SDA = 16
SCL = 17
 
dev = I2C(BUS_ID, scl=Pin(SCL), sda=Pin(SDA))
devices = dev.scan()

if not len(devices):
  print("No I2C devices detected") 
else:    
  for device in devices: print(f"  {hex(device)}")
