"""
chapter10/rpi/dht_rpi.py

Using a Raspberry Pi & Python to measure temperature with a DHT11 or DHT22 Sensor.

Dependencies:
  pip3 install pigpio pigpio-dht

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
from pigpio_dht import DHT11, DHT22          # (1)

SENSOR_GPIO = 21
sensor = DHT11(SENSOR_GPIO)                  # (2)
#sensor = DHT22(SENSOR_GPIO)

if __name__ == '__main__':

    result = sensor.read(retries=2)          # (3)
    print(result)

    result = sensor.sample(samples=5)        # (4)
    print(result)

