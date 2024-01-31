"""
File: chapter10/rpi/dht_measure_pico.py

Using MicroPython & Pico to measure temperature with a DHT11 or DHT22 Sensor.

$ mpremote mount . run dht_measure_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""

# dht is a MicroPython inbuilt library.
from dht import DHT11, DHT22               # (1)
from machine import Pin

SENSOR_GPIO = 21
sensor = DHT11(Pin(SENSOR_GPIO))           # (2)
#sensor = DHT22(Pin(SENSOR_GPIO))

try:
    # Ask sensor to capture a measurement.
    sensor.measure()                       # (3)

    temperature_c  = sensor.temperature()
    temperature_f = temperature_c * (9/5) + 32.0
    humidity_pc = sensor.humidity()

    print(f"Temperature: {temperature_c:.2f} C")
    print(f"Temperature: {temperature_f:.2f} F")
    print(f"Humidity: {humidity_pc:.2f} F")

    # There is no equivalent for taking    # (4)
    # multiple samples using the inbuilt
    # MicroPython DHT Library. However
    # you could achieve this manually 
    # using a for loop and take the
    # average of multiple measurements.

except OSError as e:
    print(f"Failure while trying to read DHT Sensor on GPIO {SENSOR_GPIO}")