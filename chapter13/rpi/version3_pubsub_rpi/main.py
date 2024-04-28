"""
chapter13/rpi/version3_pubsub_rpi/main.py

Publisher-Subscriber example with Raspberry Pi & Python.

Dependencies:
  pip3 install pigpio PyPubSub adafruit-circuitpython-ads1x15

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import adafruit_ads1x15.ads1115 as ADS
import pigpio

from signal import pause
import logging
from pubsub import pub

# Our custom classes
from Button import Button
from Pot import Pot
from LED import LED

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Main")

pi = pigpio.pi()

# Button GPIO
BUTTON_GPIO = 16

# Button state (eg PRESSED, RELEASED, HOLD)
button_state = None


def on_button_message(sender, name, state, topic=pub.AUTO_TOPIC):
    """ Handles button messages
        Parameters:
          'sender' is a reference to the Button instance that invoked the callback (ie the button variable created below)
          'name' is the string name we gave the the button
          'state' is the button state, eg PRESSED, RELEASED, HOLD
          'topic' contains topic information. Use topic.getName() to get the topic name"""

    global led_index, button_state

    button_state = state

    if state == Button.PRESSED:
        led_index += 1

        if led_index >= len(LED_TOPICS):
            led_index = 0

        logger.info("Turning the Potentiometer dial will change the rate for LED with topic {}".format(LED_TOPICS[led_index]))

    elif button_state == Button.HOLD:

        logger.info("Changing rate for all LEDs to {}".format(last_rate))
        pub.sendMessage(LED.TOPIC_ALL_LEDS, rate=last_rate)


button = Button(gpio=BUTTON_GPIO,
                pi=pi,
                name="MyButton")


# Potentiometer / ADC settings (for POT Class)
POT_CHANNEL = ADS.P0      # P0 maps to output A1 on ADS1115
POT_POLL_SECS = 0.05      # How often will we poll the ADC for value changes?
MIN_BLINK_RATE_SECS = 0.1 # Minimum value returnable by POT class
MAX_BLINK_RATE_SECS = 5   # Maximum value returnable by POT class


def on_pot_message(sender, name, value, topic=pub.AUTO_TOPIC):
    """ Handles Potentiometer messages
        Parameters:
          'sender' is a reference to the POT instance that invoked the callback (ie the pot variable created below)
          'name' is the string name we gave the the Potentiometer
          'value' is the Potentiometer current value
          'topic' contains topic information. Use topic.getName() to get the topic name"""

    global last_rate

    last_rate = value

    led_topic = LED_TOPICS[led_index]

    logger.info("Changing LED #{} rate to {} using the topic {}".format(led_index, last_rate, led_topic))

    pub.sendMessage(led_topic, rate=last_rate) # Set individual LED.



# Create Pot class instances.
pot = Pot(analog_channel=POT_CHANNEL,
         min_value=MIN_BLINK_RATE_SECS,
         max_value=MAX_BLINK_RATE_SECS,
         poll_secs=POT_POLL_SECS,
         name="MyPOT")


# Last rate/value from Potentiometer/ADC.
last_rate = pot.get_value()

# Create LED class instances.
led1 = LED(gpio=20, pi=pi, name="MyLED")
led2 = LED(gpio=21, pi=pi, name="MyOtherLED")


# Topic names to communicate with individual LEDs.
LED_TOPICS = [
    led1.topic, # == "LED.MyLED"
    led2.topic  # == "LED.MyOtherLED"
]

# The index of the LED in LEDS which will
# be affected when the potentiometer value changes.
led_index = 0


# Subscribe to POT and BUTTON messages using the on_message_* methods.
pub.subscribe(on_button_message, button.topic)
pub.subscribe(on_pot_message, pot.topic)

if __name__ == "__main__":

    try:
        logger.info("Version 3 - Raspberry Pi & Python - Publisher-Subscriber Example. Press Control + C To Exit.")

        # Initialise all LED's
        pub.sendMessage(LED.TOPIC_ALL_LEDS, rate=last_rate)

        logger.info("Turning the Potentiometer dial will change the rate for LED with topic {}".format(LED_TOPICS[led_index]))
        pause()

    except KeyboardInterrupt:
        pub.sendMessage(LED.TOPIC_ALL_LEDS, rate=0) # All LED's Off.
        pi.stop()
