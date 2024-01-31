# Practical Python Programming for IoT 2nd Edition

## Chapter 10 - Measuring Temperature, Humidity and Moisture

### Source Code

* `rpi` folder - Raspberry Pi Python Code

  * `requirements.txt` - Python dependencies required for this chapter
  * `dht_rpi.py` - Measure temperature and humidity with a DHT11 or DHT22 Sensor
  * `ldr_ads1115_rpi.py` - Detect light and dark with an LDR
  * `ldr_ads1115_calibrate_rpi.py` - Calibration the LDR
  * `ldr_calibration_config_rpi.py` - LDR calibration (will be overwritten by `ldr_ads1115_calibrate_rpi.py`)
  * `moisture_ads1115_rpi.py` - Detect moisture
  * `moisture_ads1115_calibrate_rpi.py` - Calibrate moisture detection
  * `moisture_calibration_config_rpi.py` - Moisture detection calibration (will be overwritten by `moisture_ads1115_calibrate_rpi.py`)

* `pico` folder - Pico MicroPython Code

  * `dht_pico.py` - Measure temperature and humidity with a DHT11 or DHT22 Sensor
  * `ldr_pico.py` - Detect light and dark with an LDR
  * `ldr_calibrate_pico.py` - Calibration the LDR
  * `ldr_calibration_config_pico.py` - LDR calibration (will be overwritten by `ldr_calibrate_pico.py`)
  * `moisture_pico.py` - Detect moisture
  * `moisture_calibrate_pico.py` - Calibrate moisture detection
  * `moisture_calibration_config_pico.py` - Moisture detection calibration (will be overwritten by `moisture_calibrate_pico.py`)

### Datasheets

None

### Post Publication Updates and Errata

None
