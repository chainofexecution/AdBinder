# For CircuitPython v8.0.0-beta3+ only!
# AdBinder an ESP32 CircuitPython implementation of DNS level ad blocking.
# Authors: Ian Moyer (chainofexecution), Jack LaRussa (xtyphus)
# License: GPU General Public License v3.0

import time
import board
import busio
import digitalio # Pull
import analogio # AnalogIn
import io
import socketpool
import ipaddress
import wifi
import neopixel
import adafruit_requests # as requests
import ampule
from utility import banner, debug, log
from adafruit_wsgi.wsgi_app import WSGIApp
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_dns as dns
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
import adafruit_wiznet5k.adafruit_wiznet5k_wsgiserver as server

cs = digitalio.DigitalInOut(board.D10)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
mac_eth = b"\xFE\xED\xDE\xAD\xBE\xEF"
ssid = "AdBinder"
psk = "default1"
http_port = 80
version = '0.1'
footer = 'AdBinder v' + version + ' - A DNS based ad blocker for FeatherS3 and Adafruit Ethernet FeatherWing, open source, and written in CircuitPython.\n'
wsgi_config = io.open("www/config.html", "rt").read()

banner(footer)
#Setup Ethernet Interface
phy_w = WIZNET5K(spi, cs, mac=mac_eth, debug=True) # debug should = False for releases
debug('Ethernet interface has been setup.')
# Setup Wireless Interface
ifconfig = ipaddress.ip_address(phy_w.pretty_ip(phy_w.ifconfig[0])), ipaddress.ip_address(phy_w.pretty_ip(phy_w.ifconfig[1])), ipaddress.ip_address(phy_w.pretty_ip(phy_w.ifconfig[2])), ipaddress.ip_address(phy_w.pretty_ip(phy_w.ifconfig[3]))
# Start wifi station
wifi.radio.start_station()
# Set station interface config to match the ethernet interface
wifi.radio.set_ipv4_address(ipv4=ifconfig[0], netmask=ifconfig[1], gateway=ifconfig[2], ipv4_dns=ifconfig[3])
debug('Wireless interface has been setup.')
# Start wifi access point
wifi.radio.start_ap(ssid, psk, max_connections=1)
debug(f'AP SSID is \'{ssid}\' and the password is \'{psk}\'')
wlan = socketpool.SocketPool(wifi.radio)
print(wifi.radio.ipv4_address_ap)
debug(f'Starting Ampule HTTP server on port {http_port}.')

@ampule.route("/")
def light_set(request):
    log('AMPULE', 'HTTP GET request recieved. Sent \'www/config.html\' in response.')
    return (200, {}, wsgi_config)
# Setup socket for Amplue WSGI server
http_socket = wlan.socket()
http_socket.bind(['0.0.0.0', http_port])
http_socket.listen(1)

while True:
  ampule.listen(http_socket)
