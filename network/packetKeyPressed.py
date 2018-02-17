from .packet import Packet
from .packetType import PacketType
from . import streamUtil
from directions import Direction
from keys import Key
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
		if (self.keyId == Key.UP):
			map.player.move(map, Direction.UP)
		if (self.keyId == Key.DOWN):
			map.player.move(map, Direction.DOWN)
		if (self.keyId == Key.LEFT):
			map.player.move(map, Direction.LEFT)
		if (self.keyId == Key.RIGHT):
			map.player.move(map, Direction.RIGHT)
		if (self.keyId == Key.FIRE):
			map.spawnProjectile(map.player.x, map.player.y, 0, map.player.direction)