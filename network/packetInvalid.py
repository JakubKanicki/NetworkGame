from .packet import Packet
from .packetType import PacketType
import logger
import shared


class PacketInvalid(Packet):
	
	def __init__(self):
		super().__init__(PacketType.INVALID)
	
	def writeData(self, stream):
		pass
	
	def readData(self, stream):
		logger.debug('READING PACKET INVALID: ' + str(stream.read()))

	def execute(self, map):
		logger.debug('-EXECUTING-INVALID-PACKET-')
		shared.invalidPacketCount += 1