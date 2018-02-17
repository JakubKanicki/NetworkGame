from .packet import Packet
from .packetType import PacketType
from . import streamUtil


class PacketMessage(Packet):

	def __init__(self, msg=None):
		super().__init__(PacketType.MESSAGE)
		self.msg = msg

	def writeData(self, stream):
		streamUtil.writeString(stream, self.msg)

	def readData(self, stream):
		self.msg = streamUtil.readString(stream)

	def execute(self):
		print('Executing Message Packet: ' + str(self.msg))