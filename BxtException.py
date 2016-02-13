# -*- coding: utf-8 -*-
#!/usr/bin/env python 

class BxtException(Exception):
	pass

class ExceptionUnsupportedMsg(BxtException):
	pass
class ExceptionItemStatusUnknown(BxtException):
	pass
class ExceptionCommunication(BxtException):
	pass
class ExceptionMessageFromUnknonwSource(BxtException):
	pass
