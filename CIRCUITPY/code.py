# For CircuitPython v8.0.0-beta3+ only!
# AdBinder an ESP32 CircuitPython implementation of DNS level ad blocking.
# Authors: Ian Moyer (chainofexecution), Jack LaRussa (xtyphus)
# License: GPU General Public License v3.0

import time
import sys
import board
import busio
import digitalio # Pull
import analogio # AnalogIn
import io
import asyncio
import socketpool
import ipaddress
import wifi
import neopixel
import adafruit_requests # as requests
import ampule
from utility import banner, debug, log
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
import adafruit_wiznet5k.adafruit_wiznet5k_dns as dns
import adafruit_wiznet5k.adafruit_wiznet5k_socket as socket
import adafruit_wiznet5k.adafruit_wiznet5k_wsgiserver as server

# Helper to detect uasyncio v3
#IS_UASYNCIO_V3 = hasattr(asyncio, "__version__") and asyncio.__version__ >= (3,)

cs = digitalio.DigitalInOut(board.D10)
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
mac_eth = b"\xFE\xED\xDE\xAD\xBE\xEF"
dns_forward_ip = '9.9.9.9'
ssid = "AdBinder"
psk = "default1"
http_port = 80
version = '0.1'
footer = 'AdBinder v' + version + ' - A DNS based ad blocker for FeatherS3 and Adafruit Ethernet FeatherWing, open source, and written in CircuitPython.\n'
wsgi_config = io.open("www/config.html", "rt").read()

class DNSQuery:
    def __init__(self, data):
        self.data = data
        self.domain = ''
        tipo = (data[2] >> 3) & 15  # Opcode bits
        if tipo == 0:  # Standard query
            ini = 12
            lon = data[ini]
            while lon != 0:
                self.domain += data[ini + 1:ini + lon + 1].decode('utf-8') + '.'
                ini += lon + 1
                lon = data[ini]
        print("DNSQuery domain:" + self.domain)

    def response(self, ip):
        print("DNSQuery response: {} ==> {}".format(self.domain, ip))
        if self.domain:
            packet = self.data[:2] + b'\x81\x80'
            packet += self.data[4:6] + self.data[4:6] + b'\x00\x00\x00\x00'  # Questions and Answers Counts
            packet += self.data[12:]  # Original Domain Name Question
            packet += b'\xC0\x0C'  # Pointer to domain name
            packet += b'\x00\x01\x00\x01\x00\x00\x00\x3C\x00\x04'  # Response type, ttl and resource data length -> 4 bytes
            packet += bytes(map(int, ip.split('.')))  # 4bytes of IP
        # print(packet)
        return packet


banner(footer)
#Setup Ethernet Interface
phy_e = WIZNET5K(spi, cs, mac=mac_eth, debug=True) # debug should = False for releases
phy_w = wifi.radio
debug('Ethernet interface has been setup.')
# Setup Wireless Interface
# ifconfig = ipaddress.ip_address(phy_e.pretty_ip(phy_e.ifconfig[0])), ipaddress.ip_address(phy_e.pretty_ip(phy_e.ifconfig[1])), ipaddress.ip_address(phy_e.pretty_ip(phy_e.ifconfig[2])), ipaddress.ip_address(phy_e.pretty_ip(phy_e.ifconfig[3]))
# Start wifi station
phy_w.start_station()
# Set station interface config to match the ethernet interface
# phy_w.set_ipv4_address(ipv4=ifconfig[0], netmask=ifconfig[1], gateway=ifconfig[2], ipv4_dns=ifconfig[3])
debug('Wireless interface has been setup.')
# Start wifi access point
phy_w.start_ap(ssid, psk, max_connections=1)
debug(f'AP SSID is \'{ssid}\' and the password is \'{psk}\'')
wlan = socketpool.SocketPool(phy_w)


print(phy_w.ipv4_address_ap)
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


# socket.set_interface(phy_e)
# udps = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# # udps.setblocking(False)
# udps.bind(('0.0.0.0', 53))
# udps.listen(1)
# # else:
# #     yield asyncio.IORead(udps)
# data, addr = udps.recvfrom(4096)
# print("Incoming DNS request...")
#
# DNS = DNSQuery(data)
# udps.sendto(DNS.response(dns_forward_ip), addr)

# print("Replying: {:s} -> {:s}".format(DNS.domain, dns_forward_ip))
#
# while True:
#     try:
#         # else:
#         #     yield asyncio.IORead(udps)
#         data, addr = udps.recvfrom(4096)
#         print("Incoming DNS request...")
#
#         DNS = DNSQuery(data)
#         udps.sendto(DNS.response(dns_forward_ip), addr)
#
#         print("Replying: {:s} -> {:s}".format(DNS.domain, dns_forward_ip))
#
#     except Exception as e:
#         print("DNS server error:", e)
#         time.sleep(3)

udps.close()
