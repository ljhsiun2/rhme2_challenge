import serial
import sys
import hlextend

def print_output(ser_out):
	for line in ser_out:
		print line.rstrip()

sha = hlextend.new('sha1')
ser = serial.Serial('/dev/ttyUSB0', timeout=1, baudrate=19200)
print_output(ser.readlines())

for i in range(1, 255):
	msg = sha.extend(':passwd', 'cat.txt', i, '96103df3b928d9edc5a103d690639c94628824f5', raw=True)
	#print str(msg)
	guessed_token_hash = sha.hexdigest()
	print "key length: {}\t hash: {}\t msg: {}".format(i,guessed_token_hash,msg)
	ser.write("{}#{}\r\n".format(guessed_token_hash,msg))
	output = ser.readlines()
	print_output(output)