# Ann Jones
# Course: COSC 4653 Advanced Networks
# Assignment: 2 = Link-Layer Switch Simulation - Part 1
# File Name: jonesSS.py
# Program's Purpose:  Receives the frame, checks if source MAC address is stored in the switch table
#                       if stored, update time
#                       if not stored and not full, store source MAC address and arrival time in table
#                       if not stored and full, print Warning message.
#                       x is source MAC address, y is corresponding interface number
#                     Checking for destination MAC address
# Program's Limitations:
# Development Computer:
# Operating System: Linux Mint
# IDE: Pycharm
# Compiler:

from socket import *
from sys import argv
import random
from time import sleep
from datetime import datetime

#check for input on command line
if len(argv) < 3:
    print 'python JonesSS <port #> <maximum table size> <maximum aging time>'
#variables
maxSize = int(argv[2])
maxTime = int(argv[3])
port = int(argv[1])
host = ''
data = {}
currentTime = datetime.now()
difference = 0

#create socket and bind
serverSocket = socket(AF_INET, SOCK_DGRAM)

address = (host, port)
serverSocket.bind(address)

#receive frame from TS
while 1:
    d, address = serverSocket.recvfrom(1024)
    
    iNumber, source, dest = d.split(' ')
    if source in data:
        currentTime = datetime.now()
        data[source] = (currentTime, data[source][1])
    if len(data) < maxSize and source not in data:
        data[source] = (currentTime,iNumber)
        print 'ADD: Adding MAC address' + source + ' on interface ' + iNumber + ' to switch table'
    if len(data) >= maxSize:
        print 'WARNING: Could not add MAC address '+ source + ' on interface ' + iNumber + ' to switch table'
    #after completing step 1
    if dest not in data:
        print 'BROADCAST: Broadcasting frame containing MAC address ' + dest
    if dest in data and iNumber in data:
        print 'DISCARD: Discarding frame containing MAC address ' + dest
    if (dest in data) and iNumber not in data:
        print 'FORWARD: Forwarding frame containing MAC address ' + dest + ' to interface ' + iNumber
    #after completing step 2
    for k in data.keys():
        if(datetime.now()-data[k][0]).seconds >= maxTime:
            data.pop(k, None)
            







 


