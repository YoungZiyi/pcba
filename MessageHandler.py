# -*- coding: utf-8 -*-
#!/usr/bin/env python

import pdb

from Message import *
from Device import *
from BxtException import *
from BxtLogger import *

def handle_msg(current_device, event):

	print "DDDDDDDDDD--", current_device.name, "--event:", event, "--status:", current_device.status, "--otem_status:", current_device.item_status, "--prepare_count:", current_device.prepare_count

	# log all event
	writeInfo("CLIENT: [%s] SENT: [%s]" % (current_device.name, event))

	# RES_STATUS_BUSY
	if (event == RES_STATUS_BUSY and (current_device not in [device_sbjng])):	
		#Ignore this event for every device except device_sbjng
		return

	if (event == EVENT_DEVICE_WARNING_2):
		# 这时急停报警按钮
		current_device.ChangeStatusTo(S_BROKEN)
		writeWarning("[%s] STOPED SUDDENLY" % current_device.name)
		return
		
	if (current_device in [device_ict]):
		if (event in [EVENT_READYFOR_SENDITEM_OK, EVENT_READYFOR_SENDITEM_NG, EVENT_READYFOR_SENDITEM]):
			current_device.ChangeStatusTo(S_READY_TO_SEND_ITEM)
			#If the next device is available, then send ask it to rece item.
			if(device_yz1.status in [S_IDLE, S_HALF_READY_TO_RECV_ITEM]):
				device_yz1._SendInstruction(INSTRUCTION_YZ_MOVE_LEFT_AND_RECV_ITEM)
				device_yz1.prepare_count = device_yz1.prepare_count + 1
			elif(device_yz1.status in [S_READY_TO_RECV_ITEM]):
				device_ict._SendInstruction(INSTRUCTION_DEVICE_SENDITEM)
				device_ict.ChangeStatusTo(S_SENDING)
		elif (event == EVENT_SENDITEM_FINISHED):
			current_device.ChangeStatusTo(S_IDLE)
		else:
			writeWarning("[%s] IS NOT RECOGNIZED FOR DEVICE [%s]" % (event, current_device.name))
	elif (current_device == device_yz1):
		if (event in [EVENT_AVAILABLE, RES_STATUS_AVAILABLE, EVENT_SENDITEM_FINISHED]):
			#Prepare to recv item in advance
			current_device._SendInstruction(INSTRUCTION_YZ_MOVE_LEFT_AND_RECV_ITEM)
			current_device.status = S_PREPARING_TO_RECV
			current_device.prepare_count = 1
		if(event in [EVENT_READYFOR_GETITEM_LEFT]):
			if(current_device.status not in [S_PREPARING_TO_RECV, S_HALF_READY_TO_RECV_ITEM]):
				writeWarning("[%s] send event [%s] while its satus is [%d]" % (current_device.name, event, current_device.status))
				return
			if(current_device.prepare_count == 1):
				current_device.ChangeStatusTo(S_HALF_READY_TO_RECV_ITEM)
				if(device_ict.status == S_READY_TO_SEND_ITEM):
					current_device._SendInstruction(INSTRUCTION_YZ_MOVE_LEFT_AND_RECV_ITEM)
					current_device.prepare_count = 2
				else:
					#Wait here and not to proceed until the ICT device is ready to send item.
					pass
			elif(current_device.prepare_count == 2):
				current_device.ChangeStatusTo(S_READY_TO_RECV_ITEM)
				if(device_ict.status == S_READY_TO_SEND_ITEM):
					device_ict._SendInstruction(INSTRUCTION_DEVICE_SENDITEM)
					device_ict.ChangeStatusTo(S_SENDING)
				else:
					writeWarning("WARNNING: YZ1 IS READY TO RECV ITEM, BUT THE FT IS NOT READY TO SEND ITEM. ANYBODY STEAL THE ITEM?")
		elif(event==EVENT_GETITEM_FINISHED):
			current_device.ChangeStatusTo(S_READY_TO_SEND_ITEM)
			if(ft1.status == S_IDLE):
				current_device._SendInstruction(INSTRUCTION_YZ_MOVE_LEFT_AND_SEND_ITEM)
				current_device.ChangeStatusTo(S_SENDING)
			elif(ft2.status == S_IDLE)
				current_device._SendInstruction(INSTRUCTION_YZ_MOVE_RIGHT_AND_SEND_ITEM)
				current_device.ChangeStatusTo(S_SENDING)
			else:
				writeInfo("%s is waiting for an available FT" % (current_device.name))
		else:
			writeWarning("[%s] IS NOT RECOGNIZED FOR DEVICE [%s]" % (event, current_device.name))
	elif(current_device in [device_ft1, device_ft2]):
		if (event in [EVENT_AVAILABLE, RES_STATUS_AVAILABLE, EVENT_SENDITEM_FINISHED]):
			current_device.ChangeStatusTo(S_IDLE)
		elif(event == EVENT_GETITEM_FINISHED):
			current_device.ChangeStatusTo(S_WITH_ITEM)
		elif(event in [EVENT_READYFOR_SENDITEM_NG,EVENT_READYFOR_SENDITEM_OK]):
			current_device.ChangeStatusTo(S_READY_TO_SEND_ITEM)
			if(event == EVENT_READYFOR_SENDITEM_OK):
				current_device.ChangeItemStatusTo(ITEM_STATUS_OK)
			else:
				current_device.ChangeItemStatusTo(ITEM_STATUS_NG)
			
			if(current_device == device_ft1):
				if(device_yz2.status in [S_IDLE] or (device_yz2.status == S_HALF_READY_TO_RECV_ITEM and device_yz2.direction == DIRECTION_LEFT)):
					device_yz2._SendInstruction(INSTRUCTION_YZ_MOVE_LEFT_AND_RECV_ITEM)
					device_yz2.prepare_count = device_yz2.prepare_count + 1
				elif(device_yz2.status in [S_READY_TO_RECV_ITEM]):
					current_device._SendInstruction(INSTRUCTION_DEVICE_SENDITEM)
					current_device.ChangeStatusTo(S_SENDING)
				else:
					writeInfo("%s is waiting for yz2 to be available" % (current_device.name))
			elif(current_device == device_ft2):
				if(device_yz2.status in [S_IDLE] or (device_yz2.status == S_HALF_READY_TO_RECV_ITEM and device_yz2.direction == DIRECTION_RIGHT)):
					device_yz2._SendInstruction(INSTRUCTION_YZ_MOVE_RIGHT_AND_RECV_ITEM)
					device_yz2.prepare_count = device_yz2.prepare_count + 1
				elif(device_yz2.status in [S_READY_TO_RECV_ITEM]):
					current_device._SendInstruction(INSTRUCTION_DEVICE_SENDITEM)
					current_device.ChangeStatusTo(S_SENDING)
				else:
					writeInfo("%s is waiting for yz2 to be available" % (current_device.name))
		else:
			writeWarning("[%s] IS NOT RECOGNIZED FOR DEVICE [%s]" % (event, current_device.name))
	elif (current_device in [device_yz2]):
		if (event in [EVENT_AVAILABLE, RES_STATUS_AVAILABLE, EVENT_SENDITEM_FINISHED]):
			current_device.ChangeStatusTo(S_IDLE)
		elif(event in [EVENT_READYFOR_GETITEM_LEFT, EVENT_READYFOR_GETITEM_RIGHT]):
			#TODO do some asserting
			if(current_device.direction == DIRECTION_LEFT):
				if(current_device.prepare_count == 1):
					current_device.ChangeStatusTo(S_HALF_READY_TO_RECV_ITEM)
					current_device._SendInstruction(INSTRUCTION_YZ_MOVE_LEFT_AND_RECV_ITEM)
					current_device.prepare_count = current_device.prepare_count + 1
				elif(current_device.prepare_count == 2):
					current_device.ChangeStatusTo(S_READY_TO_RECV_ITEM)
					if(device_ft1.status == S_READY_TO_SEND_ITEM):
						device_ft1._SendInstruction(INSTRUCTION_DEVICE_SENDITEM)
						device_ft1.ChangeStatusTo(S_SENDING)
					else:
						writeWarning("YZ2 IS READY TO RECV ITEM, BUT THE [%s] IS of status [%d]."%(device_ft1.name, device_ft1.satus))
						#Change it status to idel so the other FT device can use the YZ device if they need.
						current_device.ChangeStatusTo(S_IDLE)
				else:
					writeWarning("[%s] IS with a prepare_count of [%d]" % (current_device.name, current_device.prepare_count))
			elif(current_device.direction == DIRECTION_RIGHT):
				if(current_device.prepare_count == 1):
					current_device.ChangeStatusTo(S_HALF_READY_TO_RECV_ITEM)
					current_device._SendInstruction(INSTRUCTION_YZ_MOVE_RIGHT_AND_RECV_ITEM)
					current_device.prepare_count = current_device.prepare_count + 1
				elif(current_device.prepare_count == 2):
					current_device.ChangeStatusTo(S_READY_TO_RECV_ITEM)
					if(device_ft2.status == S_READY_TO_SEND_ITEM):
						device_ft2._SendInstruction(INSTRUCTION_DEVICE_SENDITEM)
						device_ft2.ChangeStatusTo(S_SENDING)
					else:
						writeWarning("YZ2 IS READY TO RECV ITEM, BUT THE [%s] IS of status [%d]."%(device_ft2.name, device_ft2.satus))
						#Change it status to idel so the other FT device can use the YZ device if they need.
						current_device.ChangeStatusTo(S_IDLE)
				else:
					writeWarning("[%s] IS with a prepare_count of [%d]" % (current_device.name, current_device.prepare_count))				
			else:
				writeWarning("[%s] reported [%d] but with a bad direction [%d]" % (current_device.name, event, current_device.direction))
		elif(event == EVENT_GETITEM_FINISHED):
			current_device.ChangeStatusTo(S_READY_TO_SEND_ITEM)
			if(current_device.item_status == ITEM_STATUS_OK):
				current_device._SendInstruction(INSTRUCTION_YZ_MOVE_LEFT_AND_SEND_ITEM)
				current_device.ChangeStatusTo(S_SENDING)
			else:
				if(device_sbjng.status == S_IDLE):
					current_device._SendInstruction(INSTRUCTION_YZ_MOVE_RIGHT_AND_SEND_ITEM)
					current_device.ChangeStatusTo(S_SENDING)
				else:
					#Do nothing but wait.
					pass
		else:
			writeWarning("[%s] IS NOT RECOGNIZED FOR DEVICE [%s]" % (event, current_device.name))
	elif (current_device in [device_sbjng]):
		if(event == RES_STATUS_BUSY):
			current_device.ChangeStatusTo(S_WITH_ITEM)
		elif(event == EVENT_AVAILABLE):
			current_device.ChangeStatusTo(S_IDLE)
			if (device_yz2.status == S_READY_TO_SEND_ITEM):
				device_yz2._SendInstruction(INSTRUCTION_YZ_MOVE_RIGHT_AND_SEND_ITEM)
				current_device.ChangeStatusTo(S_SENDING)
		else:
			print "WARNING: EVENT [%s] IS NOT RECOGNIZED FOR DEVICE [%s]" % (event, current_device.name)
	else:
		print "WARNING: DEVICE IS NOT RECOGNIZED [%s]" % device.name
