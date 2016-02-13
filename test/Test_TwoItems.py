from bxtcommon import *

listenSocket = listenOn(CLIENT_HOST, CLIENT_PORT)
response1 = None
response2 = None
try:
	content = "FT01_TestFinish_OK"
	sendToPeer(SERVER_HOST, SERVER_PORT, content)
	time.sleep(1)
	response1 = recvFromPeer(listenSocket)

	content = "FT01_TestFinish_OK"
	sendToPeer(SERVER_HOST, SERVER_PORT, content)
	time.sleep(1)
	response2 = recvFromPeer(listenSocket)
	
except Exception, e:
	print e
finally:
	if(response2 and "HasTwoItems" in response2):
		print "test passed"
	else:
		print "---------------------Test FAIL!-------------------"