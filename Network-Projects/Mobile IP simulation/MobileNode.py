import commands
from frame import Frame
from socket import *
import sys

NUMARGS = 2

# Check to ensure all arguments are accounted for
if (len(sys.argv) != (1 + NUMARGS)):
	print 'Please run this file in the following format:'
	print 'RTFMobileIPMobileNode.py <HomeAgentIP> <ForeignAgentIP>'
	sys.exit()

addrHA = sys.argv[1]
addrFA = sys.argv[2]
print 'Home address: ' + addrHA
print 'Foreign address: ' + addrFA

# Listening Socket
UDP_IP = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1]
UDP_PORT = 9000

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
sendFrame = Frame(fTyp, fIPA, fIPB, fMsg)
# Byte array for receiving data
recvData = bytearray()

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

def sendAFrame(typ,IPA,IPB,Msg,Addr,Prt):
	sendFTyp = typ
	sendFIPA = IPA
	sendFIPB = IPB
	sendFMsg = Msg
	newFrame = Frame(sendFTyp,sendFIPA,sendFIPB,sendFMsg)
	sock.sendto(newFrame.encodeFrame(), (Addr, Prt))
	

while True:
	choice = raw_input('Please enter reg (to register), drg (to deregister), or exit (to exit): ')
	
	if (choice == 'reg'):
		print '\nRegistering with Foreign Agent.\nListening...'
		
		# Send frame to register with FA
		sendAFrame(1, UDP_IP, addrHA, 'Msg', addrFA, 8000)
		
		# Listen
		while True:
			# Receive a frame and store it in recvFrame; reset recvData
			data, addr = sock.recvfrom(1024)
			for c in data:
				recvData.append(c)
			recvFrame = sendFrame.decodeFrame(recvData)
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
			if (fTyp == 8):
				# Message has been received from correspondent
				break
			else:
				print ''
				print 'Frame type invalid!'
			# End if statement
		# End While loop
		print ''
		print 'Message from Correspondent:'
		print fMsg
		print ''
		print 'Please enter a response:'
		fMsg = raw_input()
		
		# Respond to Correspondent
		trgtIP = fIPA
		sendAFrame(9, UDP_IP, '0.0.0.0', fMsg, trgtIP, 6000)
	elif (choice == 'drg'):
		print '\nDeregistering with Foreign Agent.\n'
		
		# Send frame to register with FA
		sendAFrame(2, UDP_IP, addrHA, 'Msg', addrFA, 8000)
	elif (choice == 'exit'):
		break
	else:
		print '\n"' + choice + '" is not a valid option.\n'

print ''
print 'Menu has been exited. Alerting Foreign Agent'

# Announce turning off to Foreign Agent
fTyp = 0
fIPA = '0.0.0.0'
fIPB = '0.0.0.0'
fMsg = ''
		
# Set target to Foreign Agent
trgtIP = addrFA
trgtPrt = 8000

# Create and send the frame
sendFrame = Frame(fTyp, fIPA, fIPB, fMsg)
sock.sendto(sendFrame.encodeFrame(), (trgtIP, trgtPrt))
