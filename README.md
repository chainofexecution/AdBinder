# AdBinder
DNS level ad blocking powered by CircuitPython running on cheap ESP32 hardware. 

A project by chainofexecution (Ian Moyer) and xtyphus (Jack LaRussa)

## Project Status
The hardware is mostly done and the software for this project is still being worked on.

We are using the FeatherS3 by Unexpected Maker as the main board and the Ethernet FeatherWing by Adafruit as the ethernet board.

## Hardware Configuration
Note: The three jumper wires tapped into the UART RX/TX and ground pins won't be needed to install the software or during device use as their purpose was to make development easier by having access to the ethernet board's UART (which isn't relayed through the USB serial converter for the main board)

![IMG_20221103_140926](https://user-images.githubusercontent.com/92492482/199806966-762089ed-1ca5-409c-9d2d-327c622a9b63.png)
![IMG_20221103_141326](https://user-images.githubusercontent.com/92492482/199807010-16542663-ea0d-4d36-8f72-13936ac61c66.png)
![IMG_20221103_141251](https://user-images.githubusercontent.com/92492482/199807037-323e2b89-eefa-4716-b6d3-47a61b755b59.png)
![IMG_20221103_141350](https://user-images.githubusercontent.com/92492482/199807045-18105884-3ab9-4a97-9af9-171e157baac8.png)
![IMG_20221103_141541](https://user-images.githubusercontent.com/92492482/199807053-a5771771-9f3b-4409-9ad3-4d350c31b24d.png)

## Software Status

So far the wifi access point is working and the configuration web page and server are partially operational. 

The next step of development is building the DNS server.
