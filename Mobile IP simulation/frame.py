#-------------------------------------------------------#
# Student Name: Robert Ferrill & Ann Jones				#
# Course: COSC 4653 - Advanced Networks 				#
# Assignment: #3 - Mobile IP Simulation					#
# File name: frame.py									#
# Program's Purpose: Contain a Frame object for use in	#
#	the Mobile IP Simulation assignment to be imported	#
#	by each of the other programs. Allow the creation	#
#	of frames in a standardized format, which can be	#
#	transfered using sockets and then decoded.			#
#-------------------------------------------------------#

class Frame(object):
	
	fType = 0
	ipA = '127.0.0.1'
	ipB = '127.0.0.1'
	message = ''
	
	#encodedFrame = bytearray()
	# Encoded frame will contain the following bytes:
	#	0: fType
	#	1: ipA #1
	#	2: ipA #2
	#	3: ipA #3
	#	4: ipA #4
	#	5: ipB #1
	#	6: ipB #2
	#	7: ipB #3
	#	8: ipB #4
	#	9 Onwards: message
	#	Final Byte: integer value of 0
	
	# Constructor
	def __init__(self, fType, ipA, ipB, message):
		self.fType = fType
		self.ipA = ipA
		self.ipB = ipB
		self.message = message
		self.encodedFrame = bytearray()
		# Encodes the frame
		# Endode fType
		self.encodedFrame.append(self.fType)
		
		# Encode ipA
		dividedIPA = self.ipA.split('.')
		for b in dividedIPA:
			self.encodedFrame.append(int(b))
		
		# Encode ipB
		dividedIPB = self.ipB.split('.')
		for b in dividedIPB:
			self.encodedFrame.append(int(b))
		
		# Encode message
		for c in self.message:
			self.encodedFrame.append(c)
		
		# Add end character of 0
		self.encodedFrame.append(0)
	
	# Returns the byte array containing the frame's data
	def encodeFrame(self):
		return self.encodedFrame
	
	#global decodeFrame
	# Turns a received byte array into a frame
	def decodeFrame(self,dataBytes):
		# Decode frame type
		newFType = int(dataBytes[0])
		
		# Decode/reassemble ipA
		newIPA = str(int(dataBytes[1]))
		newIPA += '.'
		newIPA += str(int(dataBytes[2]))
		newIPA += '.'
		newIPA += str(int(dataBytes[3]))
		newIPA += '.'
		newIPA += str(int(dataBytes[4]))
		
		# Decode/reassemble ipB
		newIPB = str(int(dataBytes[5]))
		newIPB += '.'
		newIPB += str(int(dataBytes[6]))
		newIPB += '.'
		newIPB += str(int(dataBytes[7]))
		newIPB += '.'
		newIPB += str(int(dataBytes[8]))
		
		# Decode message
		newMessage = ''
		# Iterate through the rest of the array
		for i in range(9, len(dataBytes)):
			# Check for the value of 0 placed at the end
			if (int(dataBytes[i]) != 0):
				# Convert the byte into a character, add it to message
				newMessage += chr(int(dataBytes[i]))
			else:
				break
		
		# Return the new frame
		return Frame(newFType, newIPA, newIPB, newMessage)
	
	# Getters to use on a decoded fram
	def getType(self):
		return self.fType
	def getIpA(self):
		return self.ipA
	def getIpB(self):
		return self.ipB
	def getMessage(self):
		return self.message


# Test Frame Class
#testType = 3
#testIPA = '10.0.0.7'
#testIPB = '10.0.0.6'
#testMessage = 'This is a message to be sent between clients in a frame!'

#print 'Type is: ' + str(testType)
#print 'IP A is: ' + str(testIPA)
#print 'IP B is: ' + str(testIPB)
#print 'Message is: ' + str(testMessage)

#testFrame1 = Frame(testType, testIPA, testIPB, testMessage)

#print ''
#print 'Encoding and decoding data...'
#print ''

#encodedFrame1 = bytearray()

#encodedFrame1 = testFrame1.encodeFrame()

#testFrame2 = testFrame1.decodeFrame(encodedFrame1)

#print 'Type is: ' + str(testFrame2.getType())
#print 'IP A is: ' + str(testFrame2.getIpA())
#print 'IP B is: ' + str(testFrame2.getIpB())
#print 'Message is: ' + str(testFrame2.getMessage())
