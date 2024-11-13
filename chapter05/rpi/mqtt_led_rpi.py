"""
chapter05/rpi/mqtt_led_rpi.py

A full life-cycle Python + MQTT program to control an LED.

Dependencies:
  pip3 install paho-mqtt pigpio

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import logging
import signal
import sys
import json
import pigpio
import paho.mqtt.client as mqtt                                               # (1)

# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger("main")          # Logger for this module
logger.setLevel(logging.INFO)               # Debugging for this file.

# Global Variables
LED_GPIO = 21
BROKER_HOST = "localhost"                                                     # (2)
BROKER_PORT = 1883
CLIENT_ID = "LEDClient-rPI"                                                   # (3)
TOPIC = "led"                                                                 # (4)
client = None  # MQTT client instance. See init_mqtt()                        # (5)

# Initialize GPIO
pi = pigpio.pi() 

# 8000 max hardware timed frequency by default pigpiod configuration.
pi.set_PWM_frequency(LED_GPIO, 8000)

# We set the range to 0..100 to mimic 0%..100%. This means
# calls to pi.set_PWM_dutycycle(GPIO_PIN, duty_cycle) now
# take a value in the range 0 to 100 as the duty_cycle
# parameter rather than the default range of 0..255.
pi.set_PWM_range(LED_GPIO, 100)

# Initialise LED brightness. Our PWM range is 0..100,
# therefore our brightness level % maps directly.
pi.set_PWM_dutycycle(LED_GPIO, 0) # Start with 0 dutycycle (LED off)


"""
GPIO Related Functions
"""

def set_led_brightness(data):                                                 # (6)
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
            pi.set_PWM_dutycycle(LED_GPIO, level)
            logger.info("LED at brightness {}%".format(level))

        else:
            logger.info("Request for unknown LED level of '{}'. We'll turn it Off instead.".format(level))
            pi.set_PWM_dutycycle(LED_GPIO, 0) # 0% = Led off.
    else:
        logger.info("Message '{}' did not contain property 'level'.".format(data))


"""
MQTT Related Functions and Callbacks
"""
def on_connect(client, userdata, flags, reason_code, properties):             # (7)
    """on_connect is called when our program connects to the MQTT Broker.
       Always subscribe to topics in an on_connect() callback.
       This way if a connection is lost, the automatic
       re-connection will also results in the re-subscription occurring."""

    if reason_code == 0:                                                      # (8)
        # 0 = successful connection
        logger.info("Connected to MQTT Broker")
    else:
        # connack_string() gives us a user friendly string for a connection code.
        logger.error("Failed to connect to MQTT Broker: " + mqtt.connack_string(reason_code))

    # Subscribe to the topic for LED level changes.
    client.subscribe(TOPIC, qos=2)                                            # (9)



def on_disconnect(client, userdata, flags, reason_code, properties):          # (10)
    """Called disconnects from MQTT Broker."""
    logger.error("Disconnected from MQTT Broker: " + mqtt.connack_string(reason_code))



def on_message(client, userdata, msg):                                        # (11)
    """Callback called when a message is received on a subscribed topic."""
    logger.info("Received message for topic {}: {}".format(msg.topic, msg.payload))

    try:                                                  
        data = json.loads(msg.payload.decode("UTF-8"))                        # (12)

        if msg.topic == TOPIC:                                                # (13)
            set_led_brightness(data)                                          # (14)
        else:
            logger.error("Unhandled message topic {} with payload " + str(msg.topic, msg.payload))

    except json.JSONDecodeError as e:
        logger.error("JSON Decode Error: " + msg.payload.decode("UTF-8"))


def signal_handler(sig, frame):
    """Capture Control+C and disconnect from Broker."""
    global led_state

    logger.info("You pressed Control + C. Shutting down, please wait...")

    client.disconnect() # Graceful disconnection.
    pi.set_PWM_dutycycle(LED_GPIO, 0) # 0% = Led off.
    sys.exit(0)



def init_mqtt():
    """Initialise MQTT Client and Callbacks"""
    global client

    # Our MQTT Client. See PAHO documentation for all configurable options.
    # "clean_session=True" means we don"t want Broker to retain QoS 1 and 2 messages
    # for us when we"re offline. You"ll see the "{"session present": 0}" logged when
    # connected.
    client = mqtt.Client(                                                     # (15)
        callback_api_version=mqtt.CallbackAPIVersion.VERSION2,
        client_id=CLIENT_ID,
        clean_session=False)

    # Route Paho logging to Python logging.
    client.enable_logger()                                                    # (16)

    # Setup callbacks
    client.on_connect = on_connect                                            # (17)
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect to Broker.
    client.connect(BROKER_HOST, BROKER_PORT)                                  # (18)


# Initialise MQTT
init_mqtt()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)  # Capture Control + C       # (19)
    logger.info("Listening for messages on topic '" + TOPIC + "'. Press Control + C to exit.")

    client.loop_start()                                                       # (20)
    signal.pause()
