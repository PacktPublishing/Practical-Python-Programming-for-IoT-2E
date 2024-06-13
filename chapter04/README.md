# Practical Python Programming for IoT 2nd Edition

## Chapter 4 - Networking with Web Sockets

* `breadboard_layout.fzz` - Fritzing breadboard layouts circuits for Raspberry Pi &amp; Pico
* `breadboard_layout.png` - Breadboard layouts circuits for Raspberry Pi &amp; Pico

* `rpi` folder - Raspberry Pi Python Code

  * `requirements.txt` - Python dependencies required for this chapter
  * `flask_ws_server_rpi.py` - Web Sockets Server to control a LED
  * `templates/index_ws_client.html` - Web client for `flask_ws_server_rpi.py`
  * `static/jquery.min.js` - JQuery JavaScript library for the web client
  * `static/socket.io.js` - Socket.io JavaScript library for `index_ws_client.html`

* `pico` folder - Pico MicroPython Code

  * `microdot_api_server_pico.py` - RESTful API Server to control a LED
  * `static/index_ws_client.html` - Web client for `microdot_api_server_pico.py`
  * `static/jquery.min.js` - JQuery JavaScript library for the web client
  * `picowifi.py` - Helper code for connecting Pico W to Wireless network
  * `wifi_credentials.example.py` - example WiFi credentials file
  * `microdot` - this folder contains the Microdot library and dependencies

### Datasheets

None

### Post Publication Updates and Errata

None

### Breadboard Layouts

![Breadboard Layouts](./breadboard_layout.png)
