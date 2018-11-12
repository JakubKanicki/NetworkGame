from .packet import Packet
from .packetType import PacketType
import logging
import shared


class PacketInvalid(Packet):
	
	def __init__(self):
		super().__init__(PacketType.INVALID)
	
	def writeData(self, stream):
		pass
	
	def readData(self, stream):
		logging.warning('READING PACKET INVALID: ' + str(stream.read()))

	def execute(self, map):
		logging.warning('-EXECUTING-INVALID-PACKET-')
		shared.invalidPacketCount += 1