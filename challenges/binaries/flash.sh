#!/bin/sh
# easier script to flash devices

avrdude -c arduino -p atmega328p -P /dev/ttyUSB0 -b57600 -u -V -U flash:w:$1/$1.hex
