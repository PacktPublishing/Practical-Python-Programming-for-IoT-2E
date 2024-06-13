"""
File: chapter04/flask_ws_server.py

A Flask based Web Sockets server to control an LED built using Flask-SocketIO.

Dependencies:
  pip3 install pigpio flask flask-socketio

Built and tested with Python 3.7 on Raspberry Pi 4 Model B
"""
import logging
from flask import Flask, request, render_template
from flask_socketio import SocketIO, send, emit                                     # (1)
import pigpio


# Initialize Logging
logging.basicConfig(level=logging.WARNING)  # Global logging configuration
logger = logging.getLogger('main')  # Logger for this module
logger.setLevel(logging.INFO) # Debugging for this file.


# Flask & Flask Restful Global Variables.
app = Flask(__name__) # Core Flask app.
socketio = SocketIO(app) # Flask-SocketIO extension wrapper.                         # (2)


# Global variables
LED_GPIO = 21
led = None # PWMLED Instance. See init_led()
state = {
    'level': 50, # 0..100 % brightless of LED.
    'gpio': LED_GPIO
}

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
pi.set_PWM_dutycycle(LED_GPIO, state['level'])


"""
Flask & Flask-SocketIO Related Functions
"""

# @app.route apply to the raw Flask instance.
# Here we are serving a simple web page.
@app.route('/', methods=['GET'])
def index():
    """Make sure index_ws_client.html is in the templates folder
    relative to this Python file."""
    return render_template('index_ws_client.html')


# Flask-SocketIO Callback Handlers
@socketio.on('connect')                                                              # (4)
def handle_connect():
    """Called when a remote web socket client connects to this server"""
    logger.info("Client {} connected.".format(request.sid))                          # (5)

    # Send initializing data to newly connected client.
    emit("state", state)                                                             # (6)


@socketio.on('disconnect')                                                           # (7)
def handle_disconnect():
    """Called with a client disconnects from this server"""
    logger.info("Client {} disconnected.".format(request.sid))


@socketio.on('state')                                                                # (8)
def handle_state(data):                                                              # (9)
    """Handle 'led' messages to control the LED."""
    global state
    logger.info("Update LED from client {}: {} ".format(request.sid, data))

    if 'level' in data and data['level'].isdigit():                                  # (10)
        new_level = int(data['level']) # data comes in as str.

        # Range validation and bounding.
        if new_level < 0:                                                            # (11)
            new_level = 0
        elif new_level > 100:
            new_level = 100
       
        # Set PWM duty cycle to adjust brightness level.
        state['level'] = new_level
        pi.set_PWM_dutycycle(LED_GPIO, state['level'])
        logger.info("LED brightness level is " + str(state['level']))


    # Broadcast new state to *every* connected (so they remain in sync).
    emit("state", state, broadcast=True)                                             # (13)


if __name__ == '__main__':
    # If you have debug=True and receive the error "OSError: [Errno 8] Exec format error", then:
    # remove the execuition bit on this file from a Terminal, ie:
    # chmod -x flask_ws_server.py
    #
    # Flask GitHub Issue: https://github.com/pallets/flask/issues/3189

    socketio.run(app, host='0.0.0.0', debug=True)                                    # (14)
