"""
chapter03/pico/server_pico.py

Microdot RESTFul API example with Pico & MicroPython.

$ mpremote mount . run server_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from picowifi import connect_wifi
from microdot import Microdot, Response
from microdot.utemplate import Template
from wifi_credentials import SSID, PASSWORD

LED_GPIO_PIN = 21

# Connect to WiFi and get Pico W's IP Address.
ip = connect_wifi(SSID, PASSWORD)

if not ip:
    print(f"Unable to connect to network.")

else:
    # Start Microdot API Server
    app = Microdot()

    @app.route('/')
    async def index(request):
        return Template('index_api_client.html').render(pin=LED_GPIO_PIN), {'Content-Type': 'text/html'}

    app.run(host=ip, debug=True)
