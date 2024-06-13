"""
chapter04/pico/microdot_ws_server_pico.py

Microdot Web Socket server example with Pico & MicroPython.

$ mpremote mount . run microdot_ws_server_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from microdot import Microdot, send_file
from microdot.websocket import with_websocket, WebSocketError                        # (1)
from picowifi import connect_wifi
from wifi_credentials import SSID, PASSWORD
from machine import Pin, PWM
from json import loads, dumps                                                        # (2)

# Variables
LED_GPIO = 21
state = {
    'level': 50, # % brightless of LED.
    'gpio': LED_GPIO
}

# Pin and PWM to control LED brightness.
p = Pin(LED_GPIO, Pin.OUT)
pwm = PWM(p)
pwm.freq(8000)

# Connect to WiFi and get Pico W's IP Address.
ip = connect_wifi(SSID, PASSWORD)


def set_led_brightness(level):
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
if not ip:
    print(f"Unable to connect to network.")

else:
    # Initialise LED
    set_led_brightness(state['level'])

    # Create Microdot server instance
    app = Microdot()

    """
    RESTFul Routes
    """

    # HTTP GET route for serving static content.
    # This could alternativly be written as
    # @app.route('/static/<path:path>', methods=['GET'])
    @app.get('/static/<path:path>')
    async def static(request, path):
        if '..' in path:
            # Directory traversal is not allowed
            return 'Not found', 404
        return send_file('static/' + path)
    

    # HTTP GET route to return a static version of the web page.
    # This could alternativly be written as @app.route('/', methods=['GET'])
    @app.get('/')
    async def index(request):
        return send_file('static/index_ws_client_static.html')


    """
    Web Sockets (using the Microdot Web Socket Extension)
    """

    # Dictionary of connected clients so we can broadcast data to all clients.
    websocket_clients = {}  # (host,port), web socket object.                        # (3)

    # Web Socket entry point defined at /.
    # In Web Page (JavaScript) we connect to the Web Socket using:
    #   const socket = new WebSocket('ws://' + location.host + '/state')
    @app.route('/state')                                                             # (4)
    @with_websocket                                                                  # (5)
    async def client_connection(request, websocket):                                 # (6)
        """
          Handle messages to control the LED.
          This method is called once for each new client connection.
        """

        # New client connection, store client and websocket so we can broadcast
        # to all connected clients later on.
        websocket_clients[request.client_addr] = websocket                           # (7)
        print("Client connected", request.client_addr)

        # On connection, send current LED brightness and GPIO to client.
        payload_str = dumps(state) # dictionary to JSON string                       # (8)
        await websocket.send(payload_str)                                            # (9)

        while True:                                                                  # (10)
            try: 
                message_str = await websocket.receive()                              # (11)
            except WebSocketError as ex:
                # Assume client has disconnected and break from while loop.
                # print("WebSocketError (receive)", ex)
                break                                                                # (12)

            # Handle Web Socket client message.
            await handle_message(request, websocket, message_str)                    # (13)

        # We are now out of while True loop and can assume
        # that client has disconnected.
        print("Client disconnected:", request.client_addr)
        del websocket_clients[request.client_addr]                                   # (14)

   
    async def handle_message(request, websocket, message_str):                       # (15)
        """
        Handle new message from a connected client.
        """
        global state

        # Convert JSON string data into a Dictionary.
        data  = loads(message_str)                                                   # (16)

        # Update LED Brightness if data includes 'level'
        if 'level' in data:                                                          # (17)
            client_host = request.client_addr[0]
            client_port = request.client_addr[1]
            print("Message {} from client {}:{}".format(message_str, client_host, client_port))

            new_level = data['level']

            # Range validation and bounding.
            if new_level < 0:
                new_level = 0
            elif new_level > 100:
                new_level = 100

            print("LED brightness level is " + str(new_level))

            # Store brightness in memory.
            state['level'] = new_level

            # Set brightness of physical LED.
            set_led_brightness(new_level)

            # Broadcast new state to every other connected client.
            await broadcast_message(state, websocket)                                # (18)


    async def broadcast_message(message, excludeWebsocket = None):                   # (19)
        """
        Broadcast payload to every connected Web Socket client
        except 'excludeWebsocket'
        """

        message_str = dumps(message) # dictionary to JSON string

        # Loop through each connected Web Socket client and send payload.
        for addr, websocket in websocket_clients.items():                            # (20)

            if websocket == excludeWebsocket:                                        # (21)
                # Not sending to 'excludeWebsocket'. We can use excludeWebsocket
                # to prevent sending data back to the originating Web Socket
                # client during a broadcast.
                continue

            try:
                client_host = addr[0]
                client_port = addr[1]                
                print("Broadcasting {} to client {}:{}".format(message_str, client_host, client_port))

                await websocket.send(message_str)                                    # (22)
            except WebSocketError as ex:
                print("WebSocketError (send)", ex)            


    app.run(host=ip, debug=True)
