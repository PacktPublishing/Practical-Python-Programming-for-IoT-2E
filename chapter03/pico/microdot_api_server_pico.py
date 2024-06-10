"""
chapter03/pico/microdot_api_server_pico.py

Microdot RESTFul API server example with Pico & MicroPython.

$ mpremote mount . run microdot_api_server_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from microdot import Microdot, send_file                                             # (1)
from picowifi import connect_wifi                                                    # (2)
from wifi_credentials import SSID, PASSWORD                                          # (3)
from machine import Pin, PWM                                                         # (4)

# Variables
LED_GPIO = 21                                                                        # (5)
state = {
    'level': 50, # 0..100 % brightless of LED.
    'gpio': LED_GPIO
}

# Pin and PWM to control LED brightness.
p = Pin(LED_GPIO, Pin.OUT)                                                           # (6)
pwm = PWM(p)
pwm.freq(8000)

# Connect to WiFi and get Pico W's IP Address.
ip = connect_wifi(SSID, PASSWORD)                                                    # (7)


def set_led_brightness(level):                                                       # (8)
    """ Set LED brightness 0 - 100% """

    # Ensure level is within expected value range 0..100
    if level < 0:
        level = 0
    elif level > 100:
       level = 100

    # Use level as Duty Cycle % (0 - 100) and map into argument value for duty_u16 (0 - 65535)
    duty_cycle = int(65535 / 100 * level)
    pwm.duty_u16(duty_cycle) # Set LED brightness


# Configure Microdot routes and start server if we have a WiFi connection.
if not ip:                                                                           # (9)
    print(f"Unable to connect to network.")

else:
    # Initialise LED
    set_led_brightness(state['level'])                                               # (10)

    # Create Microdot server instance
    app = Microdot()                                                                 # (11)

    # HTTP GET default route.
    # This could alternativly be written as @app.route('/', methods=['GET'])
    @app.get('/')                                                                    # (12)
    async def index(request):
        return send_file('static/index_api_client.html')
    
    # HTTP GET route for serving static content.
    # This could alternativly be written as
    # @app.route('/static/<path:path>', methods=['GET'])
    @app.get('/static/<path:path>')                                                  # (13)
    async def static(request, path):
        if '..' in path:
            # Directory traversal is not allowed
            return 'Not found', 404
        return send_file('static/' + path, max_age=86400)

    # HTTP GET route for getting LED state and GPIO.
    # This could alternativly be written as
    # @app.route('/led', methods=['GET'])
    @app.get('/led')                                                                 # (14)
    async def led_get(request):
        return state

    # HTTP POST route for setting LED state.
    # This could alternativly be written as
    # @app.route('/led', methods=['POST'])
    @app.post('/led')                                                                # (15)
    async def led_post(request):

        # Check that level exists in request json parameter
        if not 'level' in request.json:
            return "property 'level' expected, and must be between 0 and 100", 400

        level = int(request.json['level']) # Brightness 0-100%

        # If level is not within expected value range 0..100, return error
        if level < 0 or  level > 100:
            return "property 'level' expected, and must be between 0 and 100", 400

        # Update state and set LED brightness.
        state['level'] = level
        set_led_brightness(level)
        return state

    app.run(host=ip, debug=True)                                                     # (16)
