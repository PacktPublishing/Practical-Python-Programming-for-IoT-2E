"""
chapter03/pico/microdot_ws_server_pico.py

Microdot Web Socket server example with Pico & MicroPython.

$ mpremote mount . run microdot_ws_server_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from microdot import Microdot, send_file                                             # (1)
from microdot.utemplate import Template                                              # (2)
from microdot.websocket import with_websocket, WebSocketError                        # (3)
from picowifi import connect_wifi                                                    # (4)
from wifi_credentials import SSID, PASSWORD                                          # (5)
from machine import Pin, PWM                                                         # (6)
from json import loads, dumps                                                               # (X)

# Variables
LED_GPIO = 21                                                                        # (X)
state = {
    'level': 50 # % brightless of LED.
}

# Pin and PWM to control LED brightness.
p = Pin(LED_GPIO, Pin.OUT)                                                           # (X)
pwm = PWM(p)
pwm.freq(8000)

# Connect to WiFi and get Pico W's IP Address.
ip = connect_wifi(SSID, PASSWORD)                                                    # (X)


def set_led_brightness(level):                                                       # (X)
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

    # HTTP GET default route.
    # This could alternativly be written as @app.route('/', methods=['GET'])
    @app.get('/')                                                                    # (13)
    async def index(request):
        return Template('index_ws_client.html').render(gpio=LED_GPIO), {'Content-Type': 'text/html'}
    
    # HTTP GET route for serving static content.
    # This could alternativly be written as
    # @app.route('/static/<path:path>', methods=['GET'])
    @app.get('/static/<path:path>')                                                  # (14)
    async def static(request, path):
        if '..' in path:
            # Directory traversal is not allowed
            return 'Not found', 404
        return send_file('static/' + path, max_age=86400)


    # Dictionary of connected clients so we can broadcast data to all clients.
    websocket_clients = {}  # (host,port), web socket object.
    

    @app.route('/led')
    @with_websocket
    async def client_connection(request, ws):
        """
          Handle messages to control the LED.
          This method is called once for each new client connection.
        """

        # New client connection, store client and websocket.
        websocket_clients[request.client_addr] = ws
        print("Client connected", request.client_addr)

        while True:                                                                          # (X)
            try: 
                message_str = await ws.receive()
            except WebSocketError as ex:
                # Assume client has disconnected and break from while loop.
                # print("Error", ex)
                break

            # Handle client message.
            await handle_client_message(request, ws, message_str)

        # We are now out of while True loop and can assume
        # that client has disconnected.
        print("Client disconnected:", request.client_addr)
        del websocket_clients[request.client_addr]


    async def broadcast_message(payload):
        """
        Broadcast payload to every connected client.
        """

        payload_str = dumps(payload) # dictionary to string

        for addr, socket in websocket_clients.items():
            try:
                client_host = addr[0]
                client_port = addr[1]                
                print("Broadcasting {} to client {}:{}".format(payload_str, client_host, client_port))

                await socket.send(payload_str)                                            # (13)
            except WebSocketError as ex:
                print("Sending error", ex)

    
    async def handle_client_message(request, ws, message_str):
        """
        Handle new message from a connected client.
        """
        global state

        client_host = request.client_addr[0]
        client_port = request.client_addr[1]

        # Convert JSON string data into a dictionary.
        data  = loads(message_str)

        # Update LED Brightless if data includes 'level'
        if 'level' in data:                                                            # (10)
            print("Message {} from client {}:{}".format(message_str, client_host, client_port))

            new_level = data['level']

            # Range validation and bounding.
            if new_level < 0:                                                            # (11)
                new_level = 0
            elif new_level > 100:
                new_level = 100

            # Set PWM duty cycle to adjust brightness level.
            # We are mapping input value 0-100 to 0-1
            #Update to PiGPIO led.value = new_level / 100                               # (12)
            print("LED brightness level is " + str(new_level))

            state['level'] = new_level

            # Broadcast new state to *every* connected connected (so they remain in sync).
            await broadcast_message(state)
        
        else:
            # no 'level' in data, so just send back current level to current client
            payload_str = dumps(state) # dictionary to string
            print("Sending {} to client {}:{}".format(payload_str, client_host, client_port))
            await ws.send(payload_str)

    app.run(host=ip, debug=True)                                                     # (17)
