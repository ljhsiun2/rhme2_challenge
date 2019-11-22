# https://crypto.stackexchange.com/questions/9896/how-does-rsa-signature-verification-work
# s^e = pad(hash(M)) mod N
# pad = pkcs1_v1_5
# hash = sha1
# https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Security_and_practical_considerations
# No messages are involved, only signatures, so I want to forge a signature (see stackexchange link for forging)
# The only attack that lets me recover the key WITHOUT an oscilloscope or chipwhisperer is the weak RNG one
# so lets pray to god it works

# https://www.dlitz.net/software/pycrypto/api/2.6/Crypto.Signature.PKCS1_v1_5-module.html

"""
Common factor with Bob and Gary is 
12740687396952811643088941494602600474970968740910907077064852670904845297490889090\
164936902229457369083527167233513652960298164731764863857925799725451573
FLAG:Eucl1d_h4ck3d_crypt0_b3fore_it_was_c00l!!
"""
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Util.number import inverse
import serial
import fractions

pub_keys = {'Alice': '00c90e4c65c0a96080df5aaf73caaf1146afb364cb37894f6bb745182191bf577a2777d8b5dbf57b2ad9f902e2\
d3abadfe6ebeb7366d7b11f0cbfd4371dbadf5f548e60644b3365a654b8efe2de32bbb1cc0288d367c0e8cf9ac\
8a2544cb067f677c87e82362e3b3ce950d072c5b1baffd650a31db4ff7d7209f0aec0178d7ba8b',
			'Bob': '00db87e4a4774c4c4606faadeb58460d6c62282aced115ae9d256d6ca2d32b49615c9257869aa0b1757b8faaae\
401f94474ddbf5f54b75dfaa7bef370cc9842a920ff9484cabacece44e7c2c80c2c97775a39d035c59475db933\
74cbac0d0e4f0830bcc51fe4680ef1d8afce89d61ef7a1fe8f03dd26a7049303f1cbfa94b10323',
			'Carl': '00a8e4fe8ddca1a4b8c97376d90e43e78f9df822412215511fa3efc3f96b34c6bdc2090dbbfce2e118ff8168c6\
ba1ed965f743238467310c97d22918c4549d9c426641469a57ed75557367ad37d3c73485a5d748bbcea211897f\
72f60e7fbd6bb220e6e56e466dcc3144abb78388865ee5c9bba879ea96c0a2522bdb63383f3591',
			'David': '00b7a2434673e546ff4d7975166a5228e19aa5b43ab79e147f27695aeeeb197bb3152ef1df0b8190a7304b4db4\
9cffdf6f0cdd168f47594d2fd0672787716ae519bf78df1cb96c0968785e7f0ec7de1008644b3cc32c74748f0d\
0967cdc76b7bba0cb78a15858bcc40063e53c34bb47cf63ba2eb8af3d491131f2aa96388802677',
			'Edward': '00b7882ac1f039ce5c9cef7a66800d2247c465cd5bcbaa80cc48ba34ec2759280a666432f78f53d222a308ea2d\
c7d455be7d050faeca3fd9847fb43dbaf2a09013778e238b7a79430271c105cb959f3ff4d0e72a756ecc948bc2\
7e1b1dc7dafb3fae6e31c2571c89f06ac854cac98d10e106ec89abd4d093f28e13db54ea8798b3',
			'Fleur': '00cec274724b04bda96d51162abf710fbf1eedb978aa87639e61a166b772cf4bdfc8fdddb3b700b366d68767a5\
d33cce4e6146fe325de5d9d0dc480dbd4201c3859d1debbf952a1e3a10c0cfeb6413f740748c7a43a346d895c1\
2bf7b14068df33be376b12527b1c7fb390f95d0f878ebb8a38c621eb415a85bf42b9cbcaccc749',
			'Gary': '00bdb08ad1d97628b0d4e9bdcdb0303007e66b9d82b3ca3e7df476911f1d0ffd81f67487b4fafc4e252b30c501\
055335ab74f1e92e411615b5263d5117daf715740f826a6f8faba2620ddda2852a3595aa9f051d3e0b46766440\
360f986cc2db7b7f2d9431e9324280109ac1ed43900a57531ee2878e895c6f5b4ba4311051413d'}

for key1 in pub_keys:
	for key2 in pub_keys:
		if key1 != key2:
			gcd = fractions.gcd(int(pub_keys[key1], 16), int(pub_keys[key2], 16))
			#print "Common factor with {} and {} is {}".format(key1, key2, str(gcd))

n = int(pub_keys['Bob'], 16)
p = 12740687396952811643088941494602600474970968740910907077064852670904845297490889090164936902229457369083527167233513652960298164731764863857925799725451573
q = n/p
totient = (q-1)*(p-1)
e = 65537

assert(fractions.gcd(e, totient) == 1) # 65537 is default e for like everything, but just in case

d = inverse(e, totient)

message = 'admin'
RSAkey = RSA.construct((n, long(e), d))
h = SHA.new(message)
signer = PKCS1_v1_5.new(RSAkey)
signature = signer.sign(h)

print signature.encode('hex')

ser = serial.Serial('/dev/ttyUSB0', timeout=2, baudrate=19200)

ser.write('2\r')
ser.readlines()
ser.write(signature.encode('hex') + '\r')
print ser.readlines()