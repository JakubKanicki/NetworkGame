from .packet import Packet
from .packetType import PacketType
from . import streamUtil
import logger
from map import Map


class PacketFullMapSync(Packet):

	def __init__(self, map=None):
		super().__init__(PacketType.FULL_MAP_SYNC)
		self.map = map

	def writeData(self, stream):
		streamUtil.writeInt(stream, self.map.sizeX, 1)
		streamUtil.writeInt(stream, self.map.sizeY, 1)
		for i in range(0, self.map.sizeY):
			for j in range(0, self.map.sizeX):
				streamUtil.writeInt(stream, self.map.terrain[i][j], 1)
				logger.debug('Transmitting X%i Y%i' % (j, i))
				print('Transmitting X%i Y%i' % (j, i))

	def readData(self, stream):
		sizeX = streamUtil.readInt(stream, 1)
		sizeY = streamUtil.readInt(stream, 1)
		print('Receiving map sized X%i Y%i' % (sizeX, sizeY))
		self.map = Map(sizeX, sizeY)
		self.map.terrain = []
		for i in range(0, self.map.sizeY):
			temp = []
			for j in range(0, self.map.sizeX):
				temp.append(streamUtil.readInt(stream, 1))
				logger.debug('Receiving X%i Y%i' % (j, i))
				print('Receiving X%i Y%i' % (j, i))
			self.map.terrain.append(temp)

	def execute(self, map):
		logger.debug('Executing packet full map sync...')
		map.terrain = self.map.terrain