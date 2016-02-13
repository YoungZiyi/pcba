# -*- coding: utf-8 -*-

from bxtcommon import *
import sys

listenSocket = listenOn(CLIENT_HOST, CLIENT_PORT)
content = "FT01_GiveItemFinish"
response = None
try:
	sendToPeer(SERVER_HOST, SERVER_PORT, content)
	time.sleep(1)
	response = recvFromPeer(listenSocket)
except Exception, e:
	print e
finally:
	if(response and "Error" in response):
		print "test passed"
	else:
		print "---------------------Test FAIL!-------------------"