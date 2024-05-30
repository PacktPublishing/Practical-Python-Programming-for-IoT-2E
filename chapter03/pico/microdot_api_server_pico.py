"""
chapter03/pico/microdot_api_server_pico.py

Microdot RESTFul API server example with Pico & MicroPython.

$ mpremote mount . run microdot_api_server_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from microdot import Microdot, send_file                                             # (1)
from microdot.utemplate import Template                                              # (2)
from picowifi import connect_wifi                                                    # (3)
from wifi_credentials import SSID, PASSWORD                                          # (4)
from machine import Pin, PWM                                                         # (5)

# Variables
LED_GPIO = 21                                                                        # (6)
state = {
    'level': 50 # % brightless of LED.
}

# Pin and PWM to control LED brightness.
p = Pin(LED_GPIO, Pin.OUT)                                                           # (7)
pwm = PWM(p)
pwm.freq(8000)

# Connect to WiFi and get Pico W's IP Address.
ip = connect_wifi(SSID, PASSWORD)                                                    # (8)


def set_led_brightness(level):                                                       # (9)
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
if not ip:                                                                           # (10)
    print(f"Unable to connect to network.")

else:
    # Initialise LED
    set_led_brightness(state['level'])                                               # (11)

    # Create Microdot server instance
    app = Microdot()                                                                 # (12)

    @app.route('/')                                                                  # (13)
    async def index(request):
        return Template('index_api_client.html').render(pin=LED_GPIO), {'Content-Type': 'text/html'}
    
    @app.route('/static/<path:path>')                                                # (14)
    async def static(request, path):
        if '..' in path:
            # Directory traversal is not allowed
            return 'Not found', 404
        return send_file('static/' + path, max_age=86400)    

    @app.get('/led')                                                                 # (15)
    async def led_get(request):
        return state

    @app.post('/led')                                                                # (16)
    async def led_post(request):
        level = int(request.json['level']) # Brightness 0-100%

        # If level is not within expected value range 0..100, return error
        if level < 0 or  level > 100:
            return "property 'level' expected to be between 0 and 100", 400

        # Update state and set LED brightness.
        state['level'] = level
        set_led_brightness(level)
        return state

    app.run(host=ip, debug=True)                                                     # (17)
