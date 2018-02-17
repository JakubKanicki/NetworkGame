from .packet import Packet
from .packetType import PacketType

class PacketInvalid(Packet):
	
	def __init__(self):
		super().__init__(PacketType.INVALID)
	
	def writeData(self, stream):
		pass
	
	def readData(self, stream):
		pass