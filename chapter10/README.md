# Practical Python Programming for IoT 2nd Edition

## Chapter 10 - Measuring Temperature, Humidity and Moisture

### Source Code

* `rpi` folder - Raspberry Pi Python Code

  * `requirements.txt` - Python dependencies required for this chapter
  * `dht_rpi.py` - Measure temperature and humidity with a DHT11 or DHT22 Sensor
  * `ldr_ads1115_rpi.py` - Detect light and dark with an LDR using an ADS1115 ADC
  * `ldr_ads1115_calibrate_rpi.py` - Calebrate LDR using an ADS1115 ADC
  * `ldr_calibration_config_rpi.py` - LDR calibration (will be overwritten by `ldr_ads1115_calibrate_rpi.py`)
  * `moisture_ads1115_rpi.py` - Detect moisture using an ADS1115 ADC
  * `moisture_ads1115_calibrate_rpi.py` - Calibrate moisture detection using an ADS1115 ADC
  * `moisture_calibration_config_rpi.py` - Moisture detection calibration (will be overwritten by `moisture_ads1115_calibrate_rpi.py`)

* `pico` folder - Pico MicroPython Code
  
  * `dht_pico.py` - Measure temperature and humidity with a DHT11 or DHT22 Sensor
  * `ADS1115_pico.py` - A simple module for reading analog input from an ADS1115 ADC
  * `i2c_scan_pico.py` - A utility to detect connected I2C devices
  * `ldr_ads1115_pico.py` - Detect light and dark with an LDR using an ADS1115 ADC
  * `ldr_calibrate_ads1115_pico.py` - Calebrate LDR using an ADS1115 ADC
  * `ldr_calibration_config_ads1115_pico.py` - LDR calibration (will be overwritten by `ldr_calibrate_ads1115_pico.py`)
  * `moisture_ads1115_pico.py` - Detect moisture using an ADS1115 ADC
  * `moisture_calibrate_ads1115_pico.py` - Calibrate moisture detection using an ADS1115 ADC
  * `moisture_calibration_config_ads1115_pico.py` - Moisture detection calibration (will be overwritten by `moisture_calibrate_ads1115_pico.py`)

* `pico\pico_adc` folder - Pico MicroPython Code

  * `ldr_pico.py` - Detect light and dark with an LDR using inbuilt Pico ADC
  * `ldr_calibrate_pico.py` - Calebrate LDR using inbuilt Pico ADC
  * `ldr_calibration_config_pico.py` - LDR calibration (will be overwritten by `ldr_calibrate_pico.py`)
  * `moisture_pico.py` - Detect moisture using inbuilt Pico ADC
  * `moisture_calibrate_pico.py` - Calibrate moisture detection using inbuilt Pico ADC
  * `moisture_calibration_config_pico.py` - Moisture detection calibration (will be overwritten by `moisture_calibrate_pico.py`)
  * `Pico ADC LDR Circuit.png` - Breadboard circuit for Pico ADC LDR
  * `Pico ADC Moisture Circuit.png` - Breadboard circuit for Pico ADC moisture detection

  
### Datasheets

None

### Post Publication Updates and Errata

None
