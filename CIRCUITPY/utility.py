# For CircuitPython v7.3.x+ only!
# AdBinder an ESP32 CircuitPython implementation of DNS level ad blocking.
# Authors: Ian Moyer (chainofexecution), Jack LaRussa (xtyphus)
# License: GPU General Public License v3.0

import time

null = ''

def banner(footer):
    print('''\n
                       ██        █████ ██                          ██
     █████             ██    ██████  ███    █                      ██
    █  ███             ██   ██   █  █ ██   ███                     ██
       ███             ██  █    █  █  ██    █                      ██
      █  ██            ██      █  █   █                            ██           ███  ████
      █  ██        ███ ██     ██ ██  █    ███    ███  ████     ███ ██     ███    ████ ████ █
     █    ██      █████████   ██ ██ █      ███    ████ ████ █ █████████  █ ███    ██   ████
     █    ██     ██   ████    ██ ███        ██     ██   ████ ██   ████  █   ███   ██
    █      ██    ██    ██     ██ ██ ███     ██     ██    ██  ██    ██  ██    ███  ██
    █████████    ██    ██     ██ ██   ███   ██     ██    ██  ██    ██  ████████   ██
   █        ██   ██    ██     █  ██     ██  ██     ██    ██  ██    ██  ███████    ██
   █        ██   ██    ██        █      ██  ██     ██    ██  ██    ██  ██         ██
  █████      ██  ██    ██    ████     ███   ██     ██    ██  ██    ██  ████    █  ███
 █   ████    ██ █ █████     █  ████████     ███ █  ███   ███  █████     ███████    ███
█     ██      ██   ███     █     ████        ███    ███   ███  ███       █████
█                          █
 █                          █
  ██                         ██                                                          \n\n''' + footer)

def debug(msg):
    print('[DEBUG] ' + msg)

def log(origin, msg):
    print('[' + origin.upper() + '] ' + msg)
