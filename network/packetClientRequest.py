from .packet import Packet
from .packetType import PacketType
from . import streamUtil
import logging
import game
from .packetFullMapSync import PacketFullMapSync


class PacketClientRequest(Packet):
	REQ_INVALID = 0
	REQ_FULL_MAP_SYNC = 1

	def __init__(self, reqType=REQ_INVALID):
		super().__init__(PacketType.CLIENT_REQUEST)
		self.reqType = reqType

	def writeData(self, stream):
		streamUtil.writeInt(stream, self.reqType, 1)

	def readData(self, stream):
		self.reqType = streamUtil.readInt(stream, 1)

	def execute(self, map):
		logging.info('Executing client request type #' + str(self.reqType))
		if(self.reqType == PacketClientRequest.REQ_FULL_MAP_SYNC):
			game.networkHandler.queueOutbound(PacketFullMapSync(map))
