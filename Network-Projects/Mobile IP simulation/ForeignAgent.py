#-------------------------------------------------------#
# Student Name: Robert Ferrill & Ann Jones				#
# Course: COSC 4653 - Advanced Networks 				#
# Assignment: #3 - Mobile IP Simulation					#
# File name: RFTMobileIPForeignAgent.py					#
# Program's Purpose: Act as the foreign agent in a 		#
#	simulation of Mobile IP.							#
#-------------------------------------------------------#

from frame import Frame
from socket import *
import commands

# Listening Socket
UDP_IP = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1]
UDP_PORT = 8000

# Variables for receiving frames
fTyp = 0
fIPA = '127.0.0.1'
fIPB = '127.0.0.1'
fMsg = 'Lorem Ipsum'
recvFrame = Frame(fTyp, fIPA, fIPB, fMsg)
# Variables for sending frames
sfTyp = 0
sfIPA = '127.0.0.1'
sfIPB = '127.0.0.1'
sfMsg = 'Lorem Ipsum'
sendFrame = Frame(sfTyp, sfIPA, sfIPB, sfMsg)
# Byte array for receiving data
recvData = bytearray()

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# "Registry"
addrMN = ''
addrHA = ''

# Destination variables
trgtIP = '127.0.0.1'
trgtPrt = 8000

needToSend = False

while True:
	# Receive a frame and store it in recvFrame; reset recvData
	data, addr = sock.recvfrom(1024)
	for c in data:
		recvData.append(c)
	recvFrame = recvFrame.decodeFrame(recvData)
	recvData = bytearray()
	fTyp = recvFrame.getType()
	fIPA = recvFrame.getIpA()
	fIPB = recvFrame.getIpB()
	fMsg = recvFrame.getMessage()
	
	
	# Print out received data to visually confirm
	print ''
	print 'Received Type is: ' + str(fTyp)
	print 'Received IP A is: ' + fIPA
	print 'Received IP B is: ' + fIPB
	print 'Received Message is: ' + fMsg
	
	# Process received frame
	if (fTyp == 0):
		print ''
		print 'Mobile Node is shutting down'
		print 'Deregistering it.'
		
		# Clear the "Registry"
		addrHA = ''
		addrMN = ''
		
	elif (fTyp == 1):
		print ''
		print 'Mobile Node is registering'
		print 'Saving it and informing Home Agent'
		
		# Write to "Registry"
		addrHA = fIPB
		addrMN = fIPA
		
		needToSend = True
		sfTyp = 3
		sfIPA = UDP_IP
		sfIPB = fIPB
		sfMsg = ''
		
		# Set target to Home Agent
		trgtIP = fIPB
		trgtPrt = 7000
		
	elif (fTyp == 2):
		print ''
		print 'Mobile Node is deregistering'
		print 'Deleting it and informing Home Agent'
		
		needToSend = True
		sfTyp = 4
		sfIPA = UDP_IP
		sfIPB = fIPB
		sfMsg = ''
		
		# Set target to Home Agent
		trgtIP = fIPB
		trgtPrt = 7000
		
		# Clear the "Registry"
		addrHA = ''
		addrMN = ''
		
	elif (fTyp == 7):
		print ''
		print 'Home Agent is forwarding a message'
		print 'Passing it to Mobile Node'
		
		needToSend = True
		sfTyp = 8
		sfIPA = fIPA
		sfIPB = '0.0.0.0'
		sfMsg = fMsg
		
		# Set target to Mobile Node
		trgtIP = addrMN
		trgtPrt = 9000
	else:
		print ''
		print 'Frame type invalid!'
	# End of if statements
	
	if (needToSend):
		# Reset Boolean
		needToSend = False
		
		# Create and send the frame built in the if statements above
		sendFrame = Frame(sfTyp, sfIPA, sfIPB, sfMsg)
		sock.sendto(sendFrame.encodeFrame(), (trgtIP, trgtPrt))
	# End of Sending

# End of Program
