"""
chapter03/rpi/flask_api_server.py

Flask-RESTFul API Server example with Raspberry Pi & Python.

Dependencies:
  pip3 install pigpio flask flask-restful

Built and tested with Python 3.11.22 on Raspberry Pi 5
"""
import logging
from flask import Flask, request, render_template                                    # (1)
from flask_restful import Resource, Api, reqparse, inputs                            # (2)
import pigpio                                                                        # (3)


# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main')  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.


# Global variables
LED_GPIO = 21
state = {                                                                            # (4)
    'level': 50, # 0..100 % brightless of LED.
    'gpio': LED_GPIO
}

pi = pigpio.pi()                                                                     # (5)

# 8000 max hardware timed frequency by default pigpiod configuration.
pi.set_PWM_frequency(LED_GPIO, 8000)                                                 # (6)

# We set the range to 0..100 to mimic 0%..100%. This means
# calls to pi.set_PWM_dutycycle(GPIO_PIN, duty_cycle) now
# take a value in the range 0 to 100 as the duty_cycle
# parameter rather than the default range of 0..255.
pi.set_PWM_range(LED_GPIO, 100)                                                      # (7)

# Initialise LED brightness. Our PWM range is 0..100,
# therefore our brightness level % maps directly.
pi.set_PWM_dutycycle(LED_GPIO, state['level'])                                       # (8)

# Flask & Flask-RESTful instance variables
app = Flask(__name__) # Core Flask app.                                              # (9)
api = Api(app) # Flask-RESTful extension wrapper                                     # (10)


"""
Flask & Flask-Restful Related Functions
"""

# @app.route applies to the core Flask instance (app).
# Here we are serving a simple web page.
@app.route('/', methods=['GET'])                                                     # (11)
def index():
    """Make sure inde.html is in the templates folder
    relative to this Python file."""
    return render_template('index_api_client.html', state=state)                     # (12)


# Flask-restful resource definitions.
# A 'resource' is modeled as a Python Class.
class LEDControl(Resource):                                                          # (13)

    def __init__(self):
        self.args_parser = reqparse.RequestParser()                                  # (14)

        self.args_parser.add_argument(
            name='level',  # Name of argument
            required=True, # Mandatory argument
            type=inputs.int_range(0, 100),  # Allowed range 0..100                   # (15)
            help='Set LED brightness level {error_msg}',
            default=None)


    def get(self):
        """ Handles HTTP GET requests to return current LED state."""
        return state                                                                 # (16)


    def post(self):
        """Handles HTTP POST requests to set LED brightness level."""
        global state                                                                 # (17)

        args = self.args_parser.parse_args()                                         # (18)

        # Set PWM duty cycle to adjust brightness level.
        state['level'] = args.level                                                  # (19)
        pi.set_PWM_dutycycle(LED_GPIO, state['level'])                               # (20)
        logger.info("LED brightness level is " + str(state['level']))

        return state                                                                 # (21)


# Register Flask-RESTful resource and mount to server end point /led
api.add_resource(LEDControl, '/led')                                                 # (22)


if __name__ == '__main__':

    # If you have debug=True and receive the error "OSError: [Errno 8] Exec format error", then:
    # remove the execuition bit on this file from a Terminal, ie:
    # chmod -x flask_api_server.py
    #
    # Flask GitHub Issue: https://github.com/pallets/flask/issues/3189

    app.run(host="0.0.0.0", debug=True)                                              # (23)
