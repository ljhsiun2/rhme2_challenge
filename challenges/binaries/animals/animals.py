import serial
import sys


def print_output(ser_out):
	for line in ser_out:
		print line.rstrip()

ser = serial.Serial('/dev/ttyUSB0', timeout=1, baudrate=19200)
ser.write('ccccccccccccL\x01k\x03\r\n')
print_output(ser.readlines())