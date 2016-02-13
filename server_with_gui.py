# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import Qt
from PyQt4 import *
from spiderman import *
import sys
from threading import *
import socket
import time
from struct import pack, unpack
import signal
import binascii
import string
import select


from Message import *
from Device import *
from BxtLogger import *
from BxtException import *
from RunningMode import *

		
class ExampleApp(QtGui.QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(ExampleApp, self).__init__(parent)
		self.setupUi(self)

	def send_msg_to_server(self):
		objectName = str(self.sender().objectName())

		deviceNameInStr = objectName.split('_', 1)[0]
		variableNameInStr = objectName.split('_', 1)[1]
		
		msg = globals()[variableNameInStr]
		print deviceNameInStr, "#", msg
		
		ip = deviceName_IP_Map[deviceNameInStr]
		ip2 = socket.inet_aton(ip)
		ip_in_int = unpack("!I", ip2)[0];
		ip_in_binary_str = pack("!i",ip_in_int)
		
		msg = ip_in_binary_str + binascii.unhexlify(RemoveBlankInMiddle(msg))
		
		sock = getSocketByDeviceName(deviceNameInStr)
		sock.send(msg)

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	form = ExampleApp()
	form.show()
	InitSockets()
	t = Thread(target=ListenFromServer, args = (form.log, ))
	t.daemon = True
	t.start()

	app.exec_()