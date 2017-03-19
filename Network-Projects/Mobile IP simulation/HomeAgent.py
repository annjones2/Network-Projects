# Ann Jones
# Course: COSC 4653 Advanced Networks
# Assignment: 3 = Mobile IP Simulation
# File Name: Home Agent.py
# Program's Purpose:  Simulate the mobile IP protocol. The Home Agent program is a server process.
#                     Listens on port 7000.
#                     Receives a message from foreign agent (to register/deregister mobile node)
#                     Receives a message from a correspondent to SEND to mobile node
#                     Forwards a message from a correspondent to be a mobile node (by way of foreign agent)
#                     Registration table with two columns in it: mobile node's permanent IP address, mobile node's COA
#                     Note: mobile node's COA is the same as IP address of foreign agent.
# Program's Limitations:
# Development Computer:
# Operating System: Linux Mint
# IDE: Pycharm
# Compiler:

#import frame format section
from socket import *
from sys import *
from frame import Frame

port = 7000
host = ''
serverSocket = socket(AF_INET, SOCK_DGRAM)
address = (host, port)
serverSocket.bind(address)

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

# "Registry"
addrMN = ''
addrHA = ''
addrFA = ''

# Destination variables
trgtIP = '127.0.0.1'
trgtPrt = 8000

needToSend = False


while True:
    # Receive a frame and store it in recvFrame; reset recvData
    data, address = serverSocket.recvfrom(1024)
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

    #Process received frame
    if (fTyp == 0):
        print "Correspondent is shutting down"
        print "Deregister"
        break
    #register mobile node wtih home agent
    elif (fTyp == 3):
        addrFA = fIPA
        addrMN = fIPB

        print 'register mobile node with home agent'
        print ''

    #Deregister
    elif (fTyp == 4):
        # Clear the "Registry"
        addrFA = ''
        addrMN = ''

    elif (fTyp == 5):
		if (len(addrFA) <= 1):
			print 'Received message from correspondent'
			print 'Mobile node not registered. Telling correspondent'
			
			needToSend = True
			sfTyp = 6
			sfIPA = '0.0.0.0'
			sfIPB = fIPB
			sfMsg = ''
			#destination to mobile node
			trgtIP = fIPA
			trgtPrt = 6000
			
		else:
			print 'Received message from correspondent'
			print 'Sending to foreign agent at ' + addrFA

			needToSend = True
			sfTyp = 7
			sfIPA = fIPA
			sfIPB = fIPB
			sfMsg = fMsg
			#destination to mobile node
			trgtIP = addrFA
			trgtPrt = 8000
    else:
		print '\nInvalid frame type'


    if (needToSend):
        # Reset Boolean
        needToSend = False

        # Create and send the frame built in the if statements above
        sendFrame = Frame(sfTyp, sfIPA, sfIPB, sfMsg)
        serverSocket.sendto(sendFrame.encodeFrame(), (trgtIP, trgtPrt))
        # End of Sending
