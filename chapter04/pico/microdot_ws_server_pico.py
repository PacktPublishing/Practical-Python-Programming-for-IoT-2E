"""
chapter03/pico/microdot_ws_server_pico.py

Microdot Web Socket server example with Pico & MicroPython.

$ mpremote mount . run microdot_ws_server_pico.py

Built and tested with MicroPython Firmware 1.22.1 on Raspberry Pi Pico W
"""
from microdot import Microdot, send_file                                             # (1)
from microdot.utemplate import Template                                              # (2)
from microdot.websocket import with_websocket                                        # (3)
from picowifi import connect_wifi                                                    # (4)
from wifi_credentials import SSID, PASSWORD                                          # (5)
from machine import Pin, PWM                                                         # (6)

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


    # DEV
    @with_websocket
    async def echo(request, ws):
        while True:
            print(request)
            print(data)

            data = await ws.receive()
            await ws.send(data)
    # DEV


    @with_websocket
    async def handle_state(request, ws):
        """Handle 'led' messages to control the LED."""
        global state

        data = await ws.receive()
        print("Update LED from client {}: {} ".format(request.sid, data))

        if 'level' in data and data['level'].isdigit():                                  # (10)
            new_level = int(data['level']) # data comes in as str.

            # Range validation and bounding.
            if new_level < 0:                                                            # (11)
                new_level = 0
            elif new_level > 100:
                new_level = 100

        # Set PWM duty cycle to adjust brightness level.
        # We are mapping input value 0-100 to 0-1
        #Update to PiGPIO led.value = new_level / 100                                     # (12)
        print("LED brightness level is " + str(new_level))

        state['level'] = new_level

        # Broadcast new state to *every* connected connected (so they remain in sync).        
        await ws.send(state)                                                             # (13)
        #@TODO REMOVE emit("led", state, broadcast=True)




# # Socket Callback Handlers
# @socketio.on('connect')                                                              # (4)
# def handle_connect():
#     """Called when a remote web socket client connects to this server"""
#     logger.info("Client {} connected.".format(request.sid))                          # (5)

#     # Send initialising data to newly connected client.
#     emit("led", state)                                                               # (6)


# @socketio.on('disconnect')                                                           # (7)
# def handle_disconnect():
#     """Called with a client disconnects from this server"""
#     logger.info("Client {} disconnected.".format(request.sid))


# @socketio.on('led')                                                                  # (8)
# def handle_state(data):                                                              # (9)
#     """Handle 'led' messages to control the LED."""
#     global state
#     logger.info("Update LED from client {}: {} ".format(request.sid, data))

#     if 'level' in data and data['level'].isdigit():                                  # (10)
#         new_level = int(data['level']) # data comes in as str.

#         # Range validation and bounding.
#         if new_level < 0:                                                            # (11)
#             new_level = 0
#         elif new_level > 100:
#             new_level = 100

#         # Set PWM duty cycle to adjust brightness level.
#         # We are mapping input value 0-100 to 0-1
#         led.value = new_level / 100                                                  # (12)
#         logger.info("LED brightness level is " + str(new_level))

#         state['level'] = new_level

#     # Broadcast new state to *every* connected connected (so they remain in sync).
#     emit("led", state, broadcast=True)                                               # (13)






    # HTTP GET route for getting LED state.
    # This could alternativly be written as
    # @app.route('/led', methods=['GET'])
    @app.get('/led')                                                                 # (15)
    async def led_get(request):
        return state

    # HTTP POST route for setting LED state.
    # This could alternativly be written as
    # @app.route('/led', methods=['POST'])
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
