"""
Pico W WiFi Helper.

Basic Usage:

    from picowifi import connect_wifi, disconnect_wifi

    ip = connect_wifi("mySSID", "myPassword")

    if ip:
        print("we're connected!")

    disconnectc_wifi()

API Document for MicroPython network module: https://docs.micropython.org/en/v1.22.0/library/network.WLAN.html
"""

from machine import Pin, Timer
from time import sleep

# Sanity check and friendly error message to confirm if firmware has network capabilities.
try:
    import network
except:
    assert False, "network module not found. A Pico W with Pico W MicroPython Firmware is expected."

# network.WLAN instance.
wlan = network.WLAN(network.STA_IF)

# Connection status LED.
led = Pin("LED") # LED = Onboard LED

# Timer for blinking status LED.
led_timer = Timer()


def status_to_text(status_code):
    """ Return a friendly name for a network status code """

    if status_code == network.STAT_IDLE:
        return "Idle" # no connection and no activity,
    elif status_code == network.STAT_CONNECTING:
        return "Connecting"
    elif status_code == network.STAT_WRONG_PASSWORD:
        return "Bad Password"
    elif status_code == network.STAT_NO_AP_FOUND:
        return "No Access Point for SSID Found"
    elif status_code == network.STAT_CONNECT_FAIL:
        return "Connection Failure" # Failed due to other problems
    elif status_code == network.STAT_GOT_IP:
        return "Connected"
    else:
        return f"Unknown Status Code {status_code}"


def set_led_connecting():
    """ Slowly blink LED while connecting. """

    led_timer.deinit()
    led_timer.init(period=1000, callback=lambda t: led.toggle())


def set_led_error():
    """ Rapidly blink LED if connecton fails. """

    led_timer.deinit()
    led_timer.init(period=200, callback=lambda t: led.toggle())


def set_led_off():
    """ Turn off LED. """

    led_timer.deinit()
    led.off()


def connect_wifi(ssid, password, pm=network.WLAN.PM_PERFORMANCE):
    """ 
      Connect Pico W to WiFi Network.
      
      parameter pm is the WiFi power management setting. One of:
        - network.WLAN.PM_PERFORMANCE (default)
        - network.WLAN.PM_POWERSAVE
        - network.WLAN.PM_NONE
        For more information see https://docs.micropython.org/en/v1.22.0/library/network.WLAN.html#constants

      Returns ip address or None if WiFi connection fails.
    """

    print(f"Connecting to SSID {ssid}", end="")
    
    set_led_connecting()

    wlan.active(True)
    wlan.connect(ssid, password)

    # Loop until Pico W is connected to network or fails.
    while wlan.status() == network.STAT_CONNECTING:
        print(".", end="")
        sleep(1)

    if wlan.status() == network.STAT_GOT_IP:
        # Connected to WiFi.

        set_led_off()

        status_text = status_to_text(wlan.status())
        ip_addr = wlan.ifconfig()[0]
        # subnet_addr = wlan.ifconfig()[1]
        # gateway_addr = wlan.ifconfig()[2]
        # dns_addr = wlan.ifconfig()[3]
        
        print(f"\n{status_text}. IP {ip_addr}")

        return ip_addr
    else:
        # Failed to connect to WiFi.

        set_led_error()

        print(f"\n{status_to_text(wlan.status())}")
        
        return None


def disconnect_wifi():
    """ Disconnect Pico W from WiFi. """

    if not wlan.isconnected():
        return

    print("Disconnecting WiFi", end="")

    wlan.disconnect()
    wlan.active(False)

    while wlan.status() != network.STAT_IDLE:
        print(".", end="")
        sleep(1)

    print(f"\nDisconnected.")


def is_connected_wifi():
    """ Test if Pico W is connected to WiFi. """
    return wlan.isconnected()
