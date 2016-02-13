# -*- coding: utf-8 -*-
#!/usr/bin/env python
import socket
import time
import binascii
from Message import *
'''
send_msg = covert2Hex(INSTRUCTION_DEVICE_RESET)
print send_msg
exit('bye')
'''
listenSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listenSock.bind(("", 6001))
listenSock.listen(15)

(newsock, address) = listenSock.accept()
newsock.setblocking(0)
print "ACCEPT a connection from ", address
client_ip = address[0]
client_port = address[1]


while 1:
	msg = raw_input(">")
	if(msg == "reset"):
		cmd = INSTRUCTION_DEVICE_RESET
	elif(msg == ""):
		continue
	try:
		newsock.send(covert2Hex(cmd))
		recv_buff = newsock.recv(1024)
		hex_msg = ' '.join(x.encode('hex') for x in recv_buff)
		print hex_msg
	except:
		continue
	


print recv_buff
for x in recv_buff:
	print x.encode("hex")

#print join(x.encode('hex') for x in recv_buff)
newsock.close()
print "bye"