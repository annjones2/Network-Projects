# Ann Jones
# Course: COSC 4653 Advanced Networks
# Assignment: 3 = Mobile IP Simulation
# File Name: jonesTS.py
# Program's Purpose:  Simulate the mobile IP protocol. The Correspondent program is a client process
#                     It allows the user to send a message to a mobile node and receives the response.
#                     When exchanging messages with the mobile node, it will also send a message to the home agent.
#                     Listens on port 6000.
#                     Gets its own IP adddress and home agent's IP address
#                     python Correspondent.py <home_agent_IP_address> <own.ip>
# Program's Limitations:
# Development Computer:
# Operating System: Linux Mint
# IDE: Pycharm
# Compiler:

from frame import Frame
from socket import *
from sys import *
import commands

# Listening Socket
UDP_IP = commands.getoutput("/sbin/ifconfig").split("\n")[1].split()[1]
UDP_PORT = 6000

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

# Destination variables
trgtIP = '127.0.0.1'
trgtPrt = 6000

needToSend = False

#ckeck argument
if len(argv) < 1:
    print 'python Correspondent <home_agent_IP_address>'

addrHA = argv[1]

while True:
    print 'Type in message to send: '
    message = raw_input()
    #send message to mobile node
    sfTyp = 5
    sfIPA = UDP_IP
    sfIPB = addrHA
    sfMsg = message

    #set target to home agent
    trgtIP = addrHA
    trgtPrt = 7000
    sfMsg = message
    #this informs correspondent that no mobile node wtih that IP is registered
    sendFrame = Frame(sfTyp, sfIPA, sfIPB, sfMsg)
    sock.sendto(sendFrame.encodeFrame(), (trgtIP, trgtPrt))
    
    print '\nWaiting for a response...\n'
    
    # Receive a response
    data, addr = sock.recvfrom(1024)
    for c in data:
        recvData.append(c)
    recvFrame = recvFrame.decodeFrame(recvData)
    recvData = bytearray()
    fTyp = recvFrame.getType()
    fIPA = recvFrame.getIpA()
    fIPB = recvFrame.getIpB()
    fMsg = recvFrame.getMessage()
    if (fTyp == 6):
		# Mobile node wasn't registered
        print 'Mobile Node is not registered with Home Agent\n'


    elif (fTyp == 9):
        print 'Message from Mobile Node: ' + fMsg + '\n'
        
    else:
        print 'Frame type invalid\n'


#recv and send packet to and from mobile node
#when exchanging messages, send message to home agent.
