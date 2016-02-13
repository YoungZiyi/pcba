#!/usr/bin/env python 
from socket import *
import string
from struct import pack, unpack
import signal
from Message import *
import binascii
import time

setdefaulttimeout(3)

exit_flag = False
def signal_handler(signum, frame):
	global exit_flag
	exit_flag = True
	print "receive a signal %d, exit_flag = %d"%(signum, is_exit)
signal.signal(signal.SIGINT, signal_handler)

BUFSIZ = 16
ADDR = (SERVER_HOST, SERVER_PORT) 

print "Connecting..."
tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)


print "Recving..."
recved = tcpCliSock.recv(BUFSIZ)
print "Recv ", recved.strip()
	

'''
data = raw_input('> ')
if not data:
	print "No data to send"
	exit(-1)
'''
data = "10.0.0.100"
ip_in_str = inet_aton(data)
ip_in_int = unpack("!I", ip_in_str)[0];
ip_in_binary_str = pack("!i",ip_in_int)

msg = ip_in_binary_str + binascii.unhexlify(RemoveBlankInMiddle(EVENT_AVAILABLE))
print "Msg is ", binascii.hexlify(msg)
tcpCliSock.send(msg)

time.sleep(1)
msg = ip_in_binary_str + binascii.unhexlify(RemoveBlankInMiddle(EVENT_GETITEM_FINISHED))
print "Msg is ", binascii.hexlify(msg)
tcpCliSock.send(msg)
time.sleep(1)

msg = ip_in_binary_str + binascii.unhexlify(RemoveBlankInMiddle(EVENT_READYFOR_SENDITEM))
print "Msg is ", binascii.hexlify(msg)
tcpCliSock.send(msg)
time.sleep(1)

while(not exit_flag):

	data = raw_input('> ')
	if not data:
		print "No data to send"
		break

	msg = ip_in_binary_str + binascii.unhexlify(RemoveBlankInMiddle(data))
	print "Msg is ", binascii.hexlify(msg)
	tcpCliSock.send(msg)

print "Exiting..."
tcpCliSock.close()
