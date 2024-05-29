"""
chapter03/pico/microdot_api_server_pico.py

Microdot RESTFul API server example with Pico & MicroPython.

$ mpremote mount . run microdot_api_server_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from picowifi import connect_wifi
from microdot import Microdot, Response, send_file
from microdot.utemplate import Template
from wifi_credentials import SSID, PASSWORD
from machine import Pin, PWM

LED_GPIO_PIN = 21
state = {
    'level': 50 # % brightless of LED.
}

# Pin and PWM to control LED brightness.
p = Pin(LED_GPIO_PIN, Pin.OUT)
pwm = PWM(p)
pwm.freq(8000)

# Connect to WiFi and get Pico W's IP Address.
ip = connect_wifi(SSID, PASSWORD)

"""
GPIO Related Functions
"""
def set_led_brightness(level):
    """ Set LED brightness 0 - 100% """

    if level < 0:
        level = 0
    elif level > 100:
       level = 100

    # Use level as Duty Cycle % (0 - 100) and map into a argument value for duty_u16 (0 - 65535)
    duty_cycle = int(65535 / 100 * level)
    pwm.duty_u16(duty_cycle) # Set LED brightness


if not ip:
    print(f"Unable to connect to network.")

else:
    # Initialise LED
    set_led_brightness(state['level'])

    # Start Microdot API Server
    app = Microdot()

    @app.route('/')
    async def index(request):
        return Template('index_api_client.html').render(pin=LED_GPIO_PIN), {'Content-Type': 'text/html'}
    
    @app.route('/static/<path:path>')
    async def static(request, path):
        if '..' in path:
            # Directory traversal is not allowed
            return 'Not found', 404
        return send_file('static/' + path, max_age=86400)    

    @app.get('/led')
    async def led_get(request):
        return state

    @app.post('/led')
    async def led_post(request):
        level = int(request.json['level']) # Brightness 0-100%
        state['level'] = level
        set_led_brightness(level)
        return state

    app.run(host=ip, debug=True)
