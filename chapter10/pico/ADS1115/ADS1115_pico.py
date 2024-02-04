"""
A simple module for reading analog input from an ADS1115 ADC.

This module was created and tested for the following configuration:

    - ADS1115 ADC Module
    - 3.4.0; MicroPython v1.22.1 on 2024-01-05
    - Raspberry Pi Pico / Pico W

Example Usage:
    import utime
    from machine import I2C, Pin
    
    CHANNEL = 0 # ADS1115 A0
    BUS_ID = 0
    SCL_GPIO = 17
    SDA_GPIO = 16

    i2c = I2C(BUS_ID, scl=Pin(SCL_GPIO), sda=Pin(SDA_GPIO))
    ads = ADS1115(i2c)

    while True:
        reading = ads.read(CHANNEL)
        print(reading)
        utime.sleep(0.5)
"""
import utime
from machine import I2C, Pin

"""
With gain of 4.096 and max raw value of 32767,
for a 3v3 reference the max expected raw
value from the ADC will be: 
32767 / 4.096 * 3.3 = ~26400
"""
VOLTAGE_REF = 4.096 # ADC default gain.
MAX_VALUE = 32767   # Max raw value based on gain for single ended mode ADC.

class ADS1115:
    """
    A simple interface for an ADS1115 ADC 
    for reading an analog channel.

    Parameters:
    
      i2c:  An machine.I2C instance.
      addr: Optional ADS1115 address. 
            If None, first address on I2C instance bus is used.
    """

    def __init__(self, i2c, addr=None):
        """
        Create ADS1115 Instance.

        Parameters:
            i2c:  Initialised I2C instance
            addr: ADS1115 I2C Address (0x48 (default), 0x49, 0x4A, 0x4B)
        """

        self.i2c = i2c

        # Check that there is a device connected to I2C
        devices = self.i2c.scan()

        if len(devices) == 0:
            raise ValueError("No I2C Devices Detected")

        if not addr:
            # Auto assign (and assume ADS1115 is connected)
            self.address = devices[0]
        else:
            self.address = addr
    
        if self.address < 0x48 or self.address > 0x4B:
            raise ValueError(f"Invalid ADS1115 Address {hex(self.address)}")

        elif devices[0] != self.address:
            raise ValueError(f"Found I2C Device with address {hex(devices[0])}, but expecting {hex(self.address)}")

 
    def read_config(self):
        self.i2c.writeto(self.address, bytearray([1]))
        result = self.i2c.readfrom(self.address, 2)
        return result[0] << 8 | result[1]
    

    def read(self, channel):
        """
        Read ADC Value and Voltage.

        Parameter:
          channel: Channel 0, 1, 2 or 3.

        Returns:
            dict with raw value and voltage.
        """
        assert channel >= 0 and channel <= 4, f"Invalid channel {channel}"

        self.i2c.writeto(self.address, bytearray([0]))
        result = self.i2c.readfrom(self.address, 2)
        config = self.read_config()
        config &= ~(7 << 12) & ~(7 << 9)
        config |= (channel + 4 << 12) | (1 << 9) | (1 << 15)
        config = [int(config >> i & 0xff) for i in (8, 0)]
        self.i2c.writeto(self.address, bytearray([1] + config))

        value = result[0] << 8 | result[1]
        volts = value / MAX_VALUE * VOLTAGE_REF 

        return {
            "value": value,
            "volts": round(volts, 2)
        }


