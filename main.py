import network
import socket
import time
import io

with io.open('www/config.html', 'r', encoding="utf-8") as f:
    config_html = f.read()
# """<!DOCTYPE html>
# <html>
#     <head> <title>ESP8266 Test</title> </head>
#     <body> <h1>ESP8266 Test Site!</h1>
#     </body>
# </html>
# """

http_response_header='HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
ssid = 'AdBinder'
psk = 'default1'

WPA2_PSK = 3 # Authmode for WLAN IF
print(config_html)
network.phy_mode(network.MODE_11N)
wlan = network.WLAN(network.AP_IF)
wlan.active(True)
wlan.ifconfig(('192.168.0.1', '255.255.255.0', '192.168.0.1', '192.168.0.1'))
wlan.config(essid=ssid, password=psk, authmode=WPA2_PSK, channel=11)
print(f'Broadcasting as AP IF on SSID \'{ssid}\' with PSK \'{psk}\'')

while True:
  time.sleep(2)
  print('')
  while wlan.isconnected(): # Wait for STA to connect to AP
    print('Connection to STA was established')
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    print('Listening for HTTP traffic on port 80')
    while True:
        s.listen(1)
        conn,addr = s.accept()
        print(f'Sending response to STA over port 80')
        conn.send(http_response_header)
        conn.send(config_html)
        conn.close()
