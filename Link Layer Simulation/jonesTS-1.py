# Ann Jones
# Course: COSC 4653 Advanced Networks
# Assignment: 2 = Link-Layer Switch Simulation - Part 1
# File Name: jonesTS.py
# Program's Purpose:  Traffic Simulator, modeled as a client process, generates link-layer frames
#                     sending at random times to the switch simulator. Source and destination MAC
#                     addresses are read from a text file passed to the TS from command line.
#                     Four arguments passed:  IP address, port number, config file name, max random interval
# Program's Limitations:
# Development Computer:
# Operating System: Linux Mint
# IDE: Pycharm
# Compiler:
import struct
from socket import *
from sys import argv
import random
from time import sleep
from struct import *
from signal import *

import argparse

#error handling for arguments or file not found
if len(argv) < 4:
    print 'python jonesTS <IP addr> <port #> <config filename> <max random interval>'
try:
    open(argv[3],"r")
except:
    print 'file not found'
    exit()

# variables from command line
host = argv[1]
port = int(argv[2])
#variables
macAddress = []

clientSocket = socket(AF_INET, SOCK_DGRAM)
address = (host, port)

# associate source MAC address with interface number using dictionary
dictionary = {}

#open argv3 file, key to value
with open(argv[3]) as file1:
    for l in file1:
        (k, v) = l.split()
        dictionary[k] = int(v)
        macAddress.append(k)
#allow user to kill traffic simulator using signal, SIGINT
def sig_han(signal,frame):
  clientSocket.sendto('traffic stopped\n', address)
  print('\nkilling traffic simulator')
  exit(0)
signal(SIGINT, sig_han)

#randomly set source Mac address and desintation MAC address of each frame
while 1:
    sourceMac = macAddress[random.randrange(0,len(macAddress)-1)]
    destMac = macAddress[random.randrange(0, len(macAddress) - 1)]
    #interval each packet is sent is chosen by user by way of argv[4]
    sleep(random.randrange(0,int(argv[4])))
    #frame format is int value, sourceMac, destMac
    trafSim = str(dictionary[sourceMac]) + ' ' + sourceMac + ' ' + destMac + '\n'
    clientSocket.sendto(trafSim, address)
    #print trafSim
    



