from .packet import Packet
from .packetType import PacketType
from . import streamUtil
import inputHandler
import logger

class PacketKeyPressed(Packet):

	def __init__(self, keyId=None):
		super().__init__(PacketType.KEY_PRESSED)
		self.keyId = keyId

	def writeData(self, stream):
		streamUtil.writeInt(stream, self.keyId, 1)

	def readData(self, stream):
		self.keyId = streamUtil.readInt(stream, 1)

	def execute(self, map):
		logger.debug('Executing packet key pressed: %d' % self.keyId)
		inputHandler.processNetworked(map, self.keyId)