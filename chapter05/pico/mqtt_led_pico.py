"""
chapter05/pico/mqtt_led_pico.py

A full life-cycle Python + MQTT program to control an LED.

$ mpremote mount . run mqtt_led_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""

from picowifi import connect_wifi
from wifi_credentials import SSID, PASSWORD
from machine import Pin, PWM
from mqtt import robust as mqtt                                                                # (1)
import json                                                                                    # (2)

# Global Variables
LED_GPIO = 21
BROKER_HOST = "192.168.86.212"                                                                 # (X)  @FIXME NEED TO CHANGE.
BROKER_PORT = 1883
CLIENT_ID = "LEDClient-Pico"                                                                   # (3)
TOPIC = "led"                                                                                  # (4)
client = None  # MQTT client instance. See init_mqtt()                                         # (5)

# Pin and PWM to control LED brightness.
p = Pin(LED_GPIO, Pin.OUT)
pwm = PWM(p)
pwm.freq(8000)

# Connect to WiFi and get Pico W's IP Address.
ip = connect_wifi(SSID, PASSWORD)

def set_led_brightness(data):                                                                  # (6)
    """Set LED State to one of On, Blink or Off (Default)
      'data' expected to be a dictionary with the following format:
      {
          "level": a number between 0 and 100
      }
    """

    level = None # a number 0..100

    if "level" in data:
        level = data["level"]

        if isinstance(level, int) or isinstance(level, float) or level.isdigit():
            # State is a number
            level = max(0, min(100, int(level))) # Bound state to range 0..100

            # Use level as Duty Cycle % (0 - 100) and map into argument value for duty_u16 (0 - 65535)
            duty_cycle = int(65535 / 100 * level)
            pwm.duty_u16(duty_cycle) # Set LED brightness

            #@FIXME logger.info("LED at brightness {}%".format(level))
            print("LED at brightness {}%".format(level))

        else:
            #@FIXME  logger.info("Request for unknown LED level of '{}'. We'll turn it Off instead.".format(level))
            print("Request for unknown LED level of '{}'. We'll turn it Off instead.".format(level))
            pwm.duty_u16(0)  # 0% = Led off.

    else:
        # @FIXME logger.info("Message '{}' did not contain property 'level'.".format(data))
        print("Message '{}' did not contain property 'level'.".format(data))


def on_message(topic, msg):
    """Callback called when a message is received on a subscribed topic."""

    topic = topic.decode("UTF-8")                                                                    # (XX)
    msg = msg.decode("UTF-8")

    print("Received message for topic {}: {}".format(topic, msg))
    #FIXME use logger for pico.

    try:
        data = json.loads(msg)                                                               # (12)
        set_led_brightness(data)                                                                    # (XX)
    except ValueError as e:
        #FIXME logger.error("JSON Decode Error: " + msg) 
        print("JSON Decode Error: " + msg) 

  
def init_mqtt():
    """Initialise MQTT Client and Callbacks"""
    global client

    client = mqtt.MQTTClient(CLIENT_ID, BROKER_HOST)

    client.set_callback(on_message)
    client.connect()
    client.subscribe(TOPIC, qos=2)
    


# Configure Microdot routes and start server if we have a WiFi connection.
if not ip:
    print(f"Unable to connect to network.")

else:
    # Initialise MQTT
    init_mqtt()

    while True:
      try:
        client.check_msg()                                            # (XX)

        # if (time.time() - last_message) > message_interval:
        #   msg = b'Hello #%d' % counter
        #   client.publish(topic_pub, msg)
        #   last_message = time.time()
        #   counter += 1
      except OSError as e:
         print("Error:", e)
        # restart_and_reconnect()    